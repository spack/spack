# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import print_function

import contextlib
import multiprocessing
import os
import sys
import traceback

from .cpus import cpus_available


class ErrorFromWorker(object):
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
        self.stacktrace_message = ''.join(traceback.format_exception(exc_cls, exc, tb))

    @property
    def stacktrace(self):
        msg = "[PID={0.pid}] {0.stacktrace_message}"
        return msg.format(self)

    def __str__(self):
        return self.error_message


class Task(object):
    """Wrapped task that trap every Exception and return it as an
    ErrorFromWorker object.

    We are using a wrapper class instead of a decorator since the class
    is pickleable, while a decorator with an inner closure is not.
    """
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            value = self.func(*args, **kwargs)
        except Exception:
            value = ErrorFromWorker(*sys.exc_info())
        return value


def raise_if_errors(*results, **kwargs):
    """Analyze results from worker Processes to search for ErrorFromWorker
    objects. If found print all of them and raise an exception.

    Args:
        *results: results from worker processes
        debug: if True show complete stacktraces

    Raise:
        RuntimeError: if ErrorFromWorker objects are in the results
    """
    debug = kwargs.get('debug', False)  # This can be a keyword only arg in Python 3
    errors = [x for x in results if isinstance(x, ErrorFromWorker)]
    if not errors:
        return

    msg = '\n'.join([
        error.stacktrace if debug else str(error) for error in errors
    ])

    error_fmt = '{0}'
    if len(errors) > 1 and not debug:
        error_fmt = 'errors occurred during concretization of the environment:\n{0}'

    raise RuntimeError(error_fmt.format(msg))


@contextlib.contextmanager
def pool(*args, **kwargs):
    """Context manager to start and terminate a pool of processes, similar to the
    default one provided in Python 3.X

    Arguments are forwarded to the multiprocessing.Pool.__init__ method.
    """
    try:
        p = multiprocessing.Pool(*args, **kwargs)
        yield p
    finally:
        p.terminate()
        p.join()


def num_processes(max_processes=None):
    """Return the number of processes in a pool.

    Currently the function return the minimum between the maximum number
    of processes and the cpus available.

    When a maximum number of processes is not specified return the cpus available.

    Args:
        max_processes (int or None): maximum number of processes allowed
    """
    max_processes or cpus_available()
    return min(cpus_available(), max_processes)


def parallel_map(func, arguments, max_processes=None, debug=False):
    """Map a task object to the list of arguments, return the list of results.

    Args:
        func (Task): user defined task object
        arguments (list): list of arguments for the task
        max_processes (int or None): maximum number of processes allowed
        debug (bool): if False, raise an exception containing just the error messages
            from workers, if True an exception with complete stacktraces

    Raises:
        RuntimeError: if any error occurred in the worker processes
    """
    task_wrapper = Task(func)
    if sys.platform != 'darwin':
        with pool(processes=num_processes(max_processes=max_processes)) as p:
            results = p.map(task_wrapper, arguments)
    else:
        results = list(map(task_wrapper, arguments))
    raise_if_errors(*results, debug=debug)
    return results
