# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""New installer that will ultimately replace installer.py. It features an event loop, non-blocking
I/O, and a POSIX jobserver to limit concurrency. It also has a more advanced terminal UI. It's
mostly self-contained to avoid interfering with the rest of Spack too much while it's being
developed and tested.

The installer consists of a UI process that manages multiple build processes and handles updates
to the database. It detects or creates a jobserver, and then kicks off an event loop in which it
runs through a build queue, always running at least one build. Concurrent builds run as jobserver
tokens are obtained. This means only one -j flag is needed to control concurrency.

The UI process has two modes: an overview mode where it shows the status of all builds, and a
mode where it follows the logs of a specific build. It listens to keyboard input to switch between
modes.

The build process does an ordinary install, but also spawns a "tee" thread that forwards its build
output to both a log file and the UI process (if the UI process has requested it). This thread also
runs an event loop to listen for control messages from the UI process (to enable/disable echoing
of logs), and for output from the build process."""

import glob
import io
import json
import os
import re
import selectors
import shlex
import shutil
import signal
import sys
import tempfile
import threading
import time
import traceback
import warnings
from gzip import GzipFile
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    FrozenSet,
    Generator,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    Union,
)

from spack.vendor.typing_extensions import Literal

import spack.binary_distribution
import spack.build_environment
import spack.builder
import spack.config
import spack.database
import spack.deptypes as dt
import spack.error
import spack.hooks
import spack.llnl.util.filesystem as fs
import spack.llnl.util.tty
import spack.llnl.util.tty.color
import spack.mirrors.mirror
import spack.report
import spack.sandbox
import spack.spec
import spack.stage
import spack.store
import spack.traverse
import spack.url_buildcache
import spack.util.environment
import spack.util.lock
from spack.installer import _do_fake_install, dump_packages
from spack.llnl.util.lang import pretty_duration
from spack.new_installer_base import BaseTerminalState, StdinReaderBase
from spack.subprocess_context import GlobalStateMarshaler
from spack.util.executable import ProcessError
from spack.util.log_parse import make_log_context, parse_log_events
from spack.util.path import padding_filter, padding_filter_bytes

if sys.platform == "win32":
    from spack.new_installer_windows import WindowsTerminalState as TerminalState
else:
    import fcntl

    from spack.new_installer_posix import PosixTerminalState as TerminalState

if TYPE_CHECKING:
    import spack.package_base

#: Type for specifying installation source modes
InstallPolicy = Literal["auto", "cache_only", "source_only"]

#: How often to update a spinner in seconds
SPINNER_INTERVAL = 0.1

#: How often to wake up in headless mode to check for background->foreground transition (seconds)
HEADLESS_WAKE_INTERVAL = 1.0

#: How long to display finished packages before graying them out
CLEANUP_TIMEOUT = 2.0

#: How often to flush completed builds to the database
DATABASE_WRITE_INTERVAL = 5.0

#: Size of the output buffer for child processes
OUTPUT_BUFFER_SIZE = 32768

#: Suffix for temporary backup during overwrite install
OVERWRITE_BACKUP_SUFFIX = ".old"

#: Suffix for temporary cleanup during failed install
OVERWRITE_GARBAGE_SUFFIX = ".garbage"


class ExitCode:
    SUCCESS = 0
    BUILD_ERROR = 1
    #: Exit code used by the child process to signal that the build was stopped at a phase boundary
    STOPPED_AT_PHASE = 3
    #: Exit code used by the child process to signal a binary cache miss (no source fallback)
    BUILD_CACHE_MISS = 4


class DatabaseAction:
    """Base class for objects that need to be persisted to the database."""

    __slots__ = ("spec", "prefix_lock")

    spec: "spack.spec.Spec"
    prefix_lock: Optional[spack.util.lock.Lock]

    def save_to_db(self, db: spack.database.Database) -> None: ...

    def release_prefix_lock(self) -> None:
        if self.prefix_lock is not None:
            try:
                self.prefix_lock.release_write()
            except Exception:
                pass
        self.prefix_lock = None


class MarkExplicitAction(DatabaseAction):
    """Action to mark an already installed spec as explicitly installed. Similar to PosixChildInfo,
    but used when no build process was needed."""

    __slots__ = ()

    def __init__(self, spec: "spack.spec.Spec") -> None:
        self.spec = spec
        self.prefix_lock = None

    def save_to_db(self, db: spack.database.Database) -> None:
        db._mark(self.spec, "explicit", True)


class PosixChildInfo(DatabaseAction):
    """Information about a child process."""

    __slots__ = ("proc", "output_r_conn", "state_r_conn", "control_w_conn", "explicit", "log_path")

    def __init__(
        self,
        proc: Process,
        spec: spack.spec.Spec,
        output_r_conn: Connection,
        state_r_conn: Connection,
        control_w_conn: Connection,
        log_path: str,
        explicit: bool = False,
    ) -> None:
        self.proc = proc
        self.spec = spec
        self.output_r_conn = output_r_conn
        self.state_r_conn = state_r_conn
        self.control_w_conn = control_w_conn
        self.log_path = log_path
        self.explicit = explicit
        self.prefix_lock: Optional[spack.util.lock.Lock] = None

    def save_to_db(self, db: spack.database.Database) -> None:
        return db._add(self.spec, explicit=self.explicit)

    def close(self, selector: selectors.BaseSelector) -> int:
        """Unregister and close file descriptors, and join the child process.
        Returns the exit code of the child process."""
        try:
            selector.unregister(self.output_r_conn.fileno())
        except KeyError:
            pass
        try:
            selector.unregister(self.state_r_conn.fileno())
        except KeyError:
            pass
        try:
            selector.unregister(self.proc.sentinel)
        except (KeyError, ValueError):
            pass
        self.output_r_conn.close()
        self.state_r_conn.close()
        self.control_w_conn.close()
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


class PosixTee:
    """Emulates ./build 2>&1 | tee build.log. The output is sent both to a log file and the parent
    process (if echoing is enabled). The control_fd is used to enable/disable echoing."""

    def __init__(self, control: Connection, parent: Connection, log_path: str) -> None:
        self.control = control
        self.parent = parent
        # sys.stdout and sys.stderr may have been replaced with file objects under pytest, so
        # redirect their file descriptors in addition to the original fds 1 and 2.
        fds = {sys.stdout.fileno(), sys.stderr.fileno(), 1, 2}
        self.saved_fds = {fd: os.dup(fd) for fd in fds}
        #: The path of the log file
        self.log_path = log_path
        log_file = open(self.log_path, "ab")
        r, w = os.pipe()
        self.tee_thread = threading.Thread(target=self.run, args=(r, log_file), daemon=True)
        self.tee_thread.start()
        for fd in fds:
            os.dup2(w, fd)
        os.close(w)

    def run(self, log_r: int, log_file: io.BufferedWriter) -> None:
        """Forward log_r to log_file and parent (if echoing is enabled).
        Echoing is enabled and disabled by reading from control."""
        control_r = self.control.fileno()
        parent_w = self.parent.fileno()
        echo_on = False
        selector = selectors.DefaultSelector()
        selector.register(log_r, selectors.EVENT_READ)
        selector.register(control_r, selectors.EVENT_READ)

        try:
            with log_file, open(parent_w, "wb", closefd=False) as parent:
                while True:
                    for key, _ in selector.select():
                        if key.fd == log_r:
                            data = os.read(log_r, OUTPUT_BUFFER_SIZE)
                            if not data:  # EOF: exit the thread
                                return
                            log_file.write(data)
                            log_file.flush()
                            if echo_on:
                                parent.write(data)
                                parent.flush()

                        elif key.fd == control_r:
                            control_data = os.read(control_r, 1)
                            if not control_data:
                                return
                            else:
                                echo_on = control_data == b"1"
        except OSError:  # do not raise
            pass
        finally:
            os.close(log_r)

    def close(self) -> None:
        # Closing stdout and stderr should close the last reference to the write end of the pipe,
        # causing the tee thread to wake up, flush the last data, and exit. We restore stdout and
        # stderr, because between sys.exit and the actual process exit buffers may be flushed, and
        # can cause exit code 120 (witnessed under pytest+coverage on macOS).
        sys.stdout.flush()
        sys.stderr.flush()
        for fd, saved_fd in self.saved_fds.items():
            os.dup2(saved_fd, fd)
            os.close(saved_fd)
        self.tee_thread.join()
        # Only then close the other fds.
        self.control.close()
        self.parent.close()


def install_from_buildcache(
    mirrors: List[spack.url_buildcache.MirrorMetadata],
    spec: spack.spec.Spec,
    unsigned: Optional[bool],
    state_stream: io.TextIOWrapper,
) -> bool:
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
        os.rename(src, dst)

    def _mkdtemp(self, dir: str, prefix: str, suffix: str) -> str:
        return tempfile.mkdtemp(dir=dir, prefix=prefix, suffix=suffix)

    def _rmtree_ignore_errors(self, path: str) -> None:
        shutil.rmtree(path, ignore_errors=True)


def worker_function(
    spec: spack.spec.Spec,
    explicit: bool,
    mirrors: List[spack.url_buildcache.MirrorMetadata],
    unsigned: Optional[bool],
    install_policy: InstallPolicy,
    dirty: bool,
    keep_stage: bool,
    restage: bool,
    keep_prefix: bool,
    skip_patch: bool,
    fake: bool,
    install_source: bool,
    run_tests: bool,
    state: Connection,
    parent: Connection,
    echo_control: Connection,
    makeflags: str,
    js1: Optional[Connection],
    js2: Optional[Connection],
    log_path: str,
    global_state: GlobalStateMarshaler,
    stop_before: Optional[str] = None,
    stop_at: Optional[str] = None,
):
    """
    Function run in the build child process. Installs the specified spec, sending state updates
    and build output back to the parent process.

    Args:
        spec: Spec to install
        explicit: Whether the spec was explicitly requested by the user
        mirrors: List of buildcache mirrors to try
        unsigned: Whether to allow unsigned buildcache entries
        install_policy: ``"auto"``, ``"cache_only"``, or ``"source_only"``
        dirty: Whether to preserve user environment in the build environment
        keep_stage: Whether to keep the build stage after installation
        restage: Whether to restage the source before building
        keep_prefix: Whether to keep a failed installation prefix
        skip_patch: Whether to skip the patch phase
        run_tests: Whether to run install-time tests for this package
        state: Connection to send state updates to
        parent: Connection to send build output to
        echo_control: Connection to receive echo control messages from
        makeflags: MAKEFLAGS to set, so that the build process uses the POSIX jobserver
        js1: Connection for old style jobserver read fd (if any). Unused, just to inherit fd.
        js2: Connection for old style jobserver write fd (if any). Unused, just to inherit fd.
        log_path: Path to the log file to write build output to
        global_state: Global state to restore
    """

    # TODO: don't start a build for external packages
    if spec.external:
        return

    global_state.restore()

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
        os.killpg(0, signal.SIGTERM)

        try:
            while True:
                os.waitpid(-1, 0)
        except ChildProcessError:
            pass

        raise KeyboardInterrupt("Installation interrupted")

    signal.signal(signal.SIGTERM, handle_sigterm)

    os.environ["MAKEFLAGS"] = makeflags

    # Force line buffering for Python's textio wrappers of stdout/stderr. We're not going to print
    # much ourselves, but what we print should appear before output from `make` and other build
    # tools.
    sys.stdout = os.fdopen(
        sys.stdout.fileno(), "w", buffering=1, encoding=sys.stdout.encoding, closefd=False
    )
    sys.stderr = os.fdopen(
        sys.stderr.fileno(), "w", buffering=1, encoding=sys.stderr.encoding, closefd=False
    )

    # Detach stdin from the terminal like `./build < /dev/null`. This would not be necessary if we
    # used os.setsid() instead of os.setpgid(), but that would "break" pstree output.
    devnull_fd = os.open(os.devnull, os.O_RDONLY)
    os.dup2(devnull_fd, 0)
    os.close(devnull_fd)
    sys.stdin = open(os.devnull, "r", encoding=sys.stdin.encoding)

    # Start the tee thread to forward output to the log file and parent process.
    tee = PosixTee(echo_control, parent, log_path)

    # Use closedfd=false because of the connection objects. Use line buffering.
    state_stream = os.fdopen(state.fileno(), "w", buffering=1, closefd=False)
    exit_code = ExitCode.SUCCESS

    try:
        with PrefixPivoter(spec.prefix, keep_prefix):
            _install(
                spec,
                explicit,
                mirrors,
                unsigned,
                install_policy,
                dirty,
                keep_stage,
                restage,
                skip_patch,
                fake,
                install_source,
                state_stream,
                log_path,
                spack.store.STORE,
                run_tests,
                stop_before,
                stop_at,
            )
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
        spack.llnl.util.tty.debug(e)
    try:
        if os.path.lexists(pkg.configure_args_path):
            shutil.copy2(pkg.configure_args_path, pkg.install_configure_args_path)
    except OSError as e:
        spack.llnl.util.tty.debug(e)

    # Archive install-phase test log if present
    try:
        pkg.archive_install_test_log()
    except Exception as e:
        spack.llnl.util.tty.debug(e)

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
                        spack.llnl.util.tty.debug(e)
                        errors.write(f"[FAILED TO ARCHIVE]: {f}")
            if errors.getvalue():
                error_file = os.path.join(target_dir, "errors.txt")
                fs.mkdirp(target_dir)
                with open(error_file, "w", encoding="utf-8") as err:
                    err.write(errors.getvalue())
                spack.llnl.util.tty.warn(
                    f"Errors occurred when archiving files.\n\tSee: {error_file}"
                )
    except Exception as e:
        spack.llnl.util.tty.debug(e)

    try:
        packages_dir = spack.store.STORE.layout.build_packages_path(pkg.spec)
        dump_packages(pkg.spec, packages_dir)
    except Exception as e:
        spack.llnl.util.tty.debug(e)

    try:
        spack.store.STORE.layout.write_host_environment(pkg.spec)
    except Exception as e:
        spack.llnl.util.tty.debug(e)


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
    spec: spack.spec.Spec,
    explicit: bool,
    mirrors: List[spack.url_buildcache.MirrorMetadata],
    unsigned: Optional[bool],
    install_policy: InstallPolicy,
    dirty: bool,
    keep_stage: bool,
    restage: bool,
    skip_patch: bool,
    fake: bool,
    install_source: bool,
    state_stream: io.TextIOWrapper,
    log_path: str,
    store: spack.store.Store = spack.store.STORE,
    run_tests: bool = False,
    stop_before: Optional[str] = None,
    stop_at: Optional[str] = None,
) -> None:
    """Install a spec from build cache or source."""

    # Create the stage and log file before starting the tee thread.
    pkg = spec.package
    pkg.run_tests = run_tests

    if fake:
        store.layout.create_install_directory(spec)
        _do_fake_install(pkg)
        spack.hooks.post_install(spec, explicit)
        return

    # Try to install from buildcache, unless user asked for source only
    if install_policy != "source_only":
        if install_from_buildcache(mirrors, spec, unsigned, state_stream):
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
    env_mods = spack.build_environment.setup_package(pkg, dirty=dirty)
    store.layout.create_install_directory(spec)

    stage = pkg.stage
    stage.keep = keep_stage

    # Then try a source build.
    with stage:
        if restage:
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
        os.symlink(log_path, pkg.log_path)

        send_state("staging", state_stream)

        if not skip_patch:
            pkg.do_patch()
        else:
            pkg.do_stage()

        os.chdir(stage.source_path)

        if install_source and os.path.isdir(stage.source_path):
            src_target = os.path.join(spec.prefix, "share", spec.name, "src")
            fs.install_tree(stage.source_path, src_target)

        spack.hooks.pre_install(spec)

        builder = spack.builder.create(pkg)
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
            spack.llnl.util.tty.msg(f"{pkg.name}: Executing phase: '{phase.name}'")
            # Run the install phase with debug output enabled.
            old_debug = spack.llnl.util.tty.debug_level()
            spack.llnl.util.tty.set_debug(1)
            try:
                phase.execute()
            finally:
                spack.llnl.util.tty.set_debug(old_debug)
            if stop_at is not None and phase.name == stop_at:
                send_state(f"stopped after {stop_at}", state_stream)
                raise spack.error.StopPhase(f"Stopping at '{stop_at}'")

        _archive_build_metadata(pkg)
        spack.hooks.post_install(spec, explicit)


class PosixJobServer:
    """Attach to an existing POSIX jobserver or create a FIFO-based one."""

    def __init__(self, num_jobs: int) -> None:
        #: Keep track of how many tokens Spack itself has acquired, which is used to release them.
        self.tokens_acquired = 0
        #: The number of jobs to run concurrently. This translates to `num_jobs - 1` tokens in the
        #: jobserver.
        self.num_jobs = num_jobs
        #: The target number of jobs to run concurrently, which may differ from num_jobs if the
        #: user has requested a decrease in parallelism, but we haven't consumed enough tokens to
        #: reflect that yet. This value is used in the UI. The invariant is that self.target_jobs
        #: can only be modified if self.created is True.
        self.target_jobs = num_jobs
        self.fifo_path: Optional[str] = None
        self.created = False
        self._setup()
        # Ensure that Executable()(...) in build processes ultimately inherit jobserver fds.
        os.set_inheritable(self.r, True)
        os.set_inheritable(self.w, True)
        # r_conn and w_conn are used to make build processes inherit the jobserver fds if needed.
        # Connection objects close the fd as they are garbage collected, so store them.
        self.r_conn = Connection(self.r)
        self.w_conn = Connection(self.w)

    def _setup(self) -> None:

        fifo_config = get_jobserver_config()

        if type(fifo_config) is str:
            # FIFO-based jobserver. Try to open the FIFO.
            open_attempt = open_existing_jobserver_fifo(fifo_config)
            if open_attempt:
                self.r, self.w = open_attempt
                self.fifo_path = fifo_config
                return
        elif type(fifo_config) is tuple:
            # Old style pipe-based jobserver. Validate the fds before using them.
            r, w = fifo_config
            if fcntl.fcntl(r, fcntl.F_GETFD) != -1 and fcntl.fcntl(w, fcntl.F_GETFD) != -1:
                self.r, self.w = r, w
                return

        # No existing jobserver we can connect to: create a FIFO-based one.
        self.r, self.w, self.fifo_path = create_jobserver_fifo(self.num_jobs)
        self.created = True

    def makeflags(self, gmake: Optional[spack.spec.Spec]) -> str:
        """Return the MAKEFLAGS for a build process, depending on its gmake build dependency."""
        if self.fifo_path and (not gmake or gmake.satisfies("@4.4:")):
            return f" -j{self.num_jobs} --jobserver-auth=fifo:{self.fifo_path}"
        elif not gmake or gmake.satisfies("@4.0:"):
            return f" -j{self.num_jobs} --jobserver-auth={self.r},{self.w}"
        else:
            return f" -j{self.num_jobs} --jobserver-fds={self.r},{self.w}"

    def has_target_parallelism(self) -> bool:
        return self.num_jobs == self.target_jobs

    def increase_parallelism(self) -> None:
        """Add one token to the jobserver to increase parallelism; this should always work."""
        if not self.created:
            return
        self.target_jobs += 1
        # If a decrease was pending, don't add a token.
        if self.target_jobs <= self.num_jobs:
            return
        os.write(self.w, b"+")
        self.num_jobs += 1

    def decrease_parallelism(self) -> None:
        """Request an eventual concurrency decrease by 1."""
        if not self.created or self.target_jobs <= 1:
            return
        self.target_jobs -= 1
        self.maybe_discard_tokens()

    def maybe_discard_tokens(self) -> None:
        """Try to get reduce parallelism by discarding tokens."""
        to_discard = self.num_jobs - self.target_jobs
        if to_discard <= 0:
            return
        try:
            # The read may return zero or just fewer bytes than requested; we'll try again later.
            self.num_jobs -= len(os.read(self.r, to_discard))
        except BlockingIOError:
            pass

    def acquire(self, jobs: int) -> int:
        """Try and acquire at most 'jobs' tokens from the jobserver. Returns the number of
        tokens actually acquired (may be less than requested, or zero)."""
        try:
            num_acquired = len(os.read(self.r, jobs))
            self.tokens_acquired += num_acquired
            return num_acquired
        except BlockingIOError:
            return 0

    def release(self) -> None:
        """Release a token back to the jobserver."""
        # The last job to quit has an implicit token, so don't release if we have none.
        if self.tokens_acquired == 0:
            return
        self.tokens_acquired -= 1
        if self.target_jobs < self.num_jobs:
            # If a decrease in parallelism is requested, discard a token instead of releasing it.
            self.num_jobs -= 1
        else:
            os.write(self.w, b"+")

    def close(self) -> None:
        if self.created and self.num_jobs > 1:
            if self.tokens_acquired != 0:
                # It's a non-fatal internal error to close the jobserver with acquired tokens.
                warnings.warn("Spack failed to release jobserver tokens", stacklevel=2)
            else:
                # Verify that all build processes released the tokens they acquired.
                total = self.num_jobs - 1
                drained = self.acquire(total)
                if drained != total:
                    n = total - drained
                    warnings.warn(
                        f"{n} jobserver {'token was' if n == 1 else 'tokens were'} not released "
                        "by the build processes. This can indicate that the build ran with "
                        "limited parallelism.",
                        stacklevel=2,
                    )

        self.r_conn.close()
        self.w_conn.close()

        # Remove the FIFO if we created it.
        if self.created and self.fifo_path:
            try:
                os.unlink(self.fifo_path)
            except OSError:
                pass
            try:
                os.rmdir(os.path.dirname(self.fifo_path))
            except OSError:
                pass


def start_build(
    spec: spack.spec.Spec,
    explicit: bool,
    mirrors: List[spack.url_buildcache.MirrorMetadata],
    unsigned: Optional[bool],
    install_policy: InstallPolicy,
    dirty: bool,
    keep_stage: bool,
    restage: bool,
    keep_prefix: bool,
    skip_patch: bool,
    fake: bool,
    install_source: bool,
    run_tests: bool,
    jobserver: PosixJobServer,
    log_path: str,
    stop_before: Optional[str] = None,
    stop_at: Optional[str] = None,
) -> PosixChildInfo:
    """Start a new build."""
    # Create pipes for the child's output, state reporting, and control.
    state_r_conn, state_w_conn = Pipe(duplex=False)
    output_r_conn, output_w_conn = Pipe(duplex=False)
    control_r_conn, control_w_conn = Pipe(duplex=False)

    # Obtain the MAKEFLAGS to be set in the child process, and determine whether it's necessary
    # for the child process to inherit our jobserver fds.
    gmake = next(iter(spec.dependencies("gmake")), None)
    makeflags = jobserver.makeflags(gmake)
    fifo = "--jobserver-auth=fifo:" in makeflags

    # As a performance optimization, we do not serialize the environment which
    # is slow to serialize and not needed in the build job
    proc = Process(
        target=worker_function,
        args=(
            spec,
            explicit,
            mirrors,
            unsigned,
            install_policy,
            dirty,
            keep_stage,
            restage,
            keep_prefix,
            skip_patch,
            fake,
            install_source,
            run_tests,
            state_w_conn,
            output_w_conn,
            control_r_conn,
            makeflags,
            None if fifo else jobserver.r_conn,
            None if fifo else jobserver.w_conn,
            log_path,
            GlobalStateMarshaler(serialize_env=False),
            stop_before,
            stop_at,
        ),
    )
    proc.start()

    # The parent process does not need the write ends of the main pipes or the read end of control.
    state_w_conn.close()
    output_w_conn.close()
    control_r_conn.close()

    # Set the read ends to non-blocking: in principle redundant with epoll/kqueue, but safer.
    os.set_blocking(output_r_conn.fileno(), False)
    os.set_blocking(state_r_conn.fileno(), False)

    return PosixChildInfo(
        proc, spec, output_r_conn, state_r_conn, control_w_conn, log_path, explicit
    )


def get_jobserver_config(makeflags: Optional[str] = None) -> Optional[Union[str, Tuple[int, int]]]:
    """Parse MAKEFLAGS for jobserver. Either it's a FIFO or (r, w) pair of file descriptors.

    Args:
        makeflags: MAKEFLAGS string to parse. If None, reads from os.environ.
    """
    makeflags = os.environ.get("MAKEFLAGS", "") if makeflags is None else makeflags
    if not makeflags:
        return None
    # We can have the following flags:
    # --jobserver-fds=R,W (before GNU make 4.2)
    # --jobserver-auth=fifo:PATH or --jobserver-auth=R,W (after GNU make 4.2)
    # In case of multiple, the last one wins.
    matches = re.findall(r" --jobserver-[^=]+=([^ ]+)", makeflags)
    if not matches:
        return None
    last_match: str = matches[-1]
    assert isinstance(last_match, str)
    if last_match.startswith("fifo:"):
        return last_match[5:]
    parts = last_match.split(",", 1)
    if len(parts) != 2:
        return None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None


def create_jobserver_fifo(num_jobs: int) -> Tuple[int, int, str]:
    """Create a new jobserver FIFO with the specified number of job tokens."""
    tmpdir = tempfile.mkdtemp()
    fifo_path = os.path.join(tmpdir, "jobserver_fifo")

    try:
        os.mkfifo(fifo_path, 0o600)
        read_fd = os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK)
        write_fd = os.open(fifo_path, os.O_WRONLY)
        # write num_jobs - 1 tokens, because the first job is implicit
        os.write(write_fd, b"+" * (num_jobs - 1))
        return read_fd, write_fd, fifo_path
    except Exception:
        try:
            os.unlink(fifo_path)
        except OSError as e:
            spack.llnl.util.tty.debug(f"Failed to remove POSIX jobserver FIFO: {e}", level=3)
            pass
        try:
            os.rmdir(tmpdir)
        except OSError as e:
            spack.llnl.util.tty.debug(f"Failed to remove POSIX jobserver FIFO dir: {e}", level=3)
            pass
        raise


def open_existing_jobserver_fifo(fifo_path: str) -> Optional[Tuple[int, int]]:
    """Open an existing jobserver FIFO for reading and writing."""
    try:
        read_fd = os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK)
        write_fd = os.open(fifo_path, os.O_WRONLY)
        return read_fd, write_fd
    except OSError:
        return None


class FdInfo:
    """Information about a file descriptor mapping."""

    __slots__ = ("pid", "name")

    def __init__(self, pid: int, name: str) -> None:
        self.pid = pid
        self.name = name


class BuildInfo:
    """Information about a package being built."""

    __slots__ = (
        "state",
        "explicit",
        "version",
        "hash",
        "name",
        "external",
        "prefix",
        "finished_time",
        "start_time",
        "duration",
        "progress_percent",
        "control_w_conn",
        "log_path",
        "log_summary",
    )

    def __init__(
        self,
        spec: spack.spec.Spec,
        explicit: bool,
        control_w_conn: Optional[Connection],
        log_path: Optional[str] = None,
        start_time: float = 0.0,
    ) -> None:
        self.state: str = "starting"
        self.explicit: bool = explicit
        self.version: str = str(spec.version)
        self.hash: str = spec.dag_hash(7)
        self.name: str = spec.name
        self.external: bool = spec.external
        self.prefix: str = spec.prefix
        self.finished_time: Optional[float] = None
        self.start_time: float = start_time
        self.duration: Optional[float] = None
        self.progress_percent: Optional[int] = None
        self.control_w_conn = control_w_conn
        self.log_path = log_path
        self.log_summary: Optional[str] = None


class BuildStatus:
    """Tracks the build status display for terminal output."""

    def __init__(
        self,
        total: int,
        stdout: io.TextIOWrapper = sys.stdout,  # type: ignore[assignment]
        get_terminal_size: Callable[[], os.terminal_size] = os.get_terminal_size,
        get_time: Callable[[], float] = time.monotonic,
        is_tty: Optional[bool] = None,
        color: Optional[bool] = None,
        verbose: bool = False,
        filter_padding: bool = False,
    ) -> None:
        #: Ordered dict of build ID -> info
        self.total = total
        self.completed = 0
        self.builds: Dict[str, BuildInfo] = {}
        self.finished_builds: List[BuildInfo] = []
        self.spinner_chars = ["|", "/", "-", "\\"]
        self.spinner_index = 0
        self.dirty = True  # Start dirty to draw initial state
        self.active_area_rows = 0
        self.total_lines = 0
        self.next_spinner_update = 0.0
        self.next_update = 0.0
        self.overview_mode = True  # Whether to draw the package overview
        self.tracked_build_id = ""  # identifier of the package whose logs we follow
        self.search_term = ""
        self.search_mode = False
        self.log_ends_with_newline = True
        self.actual_jobs: int = 0
        self.target_jobs: int = 0
        self.blocked: bool = False

        self.stdout = stdout
        self.get_terminal_size = get_terminal_size
        self.terminal_size = os.terminal_size((0, 0))
        self.terminal_size_changed: bool = True
        self.get_time = get_time
        self.is_tty = is_tty if is_tty is not None else stdout.isatty()
        if color is not None:
            self.color = color
        else:
            self.color = spack.llnl.util.tty.color.get_color_when(stdout)
        #: Verbose mode only applies to non-TTY where we want to track a single build log.
        self.verbose = verbose and not self.is_tty
        self.filter_padding = filter_padding
        #: When True, suppress all terminal output (process is in background).
        #: Controlling code is responsible for modifying this variable based on process state
        self.headless = False
        self.term_title = spack.config.get("config:install_status", True) and self.is_tty

    def on_resize(self) -> None:
        """Refresh cached terminal size and trigger a redraw."""
        self.terminal_size_changed = True
        self.dirty = True

    def add_build(
        self,
        spec: spack.spec.Spec,
        explicit: bool,
        control_w_conn: Optional[Connection] = None,
        log_path: Optional[str] = None,
    ) -> None:
        """Add a new build to the display and mark the display as dirty."""
        build_info = BuildInfo(spec, explicit, control_w_conn, log_path, int(self.get_time()))
        self.builds[spec.dag_hash()] = build_info
        self.dirty = True
        # Track the new build's logs when we're not already following another build. This applies
        # only in non-TTY verbose mode.
        if self.verbose and not self.tracked_build_id and control_w_conn is not None:
            self.tracked_build_id = spec.dag_hash()
            try:
                os.write(control_w_conn.fileno(), b"1")
            except OSError:
                pass

    def remove_build(self, build_id: str) -> None:
        """Remove a build from the display (e.g. after a binary cache miss before retry)."""
        self.builds.pop(build_id, None)
        if self.tracked_build_id == build_id:
            self.tracked_build_id = ""
            if not self.overview_mode:
                self.overview_mode = True
        self.dirty = True

    def toggle(self) -> None:
        """Toggle between overview mode and following a specific build."""
        if self.overview_mode:
            self.next()
        else:
            if not self.log_ends_with_newline:
                self.stdout.buffer.write(b"\n")
                self.log_ends_with_newline = True
            self.active_area_rows = 0
            self.search_term = ""
            self.search_mode = False
            self.overview_mode = True
            self.dirty = True
            try:
                conn = self.builds[self.tracked_build_id].control_w_conn
                if conn is not None:
                    os.write(conn.fileno(), b"0")
            except (KeyError, OSError):
                pass
            self.tracked_build_id = ""

    def search_input(self, input: str) -> None:
        """Handle keyboard input when in search mode"""
        if input in ("\r", "\n"):
            self.log_ends_with_newline = False
            self.next(1)
        elif input == "\x1b":  # Escape
            self.search_mode = False
            self.search_term = ""
            self.dirty = True
        elif input in ("\x7f", "\b"):  # Backspace
            self.search_term = self.search_term[:-1]
            self.dirty = True
        elif input.isprintable():
            self.search_term += input
            self.dirty = True

    def enter_search(self) -> None:
        self.search_mode = True
        self.dirty = True

    def _is_displayed(self, build: BuildInfo) -> bool:
        """Returns true if the build matches the search term, or when no search term is set."""
        # When not in search mode, the search_term is "", which always evaluates to True below
        return self.search_term in build.name or build.hash.startswith(self.search_term)

    def _get_next(self, direction: int) -> Optional[str]:
        """Returns the next or previous unfinished build ID matching the search term, or None if
        none found. Direction should be 1 for next, -1 for previous."""
        matching = [
            build_id
            for build_id, build in self.builds.items()
            if (build.finished_time is None or build.state == "failed")
            and self._is_displayed(build)
        ]
        if not matching:
            return None
        try:
            idx = matching.index(self.tracked_build_id)
        except ValueError:
            return matching[0] if direction == 1 else matching[-1]

        return matching[(idx + direction) % len(matching)]

    def next(self, direction: int = 1) -> None:
        """Follow the logs of the next build in the list."""
        new_build_id = self._get_next(direction)

        if not new_build_id or self.tracked_build_id == new_build_id:
            return

        new_build = self.builds[new_build_id]

        if self.overview_mode:
            self.overview_mode = False

        # Stop following the previous and start following the new build.
        if self.tracked_build_id:
            try:
                conn = self.builds[self.tracked_build_id].control_w_conn
                if conn is not None:
                    os.write(conn.fileno(), b"0")
            except (KeyError, OSError):
                pass

        self.tracked_build_id = new_build_id

        version_str = (
            f"\033[0;36m@{new_build.version}\033[0m" if self.color else f"@{new_build.version}"
        )
        prefix = "" if self.log_ends_with_newline else "\n"

        if new_build.state == "failed":
            # For failed builds, show the stored log summary instead of following live logs.
            self.stdout.write(f"{prefix}==> Log summary of {new_build.name}{version_str}\n")
            self.log_ends_with_newline = True
            if new_build.log_summary:
                self.stdout.write(new_build.log_summary)
            if new_build.log_path:
                if not new_build.log_summary:
                    self.stdout.write("No errors parsed from log, see full log: ")
                else:
                    self.stdout.write("Full log: ")
                self.stdout.write(f"{new_build.log_path}\n")
            self.stdout.flush()
        else:
            # Tell the user we're following new logs, and instruct the child to start sending.
            self.stdout.write(f"{prefix}==> Following logs of {new_build.name}{version_str}\n")
            self.log_ends_with_newline = True
            self.stdout.flush()
            try:
                conn = new_build.control_w_conn
                if conn is not None:
                    os.write(conn.fileno(), b"1")
            except (KeyError, OSError):
                pass

    def set_blocked(self, blocked: bool) -> None:
        """Set whether all pending builds are blocked by another Spack process."""
        if blocked == self.blocked:
            return
        self.blocked = blocked
        self.dirty = True

    def _update_terminal_title(self, clear: bool = False) -> None:
        if not self.term_title:
            return

        term_title = ""

        if not clear:
            term_title = f"Spack: {self.completed}/{self.total} - {self.actual_jobs} jobs"

        self.stdout.write(f"\x1b]0;{term_title}\x07")
        self.stdout.flush()

    def set_jobs(self, actual: int, target: int) -> None:
        """Set the actual and target number of jobs to run concurrently."""
        if actual == self.actual_jobs and target == self.target_jobs:
            return
        self.actual_jobs = actual
        self.target_jobs = target
        self.dirty = True
        self._update_terminal_title()

    def update_state(self, build_id: str, state: str) -> None:
        """Update the state of a package and mark the display as dirty."""
        build_info = self.builds[build_id]
        build_info.state = state
        build_info.progress_percent = None

        if state in ("finished", "failed"):
            self.completed += 1
            now = self.get_time()
            build_info.duration = now - build_info.start_time
            build_info.finished_time = now + CLEANUP_TIMEOUT

            # Stop tracking the finished build's logs.
            if build_id == self.tracked_build_id:
                if not self.overview_mode:
                    self.toggle()
                if self.verbose:
                    self.tracked_build_id = ""

        self.dirty = True
        self._update_terminal_title()

        # For non-TTY output, print state changes immediately
        if not self.is_tty and not self.headless:
            line = "".join(
                self._generate_line_components(build_info, static=True, now=self.get_time())
            )
            self.stdout.write(line + "\n")
            self.stdout.flush()

    def parse_log_summary(self, build_id: str) -> None:
        """Parse the build log for errors/warnings and store the summary."""
        build_info = self.builds[build_id]
        if not build_info.log_path or not os.path.exists(build_info.log_path):
            return
        errors, warnings, tail_event = parse_log_events(build_info.log_path, tail=20)
        events = [*errors, *warnings]
        if tail_event is not None:
            events.append(tail_event)
        if events:
            build_info.log_summary = make_log_context(events)

    def update_progress(self, build_id: str, current: int, total: int) -> None:
        """Update the progress of a package and mark the display as dirty."""
        percent = int((current / total) * 100)
        build_info = self.builds[build_id]
        if build_info.progress_percent != percent:
            build_info.progress_percent = percent
            self.dirty = True

    def update(self, finalize: bool = False) -> None:
        """Redraw the interactive display."""
        if self.headless or not self.is_tty or not self.overview_mode:
            return

        now = self.get_time()

        # Avoid excessive redraws
        if not finalize and now < self.next_update:
            return

        # Only update the spinner if there are still running packages
        if now >= self.next_spinner_update and any(
            pkg.finished_time is None for pkg in self.builds.values()
        ):
            self.spinner_index = (self.spinner_index + 1) % len(self.spinner_chars)
            self.dirty = True
            self.next_spinner_update = now + SPINNER_INTERVAL

        for build_id in list(self.builds):
            build_info = self.builds[build_id]
            if build_info.state == "failed" or build_info.finished_time is None:
                continue

            if finalize or now >= build_info.finished_time:
                self.finished_builds.append(build_info)
                del self.builds[build_id]
                self.dirty = True

        if not self.dirty and not finalize:
            return

        # Build the overview output in a buffer and print all at once to avoid flickering.
        buffer = io.StringIO()

        # Move cursor up to the start of the display area assuming the same terminal width. If the
        # terminal resized, lines may have wrapped, and we should've moved up further. We do not
        # try to track that (would require keeping track of each line's width).
        if self.active_area_rows > 0:
            buffer.write(f"\033[{self.active_area_rows}A\r")

        if self.terminal_size_changed:
            self.terminal_size = self.get_terminal_size()
            self.terminal_size_changed = False
            # After resize, active_area_rows is invalidated due to possible line wrapping. Set to
            # 0 to force newlines instead of cursor movement.
            self.active_area_rows = 0
        max_width, max_height = self.terminal_size

        # First flush the finished builds. These are "persisted" in terminal history.
        if self.finished_builds:
            for build in self.finished_builds:
                self._render_build(build, buffer, now=now)
                self._println(buffer, force_newline=True)  # should scroll the terminal
            self.finished_builds.clear()
            # Finished builds can span multiple lines, overlapping our "active area", invalidating
            # active_area_rows. Set to 0 to force newlines instead of cursor movement.
            self.active_area_rows = 0

        # Then a header followed by the active builds. This is the "mutable" part of the display.
        self.total_lines = 0

        if not finalize:
            if self.color:
                bold = "\033[1m"
                reset = "\033[0m"
                cyan = "\033[36m"
            else:
                bold = reset = cyan = ""

            if self.actual_jobs != self.target_jobs:
                jobs_str = f"{self.actual_jobs}=>{self.target_jobs}"
            else:
                jobs_str = str(self.target_jobs)
            long_header_len = len(
                f"Progress: {self.completed}/{self.total}  +/-: {jobs_str} jobs"
                "  /: filter  v: logs  n/p: next/prev"
            )
            if long_header_len < max_width:
                self._println(
                    buffer,
                    f"{bold}Progress:{reset} {self.completed}/{self.total}"
                    f"  {cyan}+{reset}/{cyan}-{reset}: "
                    f"{jobs_str} jobs"
                    f"  {cyan}/{reset}: filter  {cyan}v{reset}: logs"
                    f"  {cyan}n{reset}/{cyan}p{reset}: next/prev",
                )
            else:
                self._println(buffer, f"{bold}Progress:{reset} {self.completed}/{self.total}")

        if self.blocked and not any(pkg.finished_time is None for pkg in self.builds.values()):
            self._println(buffer, "Waiting for other Spack install process...")

        displayed_builds = (
            [b for b in self.builds.values() if self._is_displayed(b)]
            if self.search_term
            else self.builds.values()
        )
        len_builds = len(displayed_builds)

        # Truncate if we have more builds than fit on the screen. In that case we have to reserve
        # an additional line for the "N more..." message.
        truncate_at = max_height - 3 if len_builds + 2 > max_height else len_builds

        for i, build in enumerate(displayed_builds, 1):
            if i > truncate_at:
                self._println(buffer, f"{len_builds - i + 1} more...")
                break
            self._render_build(build, buffer, max_width, now=now)
            self._println(buffer)

        if self.search_mode:
            buffer.write(f"filter> {self.search_term}\033[K")

        # Clear any remaining lines from previous display
        buffer.write("\033[0J")

        # Print everything at once to avoid flickering
        self.stdout.write(buffer.getvalue())
        self.stdout.flush()

        # Update the number of lines drawn for next time. It reflects the number of active builds.
        self.active_area_rows = self.total_lines
        self.dirty = False

        # Schedule next UI update
        self.next_update = now + SPINNER_INTERVAL / 2

        if finalize:
            self._update_terminal_title(True)

    def _println(self, buffer: io.StringIO, line: str = "", force_newline: bool = False) -> None:
        """Print a line to the buffer, handling line clearing and cursor movement."""
        self.total_lines += 1
        if line:
            buffer.write(line)
        if self.total_lines > self.active_area_rows or force_newline:
            buffer.write("\033[0m\033[K\n")  # reset, clear to EOL, newline
        else:
            buffer.write("\033[0m\033[K\033[1B\r")  # reset, clear to EOL, move to next line

    def print_logs(self, build_id: str, data: bytes) -> None:
        if self.headless:
            return
        # Discard logs we are not following. Generally this should not happen as we tell the child
        # to only send logs when we are following it. It could maybe happen while transitioning
        # between builds.
        if build_id != self.tracked_build_id:
            return
        if self.filter_padding:
            data = padding_filter_bytes(data)
        self.stdout.buffer.write(data)
        self.stdout.flush()
        self.log_ends_with_newline = data.endswith(b"\n")

    def _render_build(
        self, build_info: BuildInfo, buffer: io.StringIO, max_width: int = 0, now: float = 0.0
    ) -> None:
        """Print a single build line to the buffer, truncating to max_width (if > 0)."""
        line_width = 0
        for component in self._generate_line_components(build_info, now=now):
            # ANSI escape sequence(s), does not contribute to width
            if not component.startswith("\033") and max_width > 0:
                line_width += len(component)
                if line_width > max_width:
                    break
            buffer.write(component)

    def _generate_line_components(
        self, build_info: BuildInfo, static: bool = False, now: float = 0.0
    ) -> Generator[str, None, None]:
        """Yield formatted line components for a package. Escape sequences are yielded as separate
        strings so they do not contribute to the line width."""
        if build_info.external:
            indicator = "[e]"
        elif build_info.state == "finished":
            indicator = "[+]"
        elif build_info.state == "failed":
            indicator = "[x]"
        elif static:
            indicator = "[ ]"
        else:
            indicator = f"[{self.spinner_chars[self.spinner_index]}]"

        if self.color:
            if build_info.state == "failed":
                yield "\033[31m"  # red
            elif build_info.state == "finished":
                yield "\033[32m"  # green

        yield indicator
        if self.color:
            yield "\033[0m"  # reset
        yield " "
        if self.color:
            yield "\033[0;90m"  # dark gray
        yield build_info.hash
        if self.color:
            yield "\033[0m"  # reset
        yield " "

        # Package name in bold if explicit, default otherwise
        if build_info.explicit:
            if self.color:
                yield "\033[1m"
            yield build_info.name
            if self.color:
                yield "\033[0m"  # reset
        else:
            yield build_info.name

        if self.color:
            yield "\033[0;36m"  # cyan
        yield f"@{build_info.version}"
        if self.color:
            yield "\033[0m"  # reset

        # progress or state
        if build_info.progress_percent is not None:
            yield " fetching"
            yield f": {build_info.progress_percent}%"
        elif build_info.state == "finished":
            prefix = build_info.prefix
            yield f" {padding_filter(prefix) if self.filter_padding else prefix}"
        elif build_info.state == "failed":
            yield " failed"
            if build_info.log_path:
                yield f": {build_info.log_path}"
        else:
            yield f" {build_info.state}"

        # Duration
        elapsed = (
            build_info.duration
            if build_info.duration is not None
            else (now - build_info.start_time)
        )
        if elapsed > 0:
            if self.color:
                yield "\033[0;90m"  # dark gray
            yield f" ({pretty_duration(elapsed)})"
            if self.color:
                yield "\033[0m"


Nodes = Dict[str, spack.spec.Spec]
Edges = Dict[str, Set[str]]


class BuildGraph:
    """Represents the dependency graph for package installation."""

    def __init__(
        self,
        specs: List[spack.spec.Spec],
        root_policy: InstallPolicy,
        dependencies_policy: InstallPolicy,
        include_build_deps: bool,
        install_package: bool,
        install_deps: bool,
        database: spack.database.Database,
        overwrite_set: Optional[Set[str]] = None,
        tests: Union[bool, List[str], Set[str]] = False,
        explicit_set: Optional[Set[str]] = None,
        has_mirrors: bool = True,
    ):
        """Construct a build graph from the given specs. This includes only packages that need to
        be installed. Installed packages are pruned from the graph, and build dependencies are only
        included when necessary."""
        self.roots = {s.dag_hash() for s in specs}
        self.nodes = {s.dag_hash(): s for s in specs}
        self.parent_to_child: Dict[str, Set[str]] = {}
        self.child_to_parent: Dict[str, Set[str]] = {}
        overwrite_set = overwrite_set or set()
        explicit_set = explicit_set or set()
        self.pruned: Set[str] = set()
        self.done: Set[str] = set()
        self.force_source: Set[str] = set()
        stack: List[Tuple[spack.spec.Spec, InstallPolicy]] = [
            (s, root_policy) for s in self.nodes.values()
        ]

        self.tests = tests

        with database.read_transaction():
            # Set the install prefix for each spec based on the db record or store layout
            for s in spack.traverse.traverse_nodes(specs):
                _, record = database.query_by_spec_hash(s.dag_hash())
                if record and record.path:
                    s.set_prefix(record.path)
                else:
                    s.set_prefix(spack.store.STORE.layout.path_for_spec(s))

            # Build the graph and determine which specs to prune
            while stack:
                spec, install_policy = stack.pop()
                key = spec.dag_hash()
                _, record = database.query_by_spec_hash(key)
                depflag = self._base_deptypes(spec)

                # Conditionally include build dependencies. Don't prune installed specs
                # that need to be marked explicit so they flow through the DB write path.
                if record and record.installed and key not in overwrite_set:
                    # If it needs to be marked explicit, keep it in the graph (don't prune).
                    if key not in explicit_set or record.explicit:
                        self.pruned.add(key)
                elif (
                    install_policy == "source_only"
                    or include_build_deps
                    or (install_policy == "auto" and not has_mirrors)
                ):
                    depflag |= dt.BUILD

                dependencies = list(spec.dependencies(deptype=depflag))

                # For spliced specs built from source, add build_spec as a pseudo-dependency
                # so it gets built before the spliced spec.
                if spec.build_spec is not spec and key not in self.pruned and (depflag & dt.BUILD):
                    bs = spec.build_spec
                    bh = bs.dag_hash()
                    if bh not in self.pruned:
                        _, bs_record = database.query_by_spec_hash(bh)
                        if not (bs_record and bs_record.installed):
                            dependencies.append(bs)
                        else:
                            self.done.add(bh)

                self.parent_to_child[key] = {d.dag_hash() for d in dependencies}

                # Enqueue new dependencies
                for d in dependencies:
                    if d.dag_hash() in self.nodes:
                        continue
                    self.nodes[d.dag_hash()] = d
                    stack.append((d, dependencies_policy))

        # Construct reverse lookup from child to parent
        for parent, children in self.parent_to_child.items():
            for child in children:
                if child in self.child_to_parent:
                    self.child_to_parent[child].add(parent)
                else:
                    self.child_to_parent[child] = {parent}

        # If we're not installing the package itself, mark root specs for pruning too
        if not install_package:
            self.pruned.update(s.dag_hash() for s in specs)

        # Prune specs from the build graph. Their parents become parents of their children and
        # their children become children of their parents.
        for key in self.pruned:
            for parent in self.child_to_parent.get(key, ()):
                self.parent_to_child[parent].remove(key)
                self.parent_to_child[parent].update(self.parent_to_child.get(key, ()))
            for child in self.parent_to_child.get(key, ()):
                self.child_to_parent[child].remove(key)
                self.child_to_parent[child].update(self.child_to_parent.get(key, ()))
            self.parent_to_child.pop(key, None)
            self.child_to_parent.pop(key, None)
            self.nodes.pop(key, None)

        # Check that all prefixes to be created are unique.
        prefixes = [s.prefix for s in self.nodes.values() if not s.external]
        if len(prefixes) != len(set(prefixes)):
            raise spack.error.InstallError(
                "Install prefix collision: "
                + ", ".join(p for p in prefixes if prefixes.count(p) > 1)
            )

        # If we're not installing dependencies, verify that all remaining nodes in the build graph
        # after pruning are roots. If there are any non-root nodes, it means there are uninstalled
        # dependencies that we're not supposed to install.
        if not install_deps:
            non_root_spec = next((v for k, v in self.nodes.items() if k not in self.roots), None)
            if non_root_spec is not None:
                raise spack.error.InstallError(
                    f"Failed to install in package only mode: dependency {non_root_spec} is not "
                    "installed"
                )

    def _base_deptypes(self, spec: spack.spec.Spec) -> dt.DepFlag:
        """Returns the dependency types that are always eagerly traversed. These are LINK, RUN, and
        conditionally TEST, but excludes BUILD. Build deps are deferred until after a build cache
        miss."""
        deptypes = dt.LINK | dt.RUN
        if self.tests is True or (self.tests and spec.name in self.tests):
            deptypes |= dt.TEST
        return deptypes

    def enqueue_parents(self, dag_hash: str, pending_builds: List[str]) -> None:
        """After a spec is installed, remove it from the graph and enqueue any parents that are
        now ready to install.

        Args:
            dag_hash: The dag_hash of the spec that was just installed
            pending_builds: List to append parent specs that are ready to build
        """
        self.done.add(dag_hash)
        # Remove node and edges from the node in the build graph
        self.parent_to_child.pop(dag_hash, None)
        self.nodes.pop(dag_hash, None)
        parents = self.child_to_parent.pop(dag_hash, None)

        if not parents:
            return

        # Enqueue any parents and remove edges to the installed child
        for parent in parents:
            children = self.parent_to_child[parent]
            children.remove(dag_hash)
            if not children:
                pending_builds.append(parent)

    def has_unexpanded_build_deps(self, dag_hash: str) -> bool:
        return bool(self.get_unexpanded_build_deps(dag_hash))

    def get_unexpanded_build_deps(self, dag_hash: str) -> List["spack.spec.Spec"]:
        """Returns a list of unprocessed build deps for a spec."""
        spec = self.nodes[dag_hash]
        base_deptypes = self._base_deptypes(spec)
        unexpanded = []
        for edge in spec.edges_to_dependencies(depflag=dt.BUILD):
            if (edge.depflag & base_deptypes) == 0:
                unexpanded.append(edge.spec)
        if dag_hash in self.force_source and spec.build_spec is not spec:
            bh = spec.build_spec.dag_hash()
            if bh not in self.nodes and bh not in self.done and bh not in self.pruned:
                unexpanded.append(spec.build_spec)
        return unexpanded

    def expand_build_deps(
        self,
        spec_hashes: List[str],
        pending_builds: List[str],
        database: "spack.database.Database",
        dependencies_policy: InstallPolicy = "auto",
    ) -> List[str]:
        """Expand build dependencies for a list of specs after binary cache misses.

        Adds the spec's build deps and their transitive runtime deps to the graph. When
        ``dependencies_policy`` is ``"source_only"``, build deps of newly added specs are included
        immediately. Installed deps are skipped without adding edges.

        The caller must hold the database read lock and have called ``db._read()``.

        Returns the list of newly added dag hashes."""
        # Seed with tuples of (parent_hash, dep) for each to-be-expanded build dep
        stack = [(h, dep) for h in spec_hashes for dep in self.get_unexpanded_build_deps(h)]
        newly_added: List[str] = []

        while stack:
            parent_hash, dep = stack.pop()
            dep_hash = dep.dag_hash()

            # Skip installed deps
            if dep_hash in self.pruned or dep_hash in self.done:
                continue

            # If already in the graph (e.g. overwrite build in progress), add edge but don't
            # re-add node. This must be checked before the DB installed check, because an
            # overwrite build is installed in the DB but not yet done.
            if dep_hash in self.nodes:
                self.parent_to_child.setdefault(parent_hash, set()).add(dep_hash)
                self.child_to_parent.setdefault(dep_hash, set()).add(parent_hash)
                continue

            _, record = database.query_by_spec_hash(dep_hash)
            if record and record.installed:
                self.done.add(dep_hash)
                continue

            # Add forward/reverse edge
            self.parent_to_child.setdefault(parent_hash, set()).add(dep_hash)
            self.child_to_parent.setdefault(dep_hash, set()).add(parent_hash)

            # New node: add to graph and recurse into its link/run/test deps
            self.nodes[dep_hash] = dep
            self.parent_to_child.setdefault(dep_hash, set())
            newly_added.append(dep_hash)

            deptype = self._base_deptypes(dep)
            if dependencies_policy == "source_only":
                deptype |= dt.BUILD
            for child in dep.dependencies(deptype=deptype):
                stack.append((dep_hash, child))

        # Enqueue nodes that are ready (no uninstalled children)
        for h in newly_added:
            if not self.parent_to_child[h]:
                pending_builds.append(h)
        for dag_hash in spec_hashes:
            if not self.parent_to_child[dag_hash]:
                pending_builds.append(dag_hash)

        return newly_added


class ScheduleResult(NamedTuple):
    """Return value of :func:`schedule_builds`."""

    #: True if any pending builds were blocked on locks held by other processes.
    blocked: bool
    #: ``(dag_hash, lock)`` pairs where the write lock is held and the caller must start the build
    #: and eventually release the lock.
    to_start: List[Tuple[str, spack.util.lock.Lock]]
    #: ``(dag_hash, spec, lock)`` triples found already installed by another process; the read lock
    #: is held and the caller must add it to retained_read_locks.
    newly_installed: List[Tuple[str, spack.spec.Spec, spack.util.lock.Lock]]
    #: Actions to mark already installed specs explicit in the DB.
    to_mark_explicit: List[MarkExplicitAction]


def schedule_builds(
    pending: List[str],
    build_graph: BuildGraph,
    db: spack.database.Database,
    prefix_locker: spack.database.SpecLocker,
    overwrite: Set[str],
    overwrite_time: float,
    capacity: int,
    needs_jobserver_token: bool,
    jobserver: PosixJobServer,
    explicit: Set[str],
) -> ScheduleResult:
    """Try to schedule as many pending builds as possible.

    For each pending spec, attempts to acquire a non-blocking per-spec write lock. If the write
    lock times out, a read lock is tried as a fallback: a successful read lock means the first
    process finished and downgraded its write lock. If the DB confirms the spec is installed, it
    is captured as newly_installed; if the DB says it is not installed, the concurrent process was
    likely killed mid-build, and the spec is retried next iteration. Under both the DB read lock
    and the prefix lock, checks whether another process has already installed the spec. If so,
    captures it as newly_installed (caller enqueues parents) and keeps a read lock on the prefix
    to prevent concurrent uninstall. Otherwise, acquires a jobserver token if needed and adds the
    (dag_hash, lock) pair to to_start (caller launches the build).

    Args:
        pending: List of dag hashes pending installation; modified in-place.
        build_graph: The build dependency graph; used for node lookup and parent enqueueing.
        db: Package database; used for read lock and installed-status queries.
        prefix_locker: Per-spec write locker.
        overwrite: Set of dag hashes to overwrite even if already installed.
        overwrite_time: Timestamp (from time.time()) at which the overwrite install was requested.
            A spec in ``overwrite`` whose DB installation_time >= overwrite_time was installed by
            a concurrent process after our request started and should be treated as done.
        capacity: Maximum number of new builds to add to to_start in this call.
        needs_jobserver_token: True if a jobserver token is required for the first new build.
        jobserver: Jobserver for acquiring tokens.
        explicit: Set of dag hashes to mark explicit in the DB if found already installed.

    Returns:
        A :class:`ScheduleResult` with ``blocked``, ``to_start``, and ``newly_installed``
        fields; see :class:`ScheduleResult` for field semantics.
    """
    to_start: List[Tuple[str, spack.util.lock.Lock]] = []
    newly_installed: List[Tuple[str, spack.spec.Spec, spack.util.lock.Lock]] = []
    to_mark_explicit: List[MarkExplicitAction] = []
    blocked = True

    # Acquire the DB read lock non-blocking; hold it throughout the loop so the in-memory snapshot
    # stays consistent while we acquire per-spec prefix locks.
    if not db.lock.try_acquire_read():
        return ScheduleResult(blocked, to_start, newly_installed, to_mark_explicit)

    try:
        db._read()  # refresh in-memory snapshot under the read lock

        idx = 0
        while capacity and idx < len(pending):
            dag_hash = pending[idx]
            spec = build_graph.nodes[dag_hash]
            lock = prefix_locker.lock(spec)

            if lock.try_acquire_write():
                blocked = False
                have_write = True
            elif lock.try_acquire_read():
                have_write = False
            else:
                idx += 1
                continue

            # Check installed status under the DB read lock and prefix lock.
            upstream, record = db.query_by_spec_hash(dag_hash)

            # If the spec is already installed, treat it as done regardless of lock type.
            # A spec in the overwrite set is also treated as done if another process installed it
            # after our overwrite request was created (installation_time >= overwrite_time).
            if (
                record
                and record.installed
                and (dag_hash not in overwrite or record.installation_time >= overwrite_time)
            ):
                if have_write:
                    lock.downgrade_write_to_read()
                # keep the read lock (either downgraded or already a read lock)
                del pending[idx]
                newly_installed.append((dag_hash, spec, lock))
                # It's already installed, but needs to be marked as explicitly installed in the DB.
                if dag_hash in explicit and not record.explicit:
                    to_mark_explicit.append(MarkExplicitAction(spec))
                build_graph.enqueue_parents(dag_hash, pending)
                continue

            if not have_write:
                # If have to install but only got a read lock, try it in next iteration of the
                # event loop.
                lock.release_read()
                idx += 1
                continue

            # Write lock acquired: proceed with scheduling.
            # Don't schedule builds for specs from upstream databases.
            if upstream and record and not record.installed:
                lock.release_write()
                raise spack.error.InstallError(
                    f"Cannot install {spec}: it is uninstalled in an upstream database."
                )

            # Defensively assert prefix invariants
            if not spec.external:
                if (
                    dag_hash in overwrite
                    and record
                    and record.installed
                    and record.path != spec.prefix
                ):
                    # Cannot do an overwrite install to a different prefix.
                    lock.release_write()
                    raise spack.error.InstallError(
                        f"Prefix mismatch in overwrite of {spec}: expected {record.path}, "
                        f"got {spec.prefix}"
                    )
                elif dag_hash not in overwrite and spec.prefix in db._installed_prefixes:
                    # Prevent install prefix collision with other specs.
                    lock.release_write()
                    raise spack.error.InstallError(
                        f"Cannot install {spec}: prefix {spec.prefix} already exists"
                    )

            # Acquire a jobserver token if needed. The first (implicit) job needs no token.
            if needs_jobserver_token and not jobserver.acquire(1):
                lock.release_write()
                break  # no tokens available right now; stop scheduling

            del pending[idx]
            to_start.append((dag_hash, lock))
            capacity -= 1
            needs_jobserver_token = True  # all subsequent jobs need a token

    finally:
        db.lock.release_read()

    return ScheduleResult(blocked, to_start, newly_installed, to_mark_explicit)


def _node_to_roots(roots: List[spack.spec.Spec]) -> Dict[str, FrozenSet[str]]:
    """Map each node in a graph to the set of root node DAG hashes that can reach it.

    Args:
        roots: List of root specs.

    Returns:
        A dictionary mapping each node's dag_hash to a frozenset of root dag_hashes.
    """
    node_to_roots: Dict[str, FrozenSet[str]] = {
        s.dag_hash(): frozenset([s.dag_hash()]) for s in roots
    }

    for edge in spack.traverse.traverse_edges(
        roots, order="topo", cover="edges", root=False, key=spack.traverse.by_dag_hash
    ):
        parent_roots = node_to_roots[edge.parent.dag_hash()]
        child_hash = edge.spec.dag_hash()
        existing = node_to_roots.get(child_hash)

        if existing is None:
            node_to_roots[child_hash] = parent_roots  # keep a reference if no mutation is needed
        elif not parent_roots.issubset(existing):
            node_to_roots[child_hash] = existing | parent_roots

    return node_to_roots


class ReportData:
    """Data collected for reports during installation."""

    def __init__(self, roots: List[spack.spec.Spec]):
        self.roots = roots
        self.build_records: Dict[str, spack.report.InstallRecord] = {}

    def start_record(self, spec: spack.spec.Spec) -> None:
        """Begin an InstallRecord for a spec that is about to be built."""
        if spec.external:
            return
        record = spack.report.InstallRecord(spec)
        record.start()
        self.build_records[spec.dag_hash()] = record

    def finish_record(
        self, spec: spack.spec.Spec, exitcode: int, log_path: Optional[str] = None
    ) -> None:
        """Mark the InstallRecord for a spec as succeeded or failed."""
        record = self.build_records.get(spec.dag_hash())
        if record is None or spec.external:
            return
        if exitcode == ExitCode.SUCCESS:
            record.succeed(log_path)
        else:
            record.fail(
                spack.error.InstallError(
                    f"Installation of {spec.name} failed; see log for details"
                ),
                log_path,
            )

    def finalize(
        self, reports: Dict[str, spack.report.RequestRecord], build_graph: BuildGraph
    ) -> None:
        """Finalize InstallRecords and append them to RequestRecords after all builds finish.

        Args:
            reports: Map of root dag_hash to RequestRecord to append to.
            build_graph: The build graph containing all nodes and their states.
        """
        node_to_roots = _node_to_roots(self.roots)

        for spec in spack.traverse.traverse_nodes(self.roots):
            h = spec.dag_hash()
            if h in self.build_records:
                record = self.build_records[h]
            else:
                record = spack.report.InstallRecord(spec)
                if spec.external:
                    msg = "Spec is external"
                elif h in build_graph.pruned:
                    msg = "Spec was not scheduled for installation"
                elif h in build_graph.nodes:
                    msg = "Dependencies failed to install"
                else:
                    # If not installed or failed (build_records), not statically pruned ahead of
                    # time (build_graph.pruned), and also not scheduled (build_graph.nodes), it
                    # means it was in pending_builds or running_builds but never started/finished.
                    # This branch is followed on KeyboardInterrupt and --fail-fast.
                    msg = "Installation was interrupted"
                record.skip(msg=msg)

            for root_hash in node_to_roots[h]:
                reports[root_hash].append_record(record)


class NullReportData(ReportData):
    """No-op drop-in for ReportData when no reporter is configured.

    Avoids creating InstallRecords and reading log files on every completed build."""

    def __init__(self) -> None:
        pass

    def start_record(self, spec: spack.spec.Spec) -> None:
        pass

    def finish_record(
        self, spec: spack.spec.Spec, exitcode: int, log_path: Optional[str] = None
    ) -> None:
        pass

    def finalize(
        self, reports: Dict[str, spack.report.RequestRecord], build_graph: "BuildGraph"
    ) -> None:
        pass


def _signal_children(running_builds: Dict[int, PosixChildInfo], sig: signal.Signals) -> None:
    """Send a signal to the process group of each running build."""
    for child in running_builds.values():
        try:
            pid = child.proc.pid
            if pid is not None:
                os.killpg(pid, sig)
        except OSError:
            pass


class PackageInstaller:
    explicit: Set[str]

    def __init__(
        self,
        packages: List["spack.package_base.PackageBase"],
        *,
        dirty: bool = False,
        explicit: Union[Set[str], bool] = False,
        overwrite: Optional[Union[List[str], Set[str]]] = None,
        fail_fast: bool = False,
        fake: bool = False,
        include_build_deps: bool = False,
        install_deps: bool = True,
        install_package: bool = True,
        install_source: bool = False,
        keep_prefix: bool = False,
        keep_stage: bool = False,
        restage: bool = True,
        skip_patch: bool = False,
        stop_at: Optional[str] = None,
        stop_before: Optional[str] = None,
        tests: Union[bool, List[str], Set[str]] = False,
        unsigned: Optional[bool] = None,
        verbose: bool = False,
        concurrent_packages: Optional[int] = None,
        root_policy: InstallPolicy = "auto",
        dependencies_policy: InstallPolicy = "auto",
        create_reports: bool = False,
    ) -> None:
        assert install_package or install_deps, "Must install package, dependencies or both"

        self.install_source = install_source
        self.stop_at = stop_at
        self.stop_before = stop_before
        self.tests: Union[bool, List[str], Set[str]] = tests

        self.db = spack.store.STORE.db

        specs = [pkg.spec for pkg in packages]

        self.has_mirrors = bool(spack.mirrors.mirror.MirrorCollection(binary=True))
        self.root_policy: InstallPolicy = root_policy
        self.dependencies_policy: InstallPolicy = dependencies_policy
        self.include_build_deps = include_build_deps
        #: Set of DAG hashes to overwrite (if already installed)
        self.overwrite: Set[str] = set(overwrite) if overwrite else set()
        #: Time at which the overwrite install was requested; used to detect concurrent overwrites.
        self.overwrite_time: float = time.time()
        self.keep_prefix = keep_prefix
        self.fail_fast = fail_fast

        # Buffer for incoming, partially received state data from child processes
        self.state_buffers: Dict[int, str] = {}

        if explicit is True:
            self.explicit = {spec.dag_hash() for spec in specs}
        elif explicit is False:
            self.explicit = set()
        else:
            self.explicit = explicit

        # Build the dependency graph
        self.build_graph = BuildGraph(
            specs,
            root_policy,
            dependencies_policy,
            include_build_deps,
            install_package,
            install_deps,
            self.db,
            self.overwrite,
            tests,
            self.explicit,
            self.has_mirrors,
        )

        #: check what specs we could fetch from binaries (checks against cache, not remotely)
        try:
            spack.binary_distribution.BINARY_INDEX.update()
        except spack.binary_distribution.FetchCacheError:
            pass

        self.binary_cache_for_spec = {
            s.dag_hash(): spack.binary_distribution.BINARY_INDEX.find_by_hash(
                s.build_spec.dag_hash()
            )
            for s in self.build_graph.nodes.values()
        }
        self.unsigned = unsigned
        self.dirty = dirty
        self.fake = fake
        self.restage = restage
        self.keep_stage = keep_stage
        self.skip_patch = skip_patch

        #: queue of packages ready to install (no children)
        self.pending_builds = [
            parent for parent, children in self.build_graph.parent_to_child.items() if not children
        ]

        #: specs awaiting build-dep expansion (deferred until DB read lock is available)
        self.pending_expansions: List[str] = []

        self.verbose = verbose
        self.running_builds: Dict[int, PosixChildInfo] = {}
        self.log_paths: Dict[str, str] = {}
        self.build_status = BuildStatus(
            len(self.build_graph.nodes),
            verbose=verbose,
            filter_padding=spack.store.STORE.has_padding(),
            is_tty=TerminalState.stdout_is_interactive(),
        )
        self.jobs = spack.config.determine_number_of_jobs(parallel=True)
        self.build_status.actual_jobs = self.jobs
        self.build_status.target_jobs = self.jobs
        if concurrent_packages is None:
            concurrent_packages_config = spack.config.get("config:concurrent_packages", 0)
            # The value 0 in config means no limit (other than self.jobs)
            if concurrent_packages_config == 0:
                self.capacity = sys.maxsize
            else:
                self.capacity = concurrent_packages_config
        else:
            self.capacity = concurrent_packages

        # The reports property is what the old installer has and used as public interface.
        if create_reports:
            self.reports = {spec.dag_hash(): spack.report.RequestRecord(spec) for spec in specs}
            self.report_data = ReportData(specs)
        else:
            self.reports = {}
            self.report_data = NullReportData()

        self.next_database_write = 0.0

    def install(self) -> None:
        self._installer()

    def _installer(self) -> None:
        spack.store.STORE.install_sbang()
        jobserver = PosixJobServer(self.jobs)
        selector = selectors.DefaultSelector()

        # Set up terminal handling (cbreak, signals, stdin registration)
        terminal: Optional[BaseTerminalState] = None
        stdin_reader: Optional[StdinReaderBase] = None
        if TerminalState.stdin_is_interactive():
            terminal = TerminalState(
                selector,
                self.build_status,
                on_suspend=lambda: _signal_children(self.running_builds, signal.SIGSTOP),
                on_resume=lambda: _signal_children(self.running_builds, signal.SIGCONT),
            )
            terminal.setup()
            stdin_reader = terminal.create_stdin_reader()

        # Finished builds that have not yet been written to the database.
        database_actions: List[DatabaseAction] = []
        # Prefix read locks retained after DB flush (downgraded from write locks in _save_to_db).
        retained_read_locks: List[spack.util.lock.Lock] = []

        failures: List[spack.spec.Spec] = []
        finished_pids: List[int] = []

        try:
            # Try to schedule builds immediately. The first job does not require a token.
            if self.pending_builds:
                blocked = self._schedule_builds(
                    selector, jobserver, retained_read_locks, database_actions
                )
                self.build_status.set_blocked(blocked and not self.running_builds)

            while (
                self.pending_builds
                or self.running_builds
                or database_actions
                or self.pending_expansions
            ):
                # Monitor the jobserver when we have pending builds, capacity, and at least one
                # spec is not locked by another process. Also listen if the target parallelism is
                # reduced.
                wake_on_jobserver = (
                    self.pending_builds
                    and self.capacity
                    and not blocked
                    or not jobserver.has_target_parallelism()
                )
                if wake_on_jobserver and jobserver.r not in selector.get_map():
                    selector.register(jobserver.r, selectors.EVENT_READ, "jobserver")
                elif not wake_on_jobserver and jobserver.r in selector.get_map():
                    selector.unregister(jobserver.r)

                stdin_ready = False

                if self.build_status.headless:
                    # no UI to update, but check background to foreground transition periodically
                    timeout = HEADLESS_WAKE_INTERVAL
                elif self.build_status.is_tty:
                    timeout = SPINNER_INTERVAL
                else:
                    # when not in interactive mode, wake least often (no spinner/terminal updates)
                    timeout = DATABASE_WRITE_INTERVAL
                events = selector.select(timeout=timeout)

                finished_pids.clear()

                # The transition "suspended to foreground/background" is handled in the signal
                # handler, but there's no SIGCONT event in the transition of background to
                # foreground, so we conditionally poll for that here (headless case). In the
                # headless case the event loop only fires once per second, so this is cheap enough.
                if terminal and self.build_status.headless and terminal.should_enter_foreground():
                    terminal.enter_foreground()

                for key, _ in events:
                    data = key.data
                    if isinstance(data, FdInfo):
                        # Child output (logs and state updates)
                        child_info = self.running_builds[data.pid]
                        if data.name == "output":
                            self._handle_child_logs(key.fd, child_info, selector)
                        elif data.name == "state":
                            self._handle_child_state(key.fd, child_info, selector)
                        elif data.name == "sentinel":
                            finished_pids.append(data.pid)
                    elif data == "stdin":
                        stdin_ready = True
                    elif data == "sigwinch":
                        assert terminal is not None
                        terminal.drain_sigwinch()
                        self.build_status.on_resize()
                    elif data == "jobserver" and not jobserver.has_target_parallelism():
                        jobserver.maybe_discard_tokens()
                        self.build_status.set_jobs(jobserver.num_jobs, jobserver.target_jobs)

                current_time = time.monotonic()
                for pid in finished_pids:
                    self._handle_finished_build(
                        pid, current_time, jobserver, selector, failures, database_actions
                    )

                if failures and self.fail_fast:
                    # Terminate other builds to actually fail fast. We continue in the event loop
                    # waiting for child processes to finish, which may take a little while.
                    for child in self.running_builds.values():
                        child.proc.terminate()
                    self.pending_builds.clear()

                if stdin_ready and stdin_reader is not None:
                    for char in stdin_reader.read():
                        overview = self.build_status.overview_mode
                        if overview and self.build_status.search_mode:
                            self.build_status.search_input(char)
                        elif overview and char == "/":
                            self.build_status.enter_search()
                        elif char == "v" or char in ("q", "\x1b") and not overview:
                            self.build_status.toggle()
                        elif char == "n":
                            self.build_status.next(1)
                        elif char == "p" or char == "N":
                            self.build_status.next(-1)
                        elif char == "+":
                            jobserver.increase_parallelism()
                            self.build_status.set_jobs(jobserver.num_jobs, jobserver.target_jobs)
                        elif char == "-":
                            jobserver.decrease_parallelism()
                            self.build_status.set_jobs(jobserver.num_jobs, jobserver.target_jobs)

                # Insert into the database if we have any finished builds, and either the delay
                # interval has passed, or we're done with all builds. The database save is not
                # guaranteed; it fails if another process holds the lock. We'll try again next
                # iteration of the event loop in that case.
                if (
                    database_actions
                    and (
                        current_time >= self.next_database_write
                        or not (self.pending_builds or self.running_builds)
                    )
                    and self._save_to_db(database_actions, retained_read_locks)
                ):
                    database_actions.clear()

                # Try to expand build deps for cache-miss specs. This requires a read lock on the
                # database, meaning that it can take several iterations of the event loop in case
                # of contention with other processes.
                if self.pending_expansions:
                    self._try_expand_build_deps()

                # Try to schedule more builds, acquiring per-spec locks and jobserver tokens.
                if self.capacity and self.pending_builds:
                    blocked = self._schedule_builds(
                        selector, jobserver, retained_read_locks, database_actions
                    )
                    self.build_status.set_blocked(blocked and not self.running_builds)

                # Finally update the UI
                self.build_status.update()
        finally:
            # Restore input settings and signal handlers. On POSIX this runs TCSADRAIN,
            # ensuring buffered cursor-movement codes from the event loop are transmitted
            # before the final render.
            if terminal is not None:
                terminal.teardown_input()

            # Flush any not-yet-written successful builds to the DB; save the exception on error
            # to be re-raised after best-effort cleanup.
            db_exc = None
            if database_actions:
                try:
                    with self.db.write_transaction():
                        for action in database_actions:
                            action.save_to_db(self.db)
                except Exception as e:
                    db_exc = e

            # Send SIGTERM to running builds; this is a no-op in the successful case.
            for child in self.running_builds.values():
                try:
                    child.proc.terminate()
                except Exception:
                    pass

            # Release our jobserver token for each terminated build and then join.
            for child in self.running_builds.values():
                try:
                    jobserver.release()
                    child.proc.join(timeout=30)
                    if child.proc.is_alive():
                        child.proc.kill()
                        child.proc.join()
                except Exception:
                    pass

            # Release all held locks best-effort, so that one failure does not prevent the others
            # from being released.
            for child in self.running_builds.values():
                child.release_prefix_lock()

            for lock in retained_read_locks:
                try:
                    lock.release_read()
                except Exception:
                    pass
            for action in database_actions:
                action.release_prefix_lock()

            try:
                self.build_status.overview_mode = True
                self.build_status.update(finalize=True)
                selector.close()
                jobserver.close()
            except Exception:
                pass

            # Restore output settings. On Linux this is a no-op. On Windows this disables
            # VT100 processing and must happen after the final render.
            if terminal is not None:
                terminal.teardown_output()

            # Re-raise the DB exception if any.
            if db_exc is not None:
                raise db_exc

        try:
            self.report_data.finalize(self.reports, build_graph=self.build_graph)
        except Exception as e:
            spack.llnl.util.tty.debug(f"[{__name__}]: Failed to finalize reports: {e}]")

        # Clean up temp log files of successful builds now that reports have consumed them.
        if not self.keep_stage:
            failed_hashes = {s.dag_hash() for s in failures}
            for dag_hash, log_path in self.log_paths.items():
                if log_path == os.devnull or dag_hash in failed_hashes:
                    continue
                try:
                    os.unlink(log_path)
                except OSError:
                    pass

        if failures:
            for s in failures:
                build_info = self.build_status.builds[s.dag_hash()]
                if build_info and build_info.log_summary:
                    sys.stderr.write(build_info.log_summary)
            lines = [f"{s}: {self.log_paths[s.dag_hash()]}" for s in failures]
            raise spack.error.InstallError(
                "The following packages failed to install:\n" + "\n".join(lines)
            )

    def _handle_finished_build(
        self,
        pid: int,
        current_time: float,
        jobserver: PosixJobServer,
        selector: selectors.BaseSelector,
        failures: List[spack.spec.Spec],
        database_actions: List[DatabaseAction],
    ) -> None:
        """Handle a build that has finished. Remove from running_builds; release jobserver token;
        update UI state; defer database insertion if successful; possibly reschedule if failed with
        cache miss; register failures."""
        build = self.running_builds.pop(pid)
        dag_hash = build.spec.dag_hash()
        self.capacity += 1
        jobserver.release()
        self.build_status.set_jobs(jobserver.num_jobs, jobserver.target_jobs)
        self._drain_child_output(build, selector)
        self._drain_child_state(build, selector)
        exitcode = build.close(selector)
        self.report_data.finish_record(build.spec, exitcode, build.log_path)

        if exitcode == ExitCode.SUCCESS:
            # Schedule successful builds for batched database insertion. We don't release the
            # prefix lock here; that strictly happens after a successful db write.
            database_actions.append(build)
            self.build_graph.enqueue_parents(dag_hash, self.pending_builds)
            self.next_database_write = current_time + DATABASE_WRITE_INTERVAL
            self.build_status.update_state(dag_hash, "finished")
            return

        # When we don't have to do a db write, we can release the lock immediately.
        build.release_prefix_lock()

        is_root = dag_hash in self.build_graph.roots
        user_policy = self.root_policy if is_root else self.dependencies_policy

        if exitcode == ExitCode.STOPPED_AT_PHASE:
            return  # the user requested early stopping; don't treat as failure
        elif exitcode == ExitCode.BUILD_CACHE_MISS and user_policy == "auto":
            # Check if we can reschedule this as a source build after a build cache miss. If so,
            # return early without recording a failure.
            self.build_graph.force_source.add(dag_hash)
            self.build_status.remove_build(dag_hash)
            if self.build_graph.has_unexpanded_build_deps(dag_hash):
                self.pending_expansions.append(dag_hash)
            else:
                self.pending_builds.append(dag_hash)
        elif not failures or not self.fail_fast:
            # Record a failure. In fail-fast mode, only record the first failure; subsequent
            # failures may be a consequence of us terminating other builds.
            failures.append(build.spec)
            self.build_status.update_state(dag_hash, "failed")
            self.build_status.parse_log_summary(dag_hash)

    def _try_expand_build_deps(self) -> None:
        """Try to expand build deps for specs with cache misses. Non-blocking: returns immediately
        if the DB read lock is unavailable."""
        if not self.db.lock.try_acquire_read():
            return
        try:
            self.db._read()
            dep_policy = (
                "source_only"
                if (self.dependencies_policy == "auto" and not self.has_mirrors)
                else self.dependencies_policy
            )
            newly_added = self.build_graph.expand_build_deps(
                self.pending_expansions, self.pending_builds, self.db, dep_policy
            )
            for h in newly_added:
                self.binary_cache_for_spec[h] = (
                    spack.binary_distribution.BINARY_INDEX.find_by_hash(h)
                )
            self.build_status.total += len(newly_added)
            self.pending_expansions.clear()
        finally:
            self.db.lock.release_read()

    def _save_to_db(
        self,
        database_actions: List[DatabaseAction],
        retained_read_locks: List[spack.util.lock.Lock],
    ) -> bool:
        if not self.db.lock.try_acquire_write():
            return False
        try:
            self.db._read()
            for action in database_actions:
                action.save_to_db(self.db)
        finally:
            self.db.lock.release_write(self.db._write)

        # DB has been written and flushed; downgrade per-spec prefix write locks to read locks so
        # other processes can see the specs are installed, while preventing concurrent uninstalls.
        for action in database_actions:
            if action.prefix_lock is not None:
                try:
                    action.prefix_lock.downgrade_write_to_read()
                    retained_read_locks.append(action.prefix_lock)
                except Exception:
                    action.prefix_lock.release_write()
                    raise
                finally:
                    action.prefix_lock = None

        return True

    def _schedule_builds(
        self,
        selector: selectors.BaseSelector,
        jobserver: PosixJobServer,
        retained_read_locks: List[spack.util.lock.Lock],
        database_actions: List[DatabaseAction],
    ) -> bool:
        """Try to schedule as many pending builds as possible.

        Delegates to the module-level schedule_builds() function and then performs the
        side-effects that require the selector and running-build state: updating build_status for
        specs that were found already installed, and launching new builds via _start().

        Preconditions: self.capacity > 0 and self.pending_builds is not empty.

        Returns True if we had capacity to schedule, but were blocked by locks held by other
        processes. In that case we should not monitor the jobserver for new tokens, since we'd end
        up in a busy wait loop until the locks are released.
        """
        result = schedule_builds(
            pending=self.pending_builds,
            build_graph=self.build_graph,
            db=self.db,
            prefix_locker=spack.store.STORE.prefix_locker,
            overwrite=self.overwrite,
            overwrite_time=self.overwrite_time,
            capacity=self.capacity,
            needs_jobserver_token=bool(self.running_builds),
            jobserver=jobserver,
            explicit=self.explicit,
        )
        blocked = result.blocked
        database_actions.extend(result.to_mark_explicit)
        # Specs installed by another process.
        for dag_hash, spec, lock in result.newly_installed:
            retained_read_locks.append(lock)
            explicit = dag_hash in self.explicit
            self.build_status.add_build(spec, explicit=explicit)
            self.build_status.update_state(dag_hash, "finished")
        # Specs we can start building ourselves.
        for dag_hash, lock in result.to_start:
            self._start(selector, jobserver, dag_hash, lock)
        return blocked

    def _effective_install_policy(self, dag_hash: str, is_root: bool) -> InstallPolicy:
        """Compute the effective install policy based on the user policy and dynamic factors such
        as build cache availability and whether build dependencies can be skipped."""
        if dag_hash in self.build_graph.force_source:
            return "source_only"
        policy = self.root_policy if is_root else self.dependencies_policy
        if policy == "auto" and not self.has_mirrors:
            return "source_only"
        if policy == "auto" and not self.include_build_deps:
            # In case we don't require build deps and we have a binary cache configured, we install
            # build dependencies only if needed. This works in two steps: force a cache_only
            # install, and if that fails, add to force_source and schedule build deps so that a
            # second attempt uses the source_only policy. Therefore, return cache_only here.
            return "cache_only"
        return policy

    def _start(
        self,
        selector: selectors.BaseSelector,
        jobserver: PosixJobServer,
        dag_hash: str,
        prefix_lock: spack.util.lock.Lock,
    ) -> None:
        self.capacity -= 1
        explicit = dag_hash in self.explicit
        spec = self.build_graph.nodes[dag_hash]
        is_develop = spec.is_develop
        tests = self.tests
        run_tests = tests is True or bool(tests and spec.name in tests)
        is_root = dag_hash in self.build_graph.roots
        # Both possible sub-processes (cache install, source build) append to the same log file.
        if dag_hash not in self.log_paths:
            if spec.external:
                self.log_paths[dag_hash] = os.devnull
            else:
                log_fd, log_path = tempfile.mkstemp(
                    prefix=f"spack-stage-{spec.name}-{spec.version}-{spec.dag_hash()}-",
                    suffix=".log",
                    dir=spack.stage.get_stage_root(),
                )
                os.close(log_fd)
                self.log_paths[dag_hash] = log_path

        child_info = start_build(
            spec,
            explicit=explicit,
            mirrors=self.binary_cache_for_spec[dag_hash],
            unsigned=self.unsigned,
            install_policy=self._effective_install_policy(dag_hash, is_root),
            dirty=self.dirty,
            # keep_stage/restage logic taken from installer.py
            keep_stage=self.keep_stage or is_develop,
            restage=self.restage and not is_develop,
            keep_prefix=self.keep_prefix,
            skip_patch=self.skip_patch,
            fake=self.fake,
            install_source=self.install_source,
            run_tests=run_tests,
            jobserver=jobserver,
            log_path=self.log_paths[dag_hash],
            stop_before=self.stop_before if is_root else None,
            stop_at=self.stop_at if is_root else None,
        )
        child_info.prefix_lock = prefix_lock
        pid = child_info.proc.pid
        assert type(pid) is int
        self.running_builds[pid] = child_info
        selector.register(
            child_info.output_r_conn.fileno(), selectors.EVENT_READ, FdInfo(pid, "output")
        )
        selector.register(
            child_info.state_r_conn.fileno(), selectors.EVENT_READ, FdInfo(pid, "state")
        )
        selector.register(child_info.proc.sentinel, selectors.EVENT_READ, FdInfo(pid, "sentinel"))
        self.build_status.add_build(
            child_info.spec,
            explicit=explicit,
            control_w_conn=child_info.control_w_conn,
            log_path=child_info.log_path,
        )
        self.report_data.start_record(spec)

    def _handle_child_logs(
        self, r_fd: int, child_info: PosixChildInfo, selector: selectors.BaseSelector
    ) -> None:
        """Handle reading output logs from a child process pipe."""
        try:
            # There might be more data than OUTPUT_BUFFER_SIZE, but we will read that in the next
            # iteration of the event loop to keep things responsive.
            data = os.read(r_fd, OUTPUT_BUFFER_SIZE)
        except BlockingIOError:
            return
        except OSError:
            data = None

        if not data:  # EOF or error
            try:
                selector.unregister(r_fd)
            except KeyError:
                pass
            return

        self.build_status.print_logs(child_info.spec.dag_hash(), data)

    def _drain_child_output(
        self, child_info: PosixChildInfo, selector: selectors.BaseSelector
    ) -> None:
        """Read and print any remaining output from a finished child's pipe."""
        r_fd = child_info.output_r_conn.fileno()
        while r_fd in selector.get_map():
            self._handle_child_logs(r_fd, child_info, selector)

    def _drain_child_state(
        self, child_info: PosixChildInfo, selector: selectors.BaseSelector
    ) -> None:
        """Read and process any remaining state messages from a finished child's pipe."""
        r_fd = child_info.state_r_conn.fileno()
        while r_fd in selector.get_map():
            self._handle_child_state(r_fd, child_info, selector)

    def _handle_child_state(
        self, r_fd: int, child_info: PosixChildInfo, selector: selectors.BaseSelector
    ) -> None:
        """Handle reading state updates from a child process pipe."""
        try:
            # There might be more data than OUTPUT_BUFFER_SIZE, but we will read that in the next
            # iteration of the event loop to keep things responsive.
            data = os.read(r_fd, OUTPUT_BUFFER_SIZE)
        except BlockingIOError:
            return
        except OSError:
            data = None

        if not data:  # EOF or error
            try:
                selector.unregister(r_fd)
            except KeyError:
                pass
            self.state_buffers.pop(r_fd, None)
            return

        # Append new data to the buffer for this fd and process it
        buffer = self.state_buffers.get(r_fd, "") + data.decode(errors="replace")
        lines = buffer.split("\n")

        # The last element of split() will be a partial line or an empty string.
        # We store it back in the buffer for the next read.
        self.state_buffers[r_fd] = lines.pop()

        for line in lines:
            if not line:
                continue
            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "state" in message:
                self.build_status.update_state(child_info.spec.dag_hash(), message["state"])
            elif "progress" in message and "total" in message:
                self.build_status.update_progress(
                    child_info.spec.dag_hash(), message["progress"], message["total"]
                )
            elif "installed_from_binary_cache" in message:
                child_info.spec.package.installed_from_binary_cache = True


class BinaryCacheMiss(spack.error.SpackError):
    pass
