# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""New installer that will ultimately replace installer.py. It features an event loop, non-blocking
I/O, and a POSIX jobserver to limit concurrency. It also has a more advanced terminal UI. It's
mostly self-contained to avoid interfering with the rest of Spack too much while it's being
developed and tested."""

import fcntl
import io
import json
import os
import re
import selectors
import shutil
import signal
import sys
import tempfile
import termios
import threading
import time
import traceback
import tty
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from typing import TYPE_CHECKING, Dict, Generator, List, Optional, Set, Tuple, Union

import spack.binary_distribution
import spack.build_environment
import spack.builder
import spack.config
import spack.error
import spack.hooks
import spack.llnl.util.lock
import spack.paths
import spack.spec
import spack.store
import spack.traverse
import spack.url_buildcache
import spack.util.lock

if TYPE_CHECKING:
    import spack.package_base

#: How often to update a spinner in seconds
SPINNER_INTERVAL = 0.1

#: How long to display finished packages before graying them out
CLEANUP_TIMEOUT = 2.0

#: Size of the output buffer for child processes
OUTPUT_BUFFER_SIZE = 4096


def setup_signal_handling() -> int:
    """Set up signal handling for SIGCHLD using a wakeup pipe."""
    # A handler is still needed for set_wakeup_fd to work, but it can be a no-op.
    signal.signal(signal.SIGCHLD, lambda signum, frame: None)
    signal_r, signal_w = os.pipe()
    os.set_blocking(signal_r, False)
    os.set_blocking(signal_w, False)
    # This will write the signal number to the pipe, waking up select().
    signal.set_wakeup_fd(signal_w)
    return signal_r


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
                    if not data:
                        return
                    os.write(file_w, data)
                    if echo_on:
                        os.write(parent_w, data)

                elif key.fd == control_r:
                    control_data = os.read(control_r, 1)
                    if not control_data:
                        # Should be unreachable, but just in case avoid a busy loop where select
                        # immediately returns again because control_r hung up.
                        selector.unregister(control_r)
                    else:
                        echo_on = control_data == b"1"
    except OSError:  # do not raise
        pass
    finally:
        os.close(log_r)
        os.close(control_r)
        os.close(file_w)
        os.close(parent_w)


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
        tee_thread = threading.Thread(
            target=tee,
            args=(self.control.fileno(), r, self.log_fd, self.parent.fileno()),
            daemon=True,
        )
        tee_thread.start()
        os.dup2(w, sys.stdout.fileno())
        os.dup2(w, sys.stderr.fileno())
        os.close(w)

    def set_output_file(self, path: str) -> None:
        """Redirect output to the specified log file."""
        log_fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
        os.dup2(log_fd, self.log_fd)
        os.close(log_fd)

    def close(self) -> None:
        os.close(self.log_fd)
        sys.stdout.close()
        sys.stderr.close()
        self.control.close()
        self.parent.close()


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


def worker_function(
    spec: spack.spec.Spec,
    explicit: bool,
    mirrors: List[spack.url_buildcache.MirrorURLAndVersion],
    unsigned: Optional[bool],
    state: Connection,  # write end of state pipe
    parent: Connection,  # write end of output pipe to parent
    echo_control: Connection,  # read end of control pipe from parent
    js1: Optional[Connection],  # ensure that old style jobserver pipes are inherited
    js2: Optional[Connection],  # ensure that old style jobserver pipes are inherited
    store: spack.store.Store,
    config: spack.config.Configuration,
):
    # TODO: don't start a build for external packages
    if spec.external:
        return

    tee = Tee(echo_control, parent)

    spack.store.STORE = store
    spack.config.CONFIG = config
    spack.paths.set_working_dir()

    # Create the stage and log file before starting the tee thread.
    pkg = spec.package
    spack.build_environment.setup_package(pkg, dirty=False)

    # Use closedfd=false because of the connection objects. Use line buffering.
    state_stream = os.fdopen(state.fileno(), "w", buffering=1, closefd=False)

    # Create the install dir
    if os.path.exists(spec.prefix):
        shutil.rmtree(spec.prefix)

    # First try to install from binary cache.
    if mirrors and install_from_buildcache(mirrors, spec, unsigned, state_stream):
        spack.hooks.post_install(spec, explicit)
        return

    store.layout.create_install_directory(spec)
    stage = pkg.stage

    # Then try a source build.
    with stage:
        stage.destroy()
        stage.create()

        # Start collecting logs.
        tee.set_output_file(os.path.join(stage.path, "build.log"))

        send_state("staging", state_stream)
        pkg.do_patch()
        os.chdir(stage.source_path)

        try:
            spack.hooks.pre_install(spec)

            for phase_fn in spack.builder.create(pkg):
                send_state(phase_fn.name, state_stream)
                phase_fn.execute()

            spack.hooks.post_install(spec, explicit)

        except Exception:
            # Print all exceptions so they are logged.
            traceback.print_exc()
            sys.stderr.flush()
            sys.exit(1)
        finally:
            tee.close()
            state.close()


class JobServer:
    """Acts both as a jobserver client and server. The server is currently only FIFO-based but
    can easily be extended to support ordinary pipes."""

    def __init__(self, num_jobs: int) -> None:
        #: Keep track of how many tokens Spack itself has acquired, which is used to release them.
        self.tokens_acquired = 0
        self.num_jobs = num_jobs
        self.fifo_path: Optional[str] = None
        self.created = False

        fifo_config = get_jobserver_config()

        if type(fifo_config) is str:
            # FIFO-based jobserver. Try to open the FIFO.
            open_attempt = open_existing_jobserver_fifo(fifo_config)
            if open_attempt:
                self.r, self.w = open_attempt
                return
        elif type(fifo_config) is tuple:
            # Old style pipe-based jobserver. Validate the fds before using them.
            r, w = fifo_config
            if fcntl.fcntl(r, fcntl.F_GETFD) == -1 or fcntl.fcntl(w, fcntl.F_GETFD) == -1:
                self.r, self.w = r, w
                return

        # No existing jobserver we can connect to: create a FIFO-based one.
        self.r, self.w, self.fifo_path = create_jobserver_fifo(num_jobs)
        self.created = True

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
        os.close(self.r)
        os.close(self.w)


def start_build(
    spec: spack.spec.Spec,
    explicit: bool,
    mirrors: List[spack.url_buildcache.MirrorURLAndVersion],
    unsigned: Optional[bool],
    jobserver: JobServer,
) -> ChildInfo:
    """Start a new build."""
    # Create pipes for the child's output, state reporting, and control.
    state_r_conn, state_w_conn = Pipe(duplex=False)
    output_r_conn, output_w_conn = Pipe(duplex=False)
    control_r_conn, control_w_conn = Pipe(duplex=False)

    proc = Process(
        target=worker_function,
        args=(
            spec,
            explicit,
            mirrors,
            unsigned,
            state_w_conn,
            output_w_conn,
            control_r_conn,
            None if jobserver.fifo_path else Connection(jobserver.r),
            None if jobserver.fifo_path else Connection(jobserver.w),
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


def reap_children(
    child_data: Dict[int, ChildInfo], selector: selectors.BaseSelector, jobserver: JobServer
) -> List[int]:
    """Reap terminated child processes"""
    to_delete: List[int] = []
    for pid, child in child_data.items():
        if child.proc.is_alive():
            continue
        to_delete.append(pid)
        jobserver.release()
        try:
            selector.unregister(child.output_r_conn.fileno())
        except KeyError:
            pass
        try:
            selector.unregister(child.state_r_conn.fileno())
        except KeyError:
            pass
        child.output_r_conn.close()
        child.state_r_conn.close()
        child.control_w_conn.close()
        child.proc.join()
    return to_delete


def get_jobserver_config() -> Optional[Union[str, Tuple[int, int]]]:
    """Parse MAKEFLAGS for jobserver. Either it's a FIFO or (r, w) pair of file descriptors."""
    makeflags = os.environ.get("MAKEFLAGS", "")
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
        os.write(write_fd, b"+" * (num_jobs - 1))
        os.environ["MAKEFLAGS"] = f" -j{num_jobs} --jobserver-auth=fifo:{fifo_path}"
        return read_fd, write_fd, fifo_path
    except Exception:
        try:
            os.unlink(fifo_path)
        except OSError:
            pass
        try:
            os.rmdir(tmpdir)
        except OSError:
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

    def __init__(self, total: int) -> None:
        #: Ordered dict of build ID -> info
        self.total = total
        self.completed = 0
        self.builds: Dict[str, BuildInfo] = {}
        self.finished_builds: List[BuildInfo] = []
        self.spinner_chars = ["|", "/", "-", "\\"]
        self.spinner_index = 0
        self.dirty = True  # Start dirty to draw initial state
        self.last_lines_drawn = 0
        self.next_spinner_update = 0.0
        self.next_update = 0.0
        self.overview_mode = True  # Whether to draw the package overview
        self.tracked_build_id = ""  # identifier of the package whose logs we follow
        self.is_tty = sys.stdout.isatty()  # Whether stdout is a terminal

    def add_build(self, spec: spack.spec.Spec, explicit: bool, control_w_conn: Connection) -> None:
        """Add a new build to the display and mark the display as dirty."""
        self.builds[spec.dag_hash()] = BuildInfo(spec, explicit, control_w_conn)
        self.dirty = True

    def toggle(self) -> None:
        """Toggle between overview mode and following a specific build."""
        if self.overview_mode:
            self.next()
        else:
            self.last_lines_drawn = 0
            self.overview_mode = True
            self.dirty = True
            try:
                os.write(self.builds[self.tracked_build_id].control_w_conn.fileno(), b"0")
            except (KeyError, OSError):
                pass
            self.tracked_build_id = ""

    def _get_next(self, direction: int) -> Optional[str]:
        """Returns the next or previous unfinished build ID, or None if none found.
        Direction should be 1 for next, -1 for previous."""
        # We could consider an ordered dict here to avoid list() calls
        build_ids = list(self.builds)
        try:
            start = build_ids.index(self.tracked_build_id) + direction
        except ValueError:
            start = 0

        n = len(build_ids)
        for k in range(0, n):
            build_id = build_ids[(start + k * direction) % n]
            if self.builds[build_id].finished_time is None:
                return build_id

        return None

    def next(self, direction: int = 1) -> None:
        """Follow the logs of the next build in the list."""
        new_build_id = self._get_next(direction)

        if not new_build_id:
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
        print(
            f"\n==> Following logs of {new_build.name}" f"\033[0;36m@{new_build.version}\033[0m",
            flush=True,
        )
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
            build_info.finished_time = time.monotonic() + CLEANUP_TIMEOUT

            if build_id == self.tracked_build_id and not self.overview_mode:
                self.toggle()

        self.dirty = True

        # For non-TTY output, print state changes immediately without colors
        if not self.is_tty:
            print(f"{build_info.hash} {build_info.name}@{build_info.version}: {state}")

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

        now = time.monotonic()

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

        # Skip redraw when not in overview mode or when nothing changed
        if not self.dirty:
            return

        # Build the overview output in a buffer and print all at once to avoid flickering.
        buffer = io.StringIO()

        # Move cursor up to the start of the display area
        if self.last_lines_drawn > 0:
            buffer.write(f"\033[{self.last_lines_drawn}A")

        max_width = os.get_terminal_size().columns

        total_lines = 0
        end = "\033[1E"  # move to next line if overwriting, or newline if adding lines

        def advance() -> None:
            """Use cursor movement when we're overwriting a part of terminal we own, otherwise
            use newline to ensure the terminal scrolls properly."""
            nonlocal total_lines, end
            total_lines += 1
            if total_lines > self.last_lines_drawn:
                end = "\n"

        # First flush the finished builds. These are "persisted" in terminal history.
        for build in self.finished_builds:
            advance()
            self._render_build(build, buffer, max_width, end)
        self.finished_builds.clear()

        # Then a header followed by the active builds. This is the "mutable" part of the display.
        advance()
        buffer.write(f"\033[1mProgress:\033[0m {self.completed}/{self.total}")
        buffer.write(f"\033[0m\033[K{end}")
        for build in self.builds.values():
            advance()
            self._render_build(build, buffer, max_width, end)

        # Clear any remaining lines from previous display
        if total_lines < self.last_lines_drawn:
            buffer.write("\033[0J")

        # Print everything at once to avoid flickering
        sys.stdout.write(buffer.getvalue())
        sys.stdout.flush()

        # Update the number of lines drawn for the next tick. +1 for header.
        self.last_lines_drawn = len(self.builds) + 1
        self.dirty = False

        # Schedule next UI update
        self.next_update = now + SPINNER_INTERVAL / 2

    def print_logs(self, build_id: str, data: bytes) -> None:
        # Discard logs we are not following. Generally this should not happen as we tell the child
        # to only send logs when we are following it. It could maybe happen while transitioning
        # between builds.
        if self.overview_mode or build_id != self.tracked_build_id:
            return
        # TODO: drop initial bytes from data until first newline (?)
        sys.stdout.buffer.write(data)
        sys.stdout.flush()

    def _render_build(
        self, build_info: BuildInfo, buffer: io.StringIO, max_width: int, end: str
    ) -> None:
        line_width = 0
        for component in self._generate_line_components(build_info):
            # ANSI escape sequence(s), does not contribute to width
            if not component.startswith("\033"):
                line_width += len(component)
                if line_width > max_width:
                    break
            buffer.write(component)
        buffer.write(f"\033[0m\033[K{end}")  # reset, clear to end of line, newline

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


class PackageInstaller:

    def __init__(
        self,
        packages: List["spack.package_base.PackageBase"],
        *,
        cache_only: bool = False,
        dependencies_cache_only: bool = False,
        dependencies_use_cache: bool = True,
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
        package_cache_only: bool = False,
        package_use_cache: bool = True,
        restage: bool = False,
        skip_patch: bool = False,
        stop_at: Optional[str] = None,
        stop_before: Optional[str] = None,
        tests: Union[bool, List[str], Set[str]] = False,
        unsigned: Optional[bool] = None,
        use_cache: bool = False,
        verbose: bool = False,
        concurrent_packages: Optional[int] = None,
    ) -> None:
        specs = [pkg.spec for pkg in packages]

        # Buffer for incoming, partially received state data from child processes
        self.state_buffers: Dict[int, str] = {}

        #: lookup package by unique identifier
        self.nodes = {spec.dag_hash(): spec for spec in spack.traverse.traverse_nodes(specs)}

        #: mapping from parent to children (children are deleted installed)
        self.parent_to_child = {
            parent.dag_hash(): {child.dag_hash() for child in parent.dependencies()}
            for parent in self.nodes.values()
        }

        #: reverse mapping from child to parents
        self.child_to_parent: Dict[str, Set[str]] = {}
        for parent, children in self.parent_to_child.items():
            for child in children:
                if child not in self.child_to_parent:
                    self.child_to_parent[child] = set()
                self.child_to_parent[child].add(parent)

        # 1. Assign an install prefix to each spec
        # 2. Prune the build graph of already installed packages
        db = spack.store.STORE.db
        with db.read_transaction():
            for key in list(self.nodes):
                spec = self.nodes[key]
                _, record = db.query_by_spec_hash(key)
                if record and record.path:
                    spec.set_prefix(record.path)
                else:
                    spec.set_prefix(spack.store.STORE.layout.path_for_spec(spec))
                if not record:
                    continue
                # Remove node: wire children to parents and vice versa, delete node from graph.
                for parent in self.child_to_parent.get(key, ()):
                    self.parent_to_child[parent].remove(key)
                    self.parent_to_child[parent].update(self.parent_to_child.get(key, ()))
                for child in self.parent_to_child.get(key, ()):
                    self.child_to_parent[child].remove(key)
                    self.child_to_parent[child].update(self.child_to_parent.get(key, ()))
                self.parent_to_child.pop(key, None)
                self.child_to_parent.pop(key, None)
                del self.nodes[key]

        #: check what specs we could fetch from binaries (checks against cache, not remotely)
        spack.binary_distribution.BINARY_INDEX.update()
        self.binary_cache_for_spec = {
            s.dag_hash(): spack.binary_distribution.BINARY_INDEX.find_by_hash(s.dag_hash())
            for s in self.nodes.values()
        }
        self.unsigned = unsigned

        #: queue of packages ready to install (no children)
        self.pending_builds = [
            parent for parent, children in self.parent_to_child.items() if not children
        ]

        if explicit is True:
            self.explicit = {spec.dag_hash() for spec in specs}
        elif explicit is False:
            self.explicit = set()
        else:
            self.explicit = explicit

        self.running_builds: Dict[int, ChildInfo] = {}
        self.build_status = BuildStatus(len(self.nodes))
        self.jobs = spack.config.determine_number_of_jobs(parallel=True)

    def _enqueue_parents(self, dag_hash: str) -> None:
        # the job dag_hash has finished, so remove it from the mappings
        # and enqueue any parents that are now ready to install
        self.parent_to_child.pop(dag_hash, None)
        parents = self.child_to_parent.get(dag_hash)

        if not parents:
            return
        for parent in parents:
            children = self.parent_to_child[parent]
            children.remove(dag_hash)
            if not children:
                self.pending_builds.append(parent)

    def install(self) -> None:
        jobserver = JobServer(self.jobs)

        # Set up signal handling
        signal_r = setup_signal_handling()

        # Set stdin to non-blocking for key press detection
        old_stdin_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

        selector = selectors.DefaultSelector()
        selector.register(signal_r, selectors.EVENT_READ, "signal")
        selector.register(sys.stdin.fileno(), selectors.EVENT_READ, "stdin")

        # Setup the database write lock. TODO: clean this up
        if isinstance(spack.store.STORE.db.lock, spack.util.lock.Lock):
            spack.store.STORE.db.lock._ensure_parent_directory()
            spack.store.STORE.db.lock._file = spack.llnl.util.lock.FILE_TRACKER.get_fh(
                spack.store.STORE.db.lock.path
            )

        to_insert_in_database: List[ChildInfo] = []
        failures: List[spack.spec.Spec] = []

        # Continue until there are no more packages to install or running builds
        try:
            while self.pending_builds or self.running_builds or to_insert_in_database:

                # The first job starts immediately, because it does not need a token.
                if self.pending_builds and not self.running_builds:
                    self._start(selector, jobserver)

                # Subsequent jobs need to acquire a token from the jobserver first.
                if self.pending_builds and jobserver.r not in selector.get_map():
                    selector.register(jobserver.r, selectors.EVENT_READ, "jobserver")
                elif not self.pending_builds and jobserver.r in selector.get_map():
                    selector.unregister(jobserver.r)

                children_have_finished = False
                jobserver_token_available = False
                stdin_ready = False

                events = selector.select(timeout=SPINNER_INTERVAL)

                for key, _ in events:
                    data = key.data
                    if isinstance(data, FdInfo):
                        # Child output (logs and state updates)
                        child_info = self.running_builds[data.pid]
                        if data.name == "output":
                            self._handle_child_logs(key.fd, child_info, selector)
                        elif data.name == "state":
                            self._handle_child_state(key.fd, child_info, selector)
                    elif data == "signal":
                        children_have_finished = True
                    elif data == "jobserver":
                        jobserver_token_available = True
                    elif data == "stdin":
                        stdin_ready = True

                if children_have_finished:
                    try:
                        # Clear the signal pipe
                        os.read(signal_r, OUTPUT_BUFFER_SIZE)
                    except BlockingIOError:
                        pass
                    for pid in reap_children(self.running_builds, selector, jobserver):
                        build = self.running_builds.pop(pid)
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
                    if char == "v" or char == "q" and not self.build_status.overview_mode:
                        self.build_status.toggle()
                    elif char == "n":
                        self.build_status.next(1)
                    elif char == "p" or char == "N":
                        self.build_status.next(-1)

                # Flush installed packages to the database and enqueue any parents that are now
                # ready.
                if to_insert_in_database and self._save_to_db(to_insert_in_database):
                    for entry in to_insert_in_database:
                        self._enqueue_parents(entry.spec.dag_hash())
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
                child.proc.terminate()
            for child in self.running_builds.values():
                child.proc.join()
            for child in self.running_builds.values():
                shutil.rmtree(child.spec.prefix, ignore_errors=True)
            raise
        finally:
            # Restore terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_stdin_settings)

            # Clean up resources
            # Final cleanup of any remaining finished packages before exit
            self.build_status.overview_mode = True
            self.build_status.update(finalize=True)
            selector.close()
            jobserver.close()
            old_wakeup_fd = signal.set_wakeup_fd(-1)
            os.close(old_wakeup_fd)
            os.close(signal_r)

        if failures:
            raise spack.error.InstallError(f"Build failed for the following specs: {failures}")

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
        mirrors = self.binary_cache_for_spec[dag_hash]
        child_info = start_build(self.nodes[dag_hash], explicit, mirrors, self.unsigned, jobserver)
        pid = child_info.proc.pid
        assert type(pid) is int
        self.running_builds[pid] = child_info
        selector.register(
            child_info.output_r_conn.fileno(), selectors.EVENT_READ, FdInfo(pid, "output")
        )
        selector.register(
            child_info.state_r_conn.fileno(), selectors.EVENT_READ, FdInfo(pid, "state")
        )
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
