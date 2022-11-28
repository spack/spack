import os
import select

all = ["PosixJobserverClient"]


class NullJobserverClient:
    """Trivial job server that always gives as many jobs as you ask for."""

    def acquire(self, jobs: int):
        """
        Get the specified number of jobs. Note: the current process is a job
        itself, so the typical use is ``jobs = 1 + client.acquire(num_procs - 1)``.
        """
        return jobs

    def release(self):
        pass


class PosixJobserverClient:
    def __init__(self, rfd, wfd):
        self.rfd = rfd
        self.wfd = wfd
        self.tokens = b""

    def acquire(self, jobs: int):
        """Make a claim of at most ``jobs`` jobs. The return value is the number of
        jobs that can effectively be used."""
        ready, _, _ = select.select([self.rfd], [], [], 0.1)
        if self.rfd in ready:
            self.tokens = os.read(self.rfd, jobs)
            return len(self.tokens)
        else:
            return 0

    def release(self):
        """Release all acquired jobs"""
        if not self.tokens:
            return
        _, ready, _ = select.select([], [self.wfd], [], 0.1)
        if self.wfd in ready:
            os.write(self.wfd, self.tokens)
            self.tokens = b""


def parse_gnu_jobserver_filedescriptors(makeflags_str: bytes):
    """Parse a MAKEFLAGS string. Return the (read, write) file descriptors
    filenos of the jobserver, or the path to the FIFO if fifo:[path]
    was set, or None if not enabled."""
    # Look for the --jobserver-auth arg
    flag_name = b"--jobserver-auth="

    # Flag start
    flag_begin = makeflags_str.find(flag_name)
    if flag_begin == -1:
        return None

    # Flag value end
    value_end = makeflags_str.find(b" ", flag_begin)
    if value_end == -1:
        value_end = len(makeflags_str) + 1

    value_begin = flag_begin + len(flag_name)

    is_fifo = makeflags_str.startswith(b"fifo:", value_begin)

    if is_fifo:
        value_begin += 5

    value = makeflags_str[value_begin:value_end]

    # Return FIFO path
    if is_fifo:
        return value

    # There should be two items
    file_descriptors = value.split(b",")
    if len(file_descriptors) != 2:
        return None

    # And they should be integers
    try:
        rfd, wfd = int(file_descriptors[0]), int(file_descriptors[1])
    except ValueError:
        return None

    # -1 might be used to signal it's disabled.
    if rfd < 0 or wfd < 0:
        return None

    return rfd, wfd


def detect_posix_jobserver():
    makeflags = os.environb.get(b"MAKEFLAGS", None)

    if not makeflags:
        return None

    parse_result = parse_gnu_jobserver_filedescriptors(makeflags)

    # Failed to parse
    if not parse_result:
        return None

    # FIFO path
    if isinstance(parse_result, bytes):
        try:
            rfd = os.open(parse_result, os.O_RDONLY)
            wfd = os.open(parse_result, os.O_WRONLY)
        except OSError:
            return None
        return PosixJobserverClient(rfd, wfd)

    return PosixJobserverClient(parse_result[0], parse_result[1])


def jobserver_client_from_environment():
    """Construct a jobserver detected in the environment, or return
    a dummy jobserver if none can be found."""
    jobserver = detect_posix_jobserver()
    if jobserver:
        return jobserver

    return NullJobserverClient()
