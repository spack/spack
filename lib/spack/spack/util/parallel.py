# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import concurrent.futures
import multiprocessing
import os
import sys
import traceback
import warnings
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Type

from spack.util.cpus import cpus_available

#: Used in tests to disable parallelism, as tests themselves are parallelized
ENABLE_PARALLELISM = sys.platform != "win32"


class ErrorFromWorker:
    """Wrapper class to report an error from a worker process"""

    def __init__(self, exc_cls, exc, tb):
        """Create an error object from an exception raised from
        the worker process.

        The attributes of the process error objects are all strings
        as they are easy to send over a pipe.

        Args:
            exc: exception raised from the worker process
        """
        self.pid = os.getpid()
        self.error_message = str(exc)
        self.stacktrace_message = "".join(traceback.format_exception(exc_cls, exc, tb))

    @property
    def stacktrace(self):
        msg = "[PID={0.pid}] {0.stacktrace_message}"
        return msg.format(self)

    def __str__(self):
        return self.error_message


class WarningRecord(NamedTuple):
    """A warning raised in a worker process, in a form that can be sent over a pipe."""

    message: str
    category: Type[Warning]
    filename: str
    lineno: int


class Task:
    """Wrapped task that trap every Exception and return it as an
    ErrorFromWorker object, and capture warnings so that the parent process can
    re-emit them.

    We are using a wrapper class instead of a decorator since the class
    is pickleable, while a decorator with an inner closure is not.
    """

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs) -> Tuple[Any, List[WarningRecord]]:
        with warnings.catch_warnings(record=True) as recorded:
            # Report every warning, and let the parent process decide what to deduplicate
            warnings.simplefilter("always")
            try:
                value = self.func(*args, **kwargs)
            except Exception:
                value = ErrorFromWorker(*sys.exc_info())
        return value, [
            WarningRecord(str(w.message), w.category, w.filename, w.lineno) for w in recorded
        ]


def imap_unordered(
    f,
    list_of_args,
    *,
    processes: int,
    maxtaskperchild: Optional[int] = None,
    debug=False,
    serialize_env: bool = False,
):
    """Wrapper around multiprocessing.Pool.imap_unordered.

    Args:
        f: function to apply
        list_of_args: list of tuples of args for the task
        processes: maximum number of processes allowed
        debug: if False, raise an exception containing just the error messages
            from workers, if True an exception with complete stacktraces
        maxtaskperchild: number of tasks to be executed by a child before being
            killed and substituted

    Warnings raised in the worker processes are re-emitted here, so that they are formatted by
    this process' ``showwarning`` hook and deduplicated across workers.

    Raises:
        RuntimeError: if any error occurred in the worker processes
    """

    if not ENABLE_PARALLELISM or len(list_of_args) <= 1:
        yield from map(f, list_of_args)
        return

    from spack.subprocess_context import GlobalStateMarshaler

    marshaler = GlobalStateMarshaler(serialize_env=serialize_env)
    # A single registry, so a warning raised by every worker is shown once
    registry: Dict[Any, Any] = {}
    with multiprocessing.Pool(
        processes, initializer=marshaler.restore, maxtasksperchild=maxtaskperchild
    ) as p:
        for result, recorded in p.imap_unordered(Task(f), list_of_args):
            for record in recorded:
                warnings.warn_explicit(
                    record.message,
                    record.category,
                    record.filename,
                    record.lineno,
                    registry=registry,
                )
            if isinstance(result, ErrorFromWorker):
                raise RuntimeError(result.stacktrace if debug else str(result))
            yield result


class SequentialExecutor(concurrent.futures.Executor):
    """Executor that runs tasks sequentially in the current thread."""

    def submit(self, fn, *args, **kwargs):
        """Submit a function to be executed."""
        future = concurrent.futures.Future()
        try:
            future.set_result(fn(*args, **kwargs))
        except Exception as e:
            future.set_exception(e)
        return future


def make_concurrent_executor(
    jobs: Optional[int] = None, *, serialize_env: bool = False
) -> concurrent.futures.Executor:
    """Create a concurrent executor.

    If serialize_env is False (default), the active Spack environment is not transmitted to the
    worker processes, which avoids the cost of pickling potentially large environment state."""

    if not ENABLE_PARALLELISM or sys.version_info[:2] == (3, 6):
        return SequentialExecutor()

    from spack.subprocess_context import GlobalStateMarshaler

    jobs = jobs or min(cpus_available(), 16)
    marshaler = GlobalStateMarshaler(serialize_env=serialize_env)
    return concurrent.futures.ProcessPoolExecutor(jobs, initializer=marshaler.restore)  # novermin
