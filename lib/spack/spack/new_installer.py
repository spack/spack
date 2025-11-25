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

import fcntl
import io
import json
import os
import re
import selectors
import shutil
import sys
import tempfile
import termios
import threading
import time
import traceback
import tty
from gzip import GzipFile
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from typing import TYPE_CHECKING, Callable, Dict, Generator, List, Optional, Set, Tuple, Union

from spack.vendor.typing_extensions import Literal

import spack.binary_distribution
import spack.build_environment
import spack.builder
import spack.config
import spack.database
import spack.deptypes as dt
import spack.error
import spack.hooks
import spack.llnl.util.lock
import spack.llnl.util.tty
import spack.paths
import spack.report
import spack.spec
import spack.store
import spack.url_buildcache
import spack.util.lock

if TYPE_CHECKING:
    import spack.package_base

#: Type for specifying installation source modes
InstallPolicy = Literal["auto", "cache_only", "source_only"]

#: How often to update a spinner in seconds
SPINNER_INTERVAL = 0.1

#: How long to display finished packages before graying them out
CLEANUP_TIMEOUT = 2.0

#: Size of the output buffer for child processes
OUTPUT_BUFFER_SIZE = 4096

#: Suffix for temporary backup during overwrite install
OVERWRITE_BACKUP_SUFFIX = ".old"

#: Suffix for temporary cleanup during failed install
OVERWRITE_GARBAGE_SUFFIX = ".garbage"


class ChildInfo:
    """Information about a child process."""

    __slots__ = ("proc", "spec", "output_r_conn", "state_r_conn", "control_w_conn", "explicit")

    def __init__(
        self,
        proc: Process,
        spec: spack.spec.Spec,
        output_r_conn: Connection,
        state_r_conn: Connection,
        control_w_conn: Connection,
        explicit: bool = False,
    ) -> None:
        self.proc = proc
        self.spec = spec
        self.output_r_conn = output_r_conn
        self.state_r_conn = state_r_conn
        self.control_w_conn = control_w_conn
        self.explicit = explicit

    def cleanup(self, selector: selectors.BaseSelector) -> None:
        """Unregister and close file descriptors, and join the child process."""
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


def send_state(state: str, state_pipe: io.TextIOWrapper) -> None:
    """Send a state update message."""
    json.dump({"state": state}, state_pipe, separators=(",", ":"))
    state_pipe.write("\n")


def send_progress(current: int, total: int, state_pipe: io.TextIOWrapper) -> None:
    """Send a progress update message."""
    json.dump({"progress": current, "total": total}, state_pipe, separators=(",", ":"))
    state_pipe.write("\n")


def tee(control_r: int, log_r: int, file_w: int, parent_w: int) -> None:
    """Forward log_r to file_w and parent_w (if echoing is enabled).
    Echoing is enabled and disabled by reading from control_r."""
    echo_on = False
    selector = selectors.DefaultSelector()
    selector.register(log_r, selectors.EVENT_READ)
    selector.register(control_r, selectors.EVENT_READ)

    try:
        while True:
            for key, _ in selector.select():
                if key.fd == log_r:
                    data = os.read(log_r, OUTPUT_BUFFER_SIZE)
                    if not data:  # EOF: exit the thread
                        return
                    os.write(file_w, data)
                    if echo_on:
                        os.write(parent_w, data)

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


class Tee:
    """Emulates ./build 2>&1 | tee build.log. The output is sent both to a log file and the parent
    process (if echoing is enabled). The control_fd is used to enable/disable echoing. The initial
    log file is /dev/null and can be changed later with set_output_file()."""

    def __init__(self, control: Connection, parent: Connection) -> None:
        self.control = control
        self.parent = parent
        dev_null_fd = os.open(os.devnull, os.O_WRONLY)
        #: The file descriptor of the log file (initially /dev/null)
        self.log_fd = os.dup(dev_null_fd)
        os.close(dev_null_fd)
        r, w = os.pipe()
        self.tee_thread = threading.Thread(
            target=tee,
            args=(self.control.fileno(), r, self.log_fd, self.parent.fileno()),
            daemon=True,
        )
        self.tee_thread.start()
        os.dup2(w, sys.stdout.fileno())
        os.dup2(w, sys.stderr.fileno())
        os.close(w)

    def set_output_file(self, path: str) -> None:
        """Redirect output to the specified log file."""
        log_fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
        os.dup2(log_fd, self.log_fd)
        os.close(log_fd)

    def close(self) -> None:
        # Closing stdout and stderr should close the last reference to the write end of the pipe,
        # causing the tee thread to wake up, flush the last data, and exit.
        os.close(sys.stdout.fileno())
        os.close(sys.stderr.fileno())
        self.tee_thread.join()
        # Only then close the other fds.
        self.control.close()
        self.parent.close()
        os.close(self.log_fd)


def install_from_buildcache(
    mirrors: List[spack.url_buildcache.MirrorURLAndVersion],
    spec: spack.spec.Spec,
    unsigned: Optional[bool],
    state_stream: io.TextIOWrapper,
) -> bool:
    send_state("fetching from build cache", state_stream)
    tarball_stage = spack.binary_distribution.download_tarball(spec.build_spec, unsigned, mirrors)

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

    return True


class PrefixPivoter:
    """Manages the installation prefix during overwrite installations."""

    def __init__(self, prefix: str, overwrite: bool, keep_prefix: bool = False) -> None:
        """Initialize the prefix pivoter.

        Args:
            prefix: The installation prefix path
            overwrite: Whether to allow overwriting an existing prefix
            keep_prefix: Whether to keep a failed installation prefix (when not overwriting)
        """
        self.prefix = prefix
        #: Whether to allow installation when the prefix exists
        self.overwrite = overwrite
        #: Whether to keep a failed installation prefix
        self.keep_prefix = keep_prefix
        #: Temporary location for the original prefix during overwrite
        self.tmp_prefix: Optional[str] = None
        self.parent = os.path.dirname(prefix)

    def __enter__(self) -> "PrefixPivoter":
        """Enter the context: move existing prefix to temporary location if needed."""
        if not self._lexists(self.prefix):
            return self
        if not self.overwrite:
            raise spack.error.InstallError(f"Install prefix {self.prefix} already exists")
        # Move the existing prefix to a temporary location
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
            # Success: remove the backup in case of overwrite
            if self.tmp_prefix is not None:
                self._rmtree_ignore_errors(self.tmp_prefix)
            return

        # Failure handling:
        # Priority 1: If we're overwriting, always restore the original prefix
        # Priority 2: If keep_prefix is False, remove the failed installation

        if self.overwrite and self.tmp_prefix is not None:
            # Overwrite case: restore the original prefix if it existed
            # The highest priority is to restore the original prefix, so we try to:
            # rename prefix -> garbage: move failed dir out of the way
            # rename tmp_prefix -> prefix: restore original prefix
            # remove garbage (this is allowed to fail)
            garbage = self._mkdtemp(dir=self.parent, prefix=".", suffix=OVERWRITE_GARBAGE_SUFFIX)
            try:
                self._rename(self.prefix, garbage)
                has_failed_prefix = True
            except FileNotFoundError:  # prefix dir does not exist, so we don't have to delete it.
                has_failed_prefix = False
            self._rename(self.tmp_prefix, self.prefix)
            if has_failed_prefix:
                self._rmtree_ignore_errors(garbage)
        elif not self.keep_prefix and self._lexists(self.prefix):
            # Not overwriting, keep_prefix is False: remove the failed installation
            garbage = self._mkdtemp(dir=self.parent, prefix=".", suffix=OVERWRITE_GARBAGE_SUFFIX)
            self._rename(self.prefix, garbage)
            self._rmtree_ignore_errors(garbage)
        # else: keep_prefix is True, leave the failed prefix in place

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
    mirrors: List[spack.url_buildcache.MirrorURLAndVersion],
    unsigned: Optional[bool],
    install_policy: InstallPolicy,
    dirty: bool,
    keep_stage: bool,
    overwrite: bool,
    keep_prefix: bool,
    skip_patch: bool,
    state: Connection,
    parent: Connection,
    echo_control: Connection,
    makeflags: str,
    js1: Optional[Connection],
    js2: Optional[Connection],
    store: spack.store.Store,
    config: spack.config.Configuration,
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
        overwrite: Whether to overwrite the existing install prefix
        keep_prefix: Whether to keep a failed installation prefix
        skip_patch: Whether to skip the patch phase
        state: Connection to send state updates to
        parent: Connection to send build output to
        echo_control: Connection to receive echo control messages from
        makeflags: MAKEFLAGS to set, so that the build process uses the POSIX jobserver
        js1: Connection for old style jobserver read fd (if any). Unused, just to inherit fd.
        js2: Connection for old style jobserver write fd (if any). Unused, just to inherit fd.
        store: global store instance from parent
        config: global config instance from parent
    """

    # TODO: don't start a build for external packages
    if spec.external:
        return

    tee = Tee(echo_control, parent)

    os.environ["MAKEFLAGS"] = makeflags
    spack.store.STORE = store
    spack.config.CONFIG = config
    spack.paths.set_working_dir()

    # Use closedfd=false because of the connection objects. Use line buffering.
    state_stream = os.fdopen(state.fileno(), "w", buffering=1, closefd=False)
    exit_code = 0

    try:
        with PrefixPivoter(spec.prefix, overwrite, keep_prefix):
            _install(
                spec,
                explicit,
                mirrors,
                unsigned,
                install_policy,
                dirty,
                keep_stage,
                skip_patch,
                state_stream,
                tee,
                store,
            )
    except Exception:
        traceback.print_exc()  # log the traceback to the log file
        exit_code = 1
    finally:
        tee.close()
        state_stream.close()

    sys.exit(exit_code)


def _install(
    spec: spack.spec.Spec,
    explicit: bool,
    mirrors: List[spack.url_buildcache.MirrorURLAndVersion],
    unsigned: Optional[bool],
    install_policy: InstallPolicy,
    dirty: bool,
    keep_stage: bool,
    skip_patch: bool,
    state_stream: io.TextIOWrapper,
    tee: Tee,
    store: spack.store.Store = spack.store.STORE,
) -> None:
    """Install a spec from build cache or source."""

    # Create the stage and log file before starting the tee thread.
    pkg = spec.package
    spack.build_environment.setup_package(pkg, dirty=dirty)

    # Try to install from buildcache, unless user asked for source only
    if install_policy != "source_only":
        if mirrors and install_from_buildcache(mirrors, spec, unsigned, state_stream):
            spack.hooks.post_install(spec, explicit)
            return
        elif install_policy == "cache_only":
            # Binary required but not available
            send_state("no binary available", state_stream)
            raise spack.error.InstallError(f"No binary available for {spec}")

    store.layout.create_install_directory(spec)

    stage = pkg.stage

    # Then try a source build.
    with stage:
        # Set whether to keep the stage after installation
        stage.keep = keep_stage

        stage.destroy()
        stage.create()

        # Start collecting logs.
        tee.set_output_file(pkg.log_path)

        send_state("staging", state_stream)

        if not skip_patch:
            pkg.do_patch()
        else:
            pkg.do_stage()

        os.chdir(stage.source_path)

        spack.hooks.pre_install(spec)

        for phase in spack.builder.create(pkg):
            send_state(phase.name, state_stream)
            phase.execute()

        # Install source build logs
        with open(pkg.log_path, "rb") as f, open(pkg.install_log_path, "wb") as g:
            # Use GzipFile directly so we can omit filename / mtime in header
            gzip_file = GzipFile(filename="", mode="wb", compresslevel=6, mtime=0, fileobj=g)
            shutil.copyfileobj(f, gzip_file)
            gzip_file.close()

        spack.hooks.post_install(spec, explicit)


class JobServer:
    """Attach to an existing POSIX jobserver or create a FIFO-based one."""

    def __init__(self, num_jobs: int) -> None:
        #: Keep track of how many tokens Spack itself has acquired, which is used to release them.
        self.tokens_acquired = 0
        self.num_jobs = num_jobs
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
        os.write(self.w, b"+")
        self.tokens_acquired -= 1

    def close(self) -> None:
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
        # TODO: implement a sanity check here:
        # 1. did we release all tokens we acquired?
        # 2. if we created the jobserver, did the children return all tokens?
        self.r_conn.close()
        self.w_conn.close()


def start_build(
    spec: spack.spec.Spec,
    explicit: bool,
    mirrors: List[spack.url_buildcache.MirrorURLAndVersion],
    unsigned: Optional[bool],
    install_policy: InstallPolicy,
    dirty: bool,
    keep_stage: bool,
    overwrite: bool,
    keep_prefix: bool,
    skip_patch: bool,
    jobserver: JobServer,
) -> ChildInfo:
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
            overwrite,
            keep_prefix,
            skip_patch,
            state_w_conn,
            output_w_conn,
            control_r_conn,
            makeflags,
            None if fifo else jobserver.r_conn,
            None if fifo else jobserver.w_conn,
            spack.store.STORE,
            spack.config.CONFIG,
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

    return ChildInfo(proc, spec, output_r_conn, state_r_conn, control_w_conn, explicit)


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
        "progress_percent",
        "control_w_conn",
    )

    def __init__(self, spec: spack.spec.Spec, explicit: bool, control_w_conn: Connection) -> None:
        self.state: str = "starting"
        self.explicit: bool = explicit
        self.version: str = str(spec.version)
        self.hash: str = spec.dag_hash(7)
        self.name: str = spec.name
        self.external: bool = spec.external
        self.prefix: str = spec.prefix
        self.finished_time: Optional[float] = None
        self.progress_percent: Optional[int] = None
        self.control_w_conn = control_w_conn


class BuildStatus:
    """Tracks the build status display for terminal output."""

    def __init__(
        self,
        total: int,
        stdout: io.TextIOWrapper = sys.stdout,  # type: ignore[assignment]
        get_terminal_size: Callable[[], Tuple[int, int]] = os.get_terminal_size,
        get_time: Callable[[], float] = time.monotonic,
        is_tty: Optional[bool] = None,
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

        self.stdout = stdout
        self.get_terminal_size = get_terminal_size
        self.get_time = get_time
        self.is_tty = is_tty if is_tty is not None else self.stdout.isatty()

    def add_build(self, spec: spack.spec.Spec, explicit: bool, control_w_conn: Connection) -> None:
        """Add a new build to the display and mark the display as dirty."""
        self.builds[spec.dag_hash()] = BuildInfo(spec, explicit, control_w_conn)
        self.dirty = True

    def toggle(self) -> None:
        """Toggle between overview mode and following a specific build."""
        if self.overview_mode:
            self.next()
        else:
            self.active_area_rows = 0
            self.search_term = ""
            self.search_mode = False
            self.overview_mode = True
            self.dirty = True
            try:
                os.write(self.builds[self.tracked_build_id].control_w_conn.fileno(), b"0")
            except (KeyError, OSError):
                pass
            self.tracked_build_id = ""

    def search_input(self, input: str) -> None:
        """Handle keyboard input when in search mode"""
        if input in ("\r", "\n"):
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
            if build.finished_time is None and self._is_displayed(build)
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
                os.write(self.builds[self.tracked_build_id].control_w_conn.fileno(), b"0")
            except (KeyError, OSError):
                pass

        self.tracked_build_id = new_build_id

        # Tell the user we're following new logs, and instruct the child to start sending them.
        self.stdout.write(
            f"\n==> Following logs of {new_build.name}" f"\033[0;36m@{new_build.version}\033[0m\n"
        )
        self.stdout.flush()
        try:
            os.write(new_build.control_w_conn.fileno(), b"1")
        except (KeyError, OSError):
            pass

    def update_state(self, build_id: str, state: str) -> None:
        """Update the state of a package and mark the display as dirty."""
        build_info = self.builds[build_id]
        build_info.state = state
        build_info.progress_percent = None

        if state in ("finished", "failed"):
            self.completed += 1
            build_info.finished_time = self.get_time() + CLEANUP_TIMEOUT

            if build_id == self.tracked_build_id and not self.overview_mode:
                self.toggle()

        self.dirty = True

        # For non-TTY output, print state changes immediately without colors
        if not self.is_tty:
            self.stdout.write(
                f"{build_info.hash} {build_info.name}@{build_info.version}: {state}\n"
            )
            self.stdout.flush()

    def update_progress(self, build_id: str, current: int, total: int) -> None:
        """Update the progress of a package and mark the display as dirty."""
        percent = int((current / total) * 100)
        build_info = self.builds[build_id]
        if build_info.progress_percent != percent:
            build_info.progress_percent = percent
            self.dirty = True

    def update(self, finalize: bool = False) -> None:
        """Redraw the interactive display."""
        if not self.is_tty or not self.overview_mode:
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

        if not self.dirty:
            return

        # Build the overview output in a buffer and print all at once to avoid flickering.
        buffer = io.StringIO()

        # Move cursor up to the start of the display area
        if self.active_area_rows > 0:
            buffer.write(f"\033[{self.active_area_rows}F")

        max_width, max_height = self.get_terminal_size()

        self.total_lines = 0
        total_finished = len(self.finished_builds)

        # First flush the finished builds. These are "persisted" in terminal history.
        for build in self.finished_builds:
            self._render_build(build, buffer, max_width)
        self.finished_builds.clear()

        # Then a header followed by the active builds. This is the "mutable" part of the display.
        long_header_len = len(
            f"Progress: {self.completed}/{self.total}  /: filter  v: logs  n/p: next/prev"
        )
        if long_header_len < max_width:
            self._println(
                buffer,
                f"\033[1mProgress:\033[0m {self.completed}/{self.total}"
                "  \033[36m/\033[0m: filter  \033[36mv\033[0m: logs"
                "  \033[36mn\033[0m/\033[36mp\033[0m: next/prev",
            )
        else:
            self._println(buffer, f"\033[1mProgress:\033[0m {self.completed}/{self.total}")

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
            self._render_build(build, buffer, max_width)

        if self.search_mode:
            buffer.write(f"filter> {self.search_term}\033[K")

        # Clear any remaining lines from previous display
        buffer.write("\033[0J")

        # Print everything at once to avoid flickering
        self.stdout.write(buffer.getvalue())
        self.stdout.flush()

        # Update the number of lines drawn for next time. It reflects the number of active builds.
        self.active_area_rows = self.total_lines - total_finished
        self.dirty = False

        # Schedule next UI update
        self.next_update = now + SPINNER_INTERVAL / 2

    def _println(self, buffer: io.StringIO, line: str = "") -> None:
        """Print a line to the buffer, handling line clearing and cursor movement."""
        self.total_lines += 1
        if line:
            buffer.write(line)
        if self.total_lines > self.active_area_rows:
            buffer.write("\033[0m\033[K\n")  # reset, clear to EOL, newline
        else:
            buffer.write("\033[0m\033[K\033[1E")  # reset, clear to EOL, move down 1 line

    def print_logs(self, build_id: str, data: bytes) -> None:
        # Discard logs we are not following. Generally this should not happen as we tell the child
        # to only send logs when we are following it. It could maybe happen while transitioning
        # between builds.
        if self.overview_mode or build_id != self.tracked_build_id:
            return
        # TODO: drop initial bytes from data until first newline (?)
        self.stdout.buffer.write(data)
        self.stdout.flush()

    def _render_build(self, build_info: BuildInfo, buffer: io.StringIO, max_width: int) -> None:
        line_width = 0
        for component in self._generate_line_components(build_info):
            # ANSI escape sequence(s), does not contribute to width
            if not component.startswith("\033"):
                line_width += len(component)
                if line_width > max_width:
                    break
            buffer.write(component)
        self._println(buffer)

    def _generate_line_components(self, build_info: BuildInfo) -> Generator[str, None, None]:
        """Yield formatted line components for a package. Escape sequences are yielded as separate
        strings so they do not contribute to the line width."""
        if build_info.external:
            indicator = "[e]"
        elif build_info.state == "finished":
            indicator = "[+]"
        elif build_info.state == "failed":
            indicator = "[x]"
        else:
            indicator = f"[{self.spinner_chars[self.spinner_index]}]"

        if build_info.state == "failed":
            yield "\033[31m"  # red
        elif build_info.state == "finished":
            yield "\033[32m"  # green

        yield indicator
        yield "\033[0m"  # reset
        yield " "
        yield "\033[0;90m"  # dark gray
        yield build_info.hash
        yield "\033[0m"  # reset
        yield " "

        # Package name in bold white if explicit, default otherwise
        if build_info.explicit:
            yield "\033[1;37m"  # bold white
            yield build_info.name
            yield "\033[0m"  # reset
        else:
            yield build_info.name

        yield "\033[0;36m"  # cyan
        yield f"@{build_info.version}"
        yield "\033[0m"  # reset

        # progress or state
        if build_info.progress_percent is not None:
            yield " fetching"
            yield f": {build_info.progress_percent}%"
        elif build_info.state == "finished":
            yield f" {build_info.prefix}"
        else:
            yield f" {build_info.state}"


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
    ):
        """Construct a build graph from the given specs. This includes only packages that need to
        be installed. Installed packages are pruned from the graph, and build dependencies are only
        included when necessary."""
        self.roots = {s.dag_hash() for s in specs}
        self.nodes = {s.dag_hash(): s for s in specs}
        self.parent_to_child: Dict[str, Set[str]] = {}
        self.child_to_parent: Dict[str, Set[str]] = {}
        overwrite_set = overwrite_set or set()
        specs_to_prune: Set[str] = set()
        stack: List[Tuple[spack.spec.Spec, InstallPolicy]] = [
            (s, root_policy) for s in self.nodes.values()
        ]

        with database.read_transaction():
            while stack:
                spec, install_policy = stack.pop()
                key = spec.dag_hash()
                _, record = database.query_by_spec_hash(key)

                # Set the install prefix for each spec based on the db record or store layout
                if record and record.path:
                    spec.set_prefix(record.path)
                else:
                    spec.set_prefix(spack.store.STORE.layout.path_for_spec(spec))

                # Conditionally include build dependencies
                if record and record.installed and key not in overwrite_set:
                    specs_to_prune.add(key)
                    dependencies = spec.dependencies(deptype=dt.LINK | dt.RUN)
                elif install_policy == "cache_only" and not include_build_deps:
                    dependencies = spec.dependencies(deptype=dt.LINK | dt.RUN)
                else:
                    dependencies = spec.dependencies(deptype=dt.BUILD | dt.LINK | dt.RUN)

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
            specs_to_prune.update(s.dag_hash() for s in specs)

        # Prune specs from the build graph. Their parents become parents of their children and
        # their children become children of their parents.
        for key in specs_to_prune:
            for parent in self.child_to_parent.get(key, ()):
                self.parent_to_child[parent].remove(key)
                self.parent_to_child[parent].update(self.parent_to_child.get(key, ()))
            for child in self.parent_to_child.get(key, ()):
                self.child_to_parent[child].remove(key)
                self.child_to_parent[child].update(self.child_to_parent.get(key, ()))
            self.parent_to_child.pop(key, None)
            self.child_to_parent.pop(key, None)
            self.nodes.pop(key, None)

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

    def enqueue_parents(self, dag_hash: str, pending_builds: List[str]) -> None:
        """After a spec is installed, remove it from the graph and enqueue any parents that are
        now ready to install.

        Args:
            dag_hash: The dag_hash of the spec that was just installed
            pending_builds: List to append parent specs that are ready to build
        """
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


class PackageInstaller:

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
    ) -> None:
        assert install_package or install_deps, "Must install package, dependencies or both"

        if fail_fast:
            raise NotImplementedError("Fail-fast installs are not implemented")
        elif fake:
            raise NotImplementedError("Fake installs are not implemented")
        elif install_source:
            raise NotImplementedError("Installing sources is not implemented")
        elif not restage:
            raise NotImplementedError("Restaging builds is not implemented")
        elif stop_at is not None:
            raise NotImplementedError("Stopping at an install phase is not implemented")
        elif stop_before is not None:
            raise NotImplementedError("Stopping before an install phase is not implemented")
        elif tests is not False:
            raise NotImplementedError("Tests during install are not implemented")
        # verbose and concurrent_packages are not worth erroring out for

        specs = [pkg.spec for pkg in packages]

        self.root_policy: InstallPolicy = root_policy
        self.dependencies_policy: InstallPolicy = dependencies_policy
        self.include_build_deps = include_build_deps
        #: Set of DAG hashes to overwrite (if already installed)
        self.overwrite: Set[str] = set(overwrite) if overwrite else set()
        self.keep_prefix = keep_prefix

        # Buffer for incoming, partially received state data from child processes
        self.state_buffers: Dict[int, str] = {}

        # Build the dependency graph
        self.build_graph = BuildGraph(
            specs,
            root_policy,
            dependencies_policy,
            include_build_deps,
            install_package,
            install_deps,
            spack.store.STORE.db,
            self.overwrite,
        )

        #: check what specs we could fetch from binaries (checks against cache, not remotely)
        spack.binary_distribution.BINARY_INDEX.update()
        self.binary_cache_for_spec = {
            s.dag_hash(): spack.binary_distribution.BINARY_INDEX.find_by_hash(s.dag_hash())
            for s in self.build_graph.nodes.values()
        }
        self.unsigned = unsigned
        self.dirty = dirty
        self.keep_stage = keep_stage
        self.skip_patch = skip_patch

        #: queue of packages ready to install (no children)
        self.pending_builds = [
            parent for parent, children in self.build_graph.parent_to_child.items() if not children
        ]

        if explicit is True:
            self.explicit = {spec.dag_hash() for spec in specs}
        elif explicit is False:
            self.explicit = set()
        else:
            self.explicit = explicit

        self.running_builds: Dict[int, ChildInfo] = {}
        self.build_status = BuildStatus(len(self.build_graph.nodes))
        self.jobs = spack.config.determine_number_of_jobs(parallel=True)
        self.reports: Dict[str, spack.report.RequestRecord] = {}

    def install(self) -> None:
        # This installer has not implemented the per-spec exclusive locks during installation.
        # Instead, take an exclusive lock on the entire range to avoid that other Spack install
        # process start installing the same specs.
        lock = spack.util.lock.Lock(
            str(spack.store.STORE.prefix_locker.lock_path), desc="prefix lock"
        )
        lock.acquire_write()
        try:
            self._installer()
        finally:
            lock.release_write()

    def _installer(self) -> None:
        jobserver = JobServer(self.jobs)

        # Set stdin to non-blocking for key press detection
        if sys.stdin.isatty():
            old_stdin_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        else:
            old_stdin_settings = None

        selector = selectors.DefaultSelector()
        selector.register(sys.stdin.fileno(), selectors.EVENT_READ, "stdin")

        # Setup the database write lock. TODO: clean this up
        if isinstance(spack.store.STORE.db.lock, spack.util.lock.Lock):
            spack.store.STORE.db.lock._ensure_parent_directory()
            spack.store.STORE.db.lock._file = spack.llnl.util.lock.FILE_TRACKER.get_fh(
                spack.store.STORE.db.lock.path
            )

        to_insert_in_database: List[ChildInfo] = []
        failures: List[spack.spec.Spec] = []

        try:
            # Start the first job immediately, as it does not require a jobserver token.
            if self.pending_builds and not self.running_builds:
                self._start(selector, jobserver)

            while self.pending_builds or self.running_builds or to_insert_in_database:
                # Only monitor the jobserver if we have pending builds.
                if self.pending_builds and jobserver.r not in selector.get_map():
                    selector.register(jobserver.r, selectors.EVENT_READ, "jobserver")
                elif not self.pending_builds and jobserver.r in selector.get_map():
                    selector.unregister(jobserver.r)

                jobserver_token_available = False
                stdin_ready = False

                events = selector.select(timeout=SPINNER_INTERVAL)

                finished_pids = []

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
                    elif data == "jobserver":
                        jobserver_token_available = True
                    elif data == "stdin":
                        stdin_ready = True

                for pid in finished_pids:
                    build = self.running_builds.pop(pid)
                    jobserver.release()
                    build.cleanup(selector)
                    if build.proc.exitcode == 0:
                        to_insert_in_database.append(build)
                        self.build_status.update_state(build.spec.dag_hash(), "finished")
                    else:
                        failures.append(build.spec)
                        self.build_status.update_state(build.spec.dag_hash(), "failed")

                if stdin_ready:
                    try:
                        char = sys.stdin.read(1)
                    except OSError:
                        continue
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

                # Flush installed packages to the database and enqueue any parents that are now
                # ready.
                if to_insert_in_database and self._save_to_db(to_insert_in_database):
                    for entry in to_insert_in_database:
                        self.build_graph.enqueue_parents(
                            entry.spec.dag_hash(), self.pending_builds
                        )
                    to_insert_in_database.clear()

                # Again, the first job should start immediately and does not require a token.
                if self.pending_builds and not self.running_builds:
                    self._start(selector, jobserver)

                # For the rest we try to obtain tokens from the jobserver.
                if self.pending_builds and jobserver_token_available:
                    # Then we try to schedule as many jobs as we can acquire tokens for.
                    max_new_jobs = len(self.pending_builds)
                    for _ in range(jobserver.acquire(max_new_jobs)):
                        self._start(selector, jobserver)

                # Finally update the UI
                self.build_status.update()
        except KeyboardInterrupt:
            # Cleanup running builds.
            for child in self.running_builds.values():
                child.proc.join()
            raise
        finally:
            # Restore terminal settings
            if old_stdin_settings:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_stdin_settings)

            # Clean up resources
            # Final cleanup of any remaining finished packages before exit
            self.build_status.overview_mode = True
            self.build_status.update(finalize=True)
            selector.close()
            jobserver.close()

        if failures:
            lines = [f"{s}: {s.package.log_path}" for s in failures]
            raise spack.error.InstallError(
                "The following packages failed to install:\n" + "\n".join(lines)
            )

    def _save_to_db(self, to_insert_in_database: List[ChildInfo]) -> bool:
        db = spack.store.STORE.db
        try:
            # Only try to get the lock once (non-blocking). If it fails, try it next time.
            if db.lock.acquire_write(timeout=1e-9):
                db._read()
        except spack.util.lock.LockTimeoutError:
            return False
        try:
            for entry in to_insert_in_database:
                db._add(entry.spec, explicit=entry.explicit)
            return True
        finally:
            db.lock.release_write(db._write)

    def _start(self, selector: selectors.BaseSelector, jobserver: JobServer) -> None:
        dag_hash = self.pending_builds.pop()
        explicit = dag_hash in self.explicit
        child_info = start_build(
            self.build_graph.nodes[dag_hash],
            explicit=explicit,
            mirrors=self.binary_cache_for_spec[dag_hash],
            unsigned=self.unsigned,
            install_policy=(
                self.root_policy
                if dag_hash in self.build_graph.roots
                else self.dependencies_policy
            ),
            dirty=self.dirty,
            keep_stage=self.keep_stage,
            overwrite=dag_hash in self.overwrite,
            keep_prefix=self.keep_prefix,
            skip_patch=self.skip_patch,
            jobserver=jobserver,
        )
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
            child_info.spec, explicit=explicit, control_w_conn=child_info.control_w_conn
        )

    def _handle_child_logs(
        self, r_fd: int, child_info: ChildInfo, selector: selectors.BaseSelector
    ) -> None:
        """Handle reading output logs from a child process pipe."""
        try:
            # There might be more data than OUTPUT_BUFFER_SIZE, but we will read that in the next
            # iteration of the event loop to keep things responsive.
            data = os.read(r_fd, OUTPUT_BUFFER_SIZE)
        except OSError:
            data = None

        if not data:  # EOF or error
            try:
                selector.unregister(r_fd)
            except KeyError:
                pass
            return

        self.build_status.print_logs(child_info.spec.dag_hash(), data)

    def _handle_child_state(
        self, r_fd: int, child_info: ChildInfo, selector: selectors.BaseSelector
    ) -> None:
        """Handle reading state updates from a child process pipe."""
        try:
            # There might be more data than OUTPUT_BUFFER_SIZE, but we will read that in the next
            # iteration of the event loop to keep things responsive.
            data = os.read(r_fd, OUTPUT_BUFFER_SIZE)
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
            message = json.loads(line)
            if "state" in message:
                self.build_status.update_state(child_info.spec.dag_hash(), message["state"])
            elif "progress" in message and "total" in message:
                self.build_status.update_progress(
                    child_info.spec.dag_hash(), message["progress"], message["total"]
                )
