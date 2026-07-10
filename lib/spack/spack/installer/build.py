# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Build subprocess (child) side of the new installer.

This module holds everything that runs in (or directly manages) a single build's child process:
the :func:`worker_function` entry point, the install steps it drives, and the loop-side
:class:`ChildInfo` handle the parent uses to talk to the child. See :mod:`spack.installer`
for the overall design."""

import glob
import io
import json
import os
import selectors
import shlex
import shutil
import signal
import sys
import tempfile
import traceback
from gzip import GzipFile
from multiprocessing import Process
from typing import TYPE_CHECKING, List, NamedTuple, Optional

from spack.vendor.typing_extensions import Protocol

import spack.binary_distribution
import spack.build_environment
import spack.builder
import spack.config
import spack.error
import spack.hooks
import spack.mirrors.mirror
import spack.sandbox
import spack.spec
import spack.store
import spack.url_buildcache
import spack.util.environment
import spack.util.filesystem as fs
import spack.util.lock
import spack.util.tty
from spack.installer.base import (
    ExitCode,
    FdInfo,
    InstallPolicy,
    IpcChannel,
    JobServerBase,
    JobserverInfo,
    ProcessExitNotifier,
)
from spack.old_installer import _do_fake_install, dump_packages
from spack.subprocess_context import GlobalStateMarshaler
from spack.util.executable import ProcessError

if sys.platform == "win32":
    from spack.installer.windows import WindowsSentinelBridge as ExitNotifier
    from spack.installer.windows import WindowsTee as Tee
    from spack.installer.windows import create_build_channels, make_state_stream
else:
    from spack.installer.posix import PosixExitNotifier as ExitNotifier
    from spack.installer.posix import PosixTee as Tee
    from spack.installer.posix import create_build_channels, make_state_stream

if TYPE_CHECKING:
    import spack.package_base

#: Suffix for temporary backup during overwrite install
OVERWRITE_BACKUP_SUFFIX = ".old"

#: Suffix for temporary cleanup during failed install
OVERWRITE_GARBAGE_SUFFIX = ".garbage"


class ProcessLike(Protocol):
    """The part of the ``multiprocessing.Process`` interface the event loop relies on. Tests
    provide synthetic implementations to exercise the loop without forking."""

    @property
    def pid(self) -> Optional[int]: ...

    @property
    def exitcode(self) -> Optional[int]: ...

    def terminate(self) -> None: ...

    def kill(self) -> None: ...

    def is_alive(self) -> bool: ...

    def join(self, timeout: Optional[float] = None) -> None: ...


class ChildInfo:
    """Loop-side handle to a running build: the child process and its IPC channels. Owns the
    prefix write lock while the build runs; on success ownership transfers to the pending
    ``AddSpecAction`` DB insert."""

    __slots__ = (
        "proc",
        "spec",
        "output_r_conn",
        "state_r_conn",
        "control_w_conn",
        "notifier",
        "log_path",
        "prefix_lock",
        "state_buffer",
    )

    def __init__(
        self,
        proc: ProcessLike,
        spec: spack.spec.Spec,
        output_r_conn: IpcChannel,
        state_r_conn: IpcChannel,
        control_w_conn: IpcChannel,
        notifier: ProcessExitNotifier,
        log_path: str,
    ) -> None:
        self.proc = proc
        self.spec = spec
        self.output_r_conn = output_r_conn
        self.state_r_conn = state_r_conn
        self.control_w_conn = control_w_conn
        self.notifier = notifier
        self.log_path = log_path
        self.prefix_lock: Optional[spack.util.lock.Lock] = None
        # Buffer for partially received state data from this child. Kept as raw bytes and split on
        # b"\n": the newline byte cannot occur inside a multi-byte UTF-8 sequence, so framing is
        # safe without decoding partial reads.
        self.state_buffer = b""

    def release_prefix_lock(self) -> None:
        if self.prefix_lock is not None:
            try:
                self.prefix_lock.release_write()
            except Exception:
                pass
        self.prefix_lock = None

    def register_with_selector(self, selector: selectors.BaseSelector, build_id: str) -> None:
        """Register output, state, and sentinel channels with the selector."""
        selector.register(self.output_r_conn, selectors.EVENT_READ, FdInfo(build_id, "output"))
        selector.register(self.state_r_conn, selectors.EVENT_READ, FdInfo(build_id, "state"))
        selector.register(
            self.notifier.fileobj, selectors.EVENT_READ, FdInfo(build_id, "sentinel")
        )

    def close(self, selector: selectors.BaseSelector) -> int:
        """Unregister and close file descriptors, and join the child process.
        Returns the exit code of the child process."""
        try:
            selector.unregister(self.output_r_conn)
        except (KeyError, OSError):
            pass
        try:
            selector.unregister(self.state_r_conn)
        except (KeyError, OSError):
            pass
        try:
            selector.unregister(self.notifier.fileobj)
        except (KeyError, ValueError, OSError):
            pass
        self.output_r_conn.close()
        self.state_r_conn.close()
        self.control_w_conn.close()
        self.notifier.close()
        self.proc.join()
        exit_code = self.proc.exitcode
        assert exit_code is not None, "Finished build should have exit code set"
        if hasattr(self.proc, "close"):  # No known equivalent in Python 3.6
            self.proc.close()
        return exit_code


def send_state(state: str, state_pipe: io.TextIOWrapper) -> None:
    """Send a state update message."""
    json.dump({"state": state}, state_pipe, separators=(",", ":"))
    state_pipe.write("\n")


def send_progress(current: int, total: int, state_pipe: io.TextIOWrapper) -> None:
    """Send a progress update message."""
    json.dump({"progress": current, "total": total}, state_pipe, separators=(",", ":"))
    state_pipe.write("\n")


def send_installed_from_binary_cache(state_pipe: io.TextIOWrapper) -> None:
    """Send a notification that the package was installed from binary cache."""
    json.dump({"installed_from_binary_cache": True}, state_pipe, separators=(",", ":"))
    state_pipe.write("\n")


def install_from_buildcache(
    mirrors: List[spack.url_buildcache.MirrorMetadata],
    spec: spack.spec.Spec,
    unsigned: Optional[bool],
    state_stream: io.TextIOWrapper,
) -> bool:
    # Skip if no configured mirror accepts this spec (select/exclude filters)
    if not any(
        m.matches_binary(spec, direction="fetch")
        for m in spack.mirrors.mirror.MirrorCollection(binary=True).values()
    ):
        return False

    send_state("fetching from build cache", state_stream)
    try:
        tarball_stage = spack.binary_distribution.download_tarball(
            spec.build_spec, unsigned, mirrors
        )
    except spack.binary_distribution.NoConfiguredBinaryMirrors:
        return False

    if tarball_stage is None:
        return False

    send_state("relocating", state_stream)
    spack.binary_distribution.extract_tarball(spec, tarball_stage, force=False)

    if spec.spliced:  # overwrite old metadata with new
        spack.store.STORE.layout.write_spec(spec, spack.store.STORE.layout.spec_file_path(spec))

    # now a block of curious things follow that should be fixed.
    pkg = spec.package
    if hasattr(pkg, "_post_buildcache_install_hook"):
        pkg._post_buildcache_install_hook()
    pkg.installed_from_binary_cache = True

    # inform also the parent that this package was installed from binary cache.
    send_installed_from_binary_cache(state_stream)

    return True


class PrefixPivoter:
    """Manages the installation prefix of a build."""

    def __init__(self, prefix: str, keep_prefix: bool = False) -> None:
        """Initialize the prefix pivoter.

        Args:
            prefix: The installation prefix path
            keep_prefix: Whether to keep a failed installation prefix
        """
        self.prefix = prefix
        #: Whether to keep a failed installation prefix
        self.keep_prefix = keep_prefix
        #: Temporary location for the original prefix
        self.tmp_prefix: Optional[str] = None
        self.parent = os.path.dirname(prefix)

    def __enter__(self) -> "PrefixPivoter":
        """Enter the context: move existing prefix to temporary location if needed."""
        if not self._lexists(self.prefix):
            return self
        # Move the existing prefix to a temporary location so the build starts fresh
        self.tmp_prefix = self._mkdtemp(
            dir=self.parent, prefix=".", suffix=OVERWRITE_BACKUP_SUFFIX
        )
        self._rename(self.prefix, self.tmp_prefix)
        return self

    def __exit__(
        self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[object]
    ) -> None:
        """Exit the context: cleanup on success, restore on failure."""
        if exc_type is None:
            # Success: remove the backup
            if self.tmp_prefix is not None:
                self._rmtree_ignore_errors(self.tmp_prefix)
            return

        # Failure handling:
        if self.keep_prefix and not issubclass(exc_type, BinaryCacheMiss):
            # Leave the failed prefix in place, discard the backup. Except for binary cache misses,
            # which is a scheduling failure and not a build failure.
            if self.tmp_prefix is not None:
                self._rmtree_ignore_errors(self.tmp_prefix)
        elif self.tmp_prefix is not None:
            # There was a pre-existing prefix: pivot back to it and discard the failed build
            garbage = self._mkdtemp(dir=self.parent, prefix=".", suffix=OVERWRITE_GARBAGE_SUFFIX)
            try:
                self._rename(self.prefix, garbage)
                has_failed_prefix = True
            except FileNotFoundError:  # build never created the prefix dir
                has_failed_prefix = False
            self._rename(self.tmp_prefix, self.prefix)
            if has_failed_prefix:
                self._rmtree_ignore_errors(garbage)
        elif self._lexists(self.prefix):
            # No backup, just remove the failed installation
            garbage = self._mkdtemp(dir=self.parent, prefix=".", suffix=OVERWRITE_GARBAGE_SUFFIX)
            self._rename(self.prefix, garbage)
            self._rmtree_ignore_errors(garbage)

    def _lexists(self, path: str) -> bool:
        return os.path.lexists(path)

    def _rename(self, src: str, dst: str) -> None:
        fs.rename(src, dst)

    def _mkdtemp(self, dir: str, prefix: str, suffix: str) -> str:
        return tempfile.mkdtemp(dir=dir, prefix=prefix, suffix=suffix)

    def _rmtree_ignore_errors(self, path: str) -> None:
        shutil.rmtree(path, ignore_errors=True)


class BuildRequest(NamedTuple):
    """Plain data describing a single build to be launched: the input of a build launcher."""

    spec: spack.spec.Spec
    explicit: bool
    mirrors: List[spack.url_buildcache.MirrorMetadata]
    unsigned: Optional[bool]
    install_policy: InstallPolicy
    dirty: bool
    keep_stage: bool
    restage: bool
    keep_prefix: bool
    skip_patch: bool
    fake: bool
    install_source: bool
    run_tests: bool
    log_path: str
    stop_before: Optional[str]
    stop_at: Optional[str]


def worker_function(
    request: BuildRequest,
    state: IpcChannel,
    parent: IpcChannel,
    tee_control_r: IpcChannel,
    tee_control_w: Optional[IpcChannel],
    jobserver_info: JobserverInfo,
    global_state: GlobalStateMarshaler,
):
    """
    Function run in the build child process. Installs the requested spec, sending state updates
    and build output back to the parent process.

    Args:
        request: Description of the build to perform
        state: Connection to send state updates to
        parent: Connection to send build output to
        tee_control_r: Read end of the control pipe; the parent sends echo on/off here
        tee_control_w: Write end of the control pipe; used to stop the tee thread on POSIX
        jobserver_info: MAKEFLAGS to set, so that the build process uses the POSIX jobserver, and
            opaque data only to be serialized (e.g. old style jobserver r/w pipes, only to be
            inherited in the build process)
        global_state: Global state to restore
    """
    spec, log_path = request.spec, request.log_path

    # TODO: don't start a build for external packages
    if spec.external:
        return

    global_state.restore()

    if sys.platform != "win32":
        # Isolate the process group to shield against Ctrl+C and enable safe killpg() cleanup. In
        # constrast to setsid(), this keeps a neat process group hierarchy for utils like pstree.
        os.setpgid(0, 0)

        # Reset SIGTSTP to default in case the parent had a custom handler.
        signal.signal(signal.SIGTSTP, signal.SIG_DFL)

    def handle_sigterm(signum, frame):
        # This SIGTERM handler forwards the signal to child processes (cmake, make, etc). We wait
        # for all child processes to exit before raising KeyboardInterrupt. This ensures all
        # __exit__ and finally blocks run after the child processes have stopped, meaning that we
        # get to clean up the prefix without risking that the child process writes to it
        # afterwards.
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        if sys.platform != "win32":
            os.killpg(0, signal.SIGTERM)
            try:
                while True:
                    os.waitpid(-1, 0)
            except ChildProcessError:
                pass

        raise KeyboardInterrupt("Installation interrupted")

    signal.signal(signal.SIGTERM, handle_sigterm)

    if jobserver_info.makeflags is not None:
        os.environ["MAKEFLAGS"] = jobserver_info.makeflags

    # Save encodings before the Tee redirects fds 1/2 to the pipe. We need them to create the
    # line-buffered wrappers after the Tee starts.
    _stdout_enc = sys.stdout.encoding or "utf-8"
    _stderr_enc = sys.stderr.encoding or "utf-8"

    # Detach stdin from the terminal like `./build < /dev/null`. This would not be necessary if we
    # used os.setsid() instead of os.setpgid(), but that would "break" pstree output.
    devnull_fd = os.open(os.devnull, os.O_RDONLY)
    os.dup2(devnull_fd, 0)
    os.close(devnull_fd)
    sys.stdin = open(os.devnull, "r", encoding=sys.stdin.encoding)

    # Start the tee thread to forward output to the log file and parent process.
    tee = Tee(tee_control_r, tee_control_w, parent, log_path)

    # Use closedfd=false because of the connection objects. Use line buffering.
    # Replace sys.stdout/stderr AFTER Tee.dup2() so Python creates FileIO (WriteFile) rather
    # than ConsoleIO (WriteConsoleW). On Windows, if fds 1/2 are still console handles when
    # os.fdopen() is called, Python picks ConsoleIO; WriteConsoleW on a pipe handle returns
    # ERROR_INVALID_FUNCTION. Post-dup2 the fds are pipe handles, so FileIO is chosen.
    sys.stdout = os.fdopen(
        sys.stdout.fileno(), "w", buffering=1, encoding=_stdout_enc, closefd=False
    )
    sys.stderr = os.fdopen(
        sys.stderr.fileno(), "w", buffering=1, encoding=_stderr_enc, closefd=False
    )
    state_stream = make_state_stream(state)
    exit_code = ExitCode.SUCCESS

    try:
        with PrefixPivoter(spec.prefix, request.keep_prefix):
            _install(request, state_stream, spack.store.STORE)
    except spack.error.StopPhase:
        exit_code = ExitCode.STOPPED_AT_PHASE
    except ProcessError as e:
        print(e, file=sys.stderr)
        exit_code = ExitCode.BUILD_ERROR
    except BinaryCacheMiss:
        exit_code = ExitCode.BUILD_CACHE_MISS
    except BaseException:
        traceback.print_exc(limit=-4)
        exit_code = ExitCode.BUILD_ERROR
    finally:
        tee.close()
        state_stream.close()

    if exit_code == ExitCode.SUCCESS:
        # Try to install the compressed log file
        if not os.path.lexists(spec.package.install_log_path):
            try:
                with open(log_path, "rb") as f, open(spec.package.install_log_path, "wb") as g:
                    # Use GzipFile directly so we can omit filename / mtime in header
                    gzip_file = GzipFile(
                        filename="", mode="wb", compresslevel=6, mtime=0, fileobj=g
                    )
                    shutil.copyfileobj(f, gzip_file)
                    gzip_file.close()
            except Exception:
                pass  # don't fail the build just because log compression failed

    sys.exit(exit_code)


def _archive_build_metadata(pkg: "spack.package_base.PackageBase") -> None:
    """Copy build metadata from stage to install prefix .spack directory.

    Mirrors what the old installer's log() function does in the parent process.
    Only called after a successful source build (not for binary cache installs).
    Errors are suppressed to avoid failing the build over metadata archiving."""

    try:
        if os.path.lexists(pkg.env_mods_path):
            shutil.copy2(pkg.env_mods_path, pkg.install_env_path)
    except OSError as e:
        spack.util.tty.debug(e)
    try:
        if os.path.lexists(pkg.configure_args_path):
            shutil.copy2(pkg.configure_args_path, pkg.install_configure_args_path)
    except OSError as e:
        spack.util.tty.debug(e)

    # Archive install-phase test log if present
    try:
        pkg.archive_install_test_log()
    except Exception as e:
        spack.util.tty.debug(e)

    # Archive package-specific files matched by archive_files glob patterns
    try:
        with fs.working_dir(pkg.stage.path):
            target_dir = os.path.join(
                spack.store.STORE.layout.metadata_path(pkg.spec), "archived-files"
            )
            errors = io.StringIO()
            for glob_expr in spack.builder.create(pkg).archive_files:
                abs_expr = os.path.realpath(glob_expr)
                if os.path.realpath(pkg.stage.path) not in abs_expr:
                    errors.write(f"[OUTSIDE SOURCE PATH]: {glob_expr}\n")
                    continue
                if os.path.isabs(glob_expr):
                    glob_expr = os.path.relpath(glob_expr, pkg.stage.path)
                for f in glob.glob(glob_expr):
                    try:
                        target = os.path.join(target_dir, f)
                        fs.mkdirp(os.path.dirname(target))
                        fs.install(f, target)
                    except Exception as e:
                        spack.util.tty.debug(e)
                        errors.write(f"[FAILED TO ARCHIVE]: {f}")
            if errors.getvalue():
                error_file = os.path.join(target_dir, "errors.txt")
                fs.mkdirp(target_dir)
                with open(error_file, "w", encoding="utf-8") as err:
                    err.write(errors.getvalue())
                spack.util.tty.warn(f"Errors occurred when archiving files.\n\tSee: {error_file}")
    except Exception as e:
        spack.util.tty.debug(e)

    try:
        packages_dir = spack.store.STORE.layout.build_packages_path(pkg.spec)
        dump_packages(pkg.spec, packages_dir)
    except Exception as e:
        spack.util.tty.debug(e)

    try:
        spack.store.STORE.layout.write_host_environment(pkg.spec)
    except Exception as e:
        spack.util.tty.debug(e)


def _enable_sandbox(config: dict, spec: spack.spec.Spec, stage_path: str) -> None:
    if not config.get("enable", False):
        return

    try:
        sandbox = spack.sandbox.get_sandbox()
    except spack.sandbox.SandboxError as e:
        raise spack.error.InstallError(f"Cannot enable build sandbox: {e}") from e

    for dep in spec.traverse(root=False):
        if not dep.external:
            sandbox.allow_read(dep.prefix)

    sandbox.allow_write(stage_path)
    sandbox.allow_write(spec.prefix)

    # POSIX prescribes /tmp and /dev/null are present. In the future we can consider setting
    # TMPPATH to a sibling of the stage path to isolate concurrent builds better.
    sandbox.allow_write(tempfile.gettempdir())
    sandbox.allow_write(os.devnull)

    # Allow read access to sbang, which might be needed to run build scripts.
    sandbox.allow_read(os.path.join(spack.store.STORE.unpadded_root, "bin", "sbang"))
    for upstream_db in spack.store.STORE.upstreams or []:
        sandbox.allow_read(os.path.join(upstream_db.root, "bin", "sbang"))

    # User-configured paths
    for p in config.get("allow_read", []):
        sandbox.allow_read(p)
    for p in config.get("allow_write", []):
        sandbox.allow_write(p)

    try:
        sandbox.apply(block_network=not config.get("allow_network", True))
    except spack.sandbox.SandboxError as e:
        raise spack.error.InstallError(f"Cannot enable build sandbox: {e}") from e


def _rewire_no_db(spec: spack.spec.Spec, explicit: bool) -> None:
    """Rewire a spliced spec from its build_spec prefix, without writing to the database."""
    tmpdir = tempfile.mkdtemp()
    try:
        tarball = os.path.join(tmpdir, f"{spec.dag_hash()}.tar.gz")
        spack.binary_distribution.create_tarball(spec.build_spec, tarball)
        spack.hooks.pre_install(spec)
        spack.binary_distribution.extract_buildcache_tarball(tarball, destination=spec.prefix)
        spack.binary_distribution.relocate_package(spec)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    spack.hooks.post_install(spec, explicit)


def _install(
    request: BuildRequest, state_stream: io.TextIOWrapper, store: spack.store.Store
) -> None:
    """Install a spec from build cache or source."""
    spec, explicit, install_policy = request.spec, request.explicit, request.install_policy

    # Create the stage and log file before starting the tee thread.
    pkg = spec.package
    pkg.run_tests = request.run_tests

    if request.fake:
        store.layout.create_install_directory(spec)
        _do_fake_install(pkg)
        spack.hooks.post_install(spec, explicit)
        return

    # Try to install from buildcache, unless user asked for source only
    if install_policy != "source_only":
        if install_from_buildcache(request.mirrors, spec, request.unsigned, state_stream):
            spack.hooks.post_install(spec, explicit)
            return
        elif install_policy == "cache_only":
            send_state("no binary available", state_stream)
            raise BinaryCacheMiss(f"No binary available for {spec}")

    # Spliced spec: rewire from build_spec prefix, or trigger build_spec installation.
    if spec.build_spec is not spec:
        if install_policy == "source_only":
            send_state("rewiring", state_stream)
            _rewire_no_db(spec, explicit)
            return
        # Binary cache was the only option; signal miss for force_source expansion.
        send_state("no binary available", state_stream)
        raise BinaryCacheMiss(f"No binary available for {spec}")

    unmodified_env = os.environ.copy()
    env_mods = spack.build_environment.setup_package(pkg, dirty=request.dirty)
    store.layout.create_install_directory(spec)

    stage = pkg.stage
    stage.keep = request.keep_stage

    # Then try a source build.
    with stage:
        if request.restage:
            stage.destroy()
        stage.create()

        # Write build environment and env-mods to stage
        spack.util.environment.dump_environment(pkg.env_path)
        with open(pkg.env_mods_path, "w", encoding="utf-8") as f:
            f.write(env_mods.shell_modifications(explicit=True, env=unmodified_env))

        # Try to snapshot configure/cmake args before phases run
        for attr in ("configure_args", "cmake_args"):
            try:
                args = getattr(pkg, attr)()
                with open(pkg.configure_args_path, "w", encoding="utf-8") as f:
                    f.write(" ".join(shlex.quote(a) for a in args))
                break
            except Exception:
                pass

        # For develop packages or non-develop packages with --keep-stage there may be a
        # pre-existing symlink at pkg.log_path which would cause the new symlink to fail.
        # Try removing it if it exists.
        try:
            os.unlink(pkg.log_path)
        except OSError:
            pass
        os.symlink(request.log_path, pkg.log_path)

        send_state("staging", state_stream)

        if not request.skip_patch:
            pkg.do_patch()
        else:
            pkg.do_stage()

        os.chdir(stage.source_path)

        if request.install_source and os.path.isdir(stage.source_path):
            src_target = os.path.join(spec.prefix, "share", spec.name, "src")
            fs.install_tree(stage.source_path, src_target)

        spack.hooks.pre_install(spec)

        builder = spack.builder.create(pkg)
        stop_before, stop_at = request.stop_before, request.stop_at
        if stop_before is not None and stop_before not in builder.phases:
            raise spack.error.InstallError(f"'{stop_before}' is not a valid phase for {pkg.name}")
        if stop_at is not None and stop_at not in builder.phases:
            raise spack.error.InstallError(f"'{stop_at}' is not a valid phase for {pkg.name}")

        _enable_sandbox(spack.config.get("config:sandbox", {}), spec, stage.path)

        for phase in builder:
            if stop_before is not None and phase.name == stop_before:
                send_state(f"stopped before {stop_before}", state_stream)
                raise spack.error.StopPhase(f"Stopping before '{stop_before}'")
            send_state(phase.name, state_stream)
            spack.util.tty.msg(f"{pkg.name}: Executing phase: '{phase.name}'")
            # Run the install phase with debug output enabled.
            old_debug = spack.util.tty.debug_level()
            spack.util.tty.set_debug(1)
            try:
                phase.execute()
            finally:
                spack.util.tty.set_debug(old_debug)
            if stop_at is not None and phase.name == stop_at:
                send_state(f"stopped after {stop_at}", state_stream)
                raise spack.error.StopPhase(f"Stopping at '{stop_at}'")

        _archive_build_metadata(pkg)
        spack.hooks.post_install(spec, explicit)


def start_build(request: BuildRequest, jobserver: JobServerBase) -> ChildInfo:
    """Start a new build in a child process."""
    spec = request.spec
    channels = create_build_channels()

    # Obtain the MAKEFLAGS to be set in the child process, and determine whether it's necessary
    # for the child process to inherit our jobserver fds.
    gmake = next(iter(spec.dependencies("gmake")), None)
    jobserver_details = jobserver.makeflags_and_data(gmake)

    # As a performance optimization, we do not serialize the environment which
    # is slow to serialize and not needed in the build job
    proc = Process(
        target=worker_function,
        args=(
            request,
            channels.state_w,
            channels.output_w,
            channels.control_r,
            channels.tee_control_w,
            jobserver_details,
            GlobalStateMarshaler(serialize_env=False),
        ),
    )
    proc.start()

    # The parent process does not need the write ends of the main pipes or the read end of control.
    channels.close_child_ends()

    return ChildInfo(
        proc,
        spec,
        channels.output_r,
        channels.state_r,
        channels.control_w,
        ExitNotifier(proc),
        request.log_path,
    )


class BinaryCacheMiss(spack.error.SpackError):
    pass
