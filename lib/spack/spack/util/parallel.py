# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import print_function

import contextlib
import multiprocessing
import os
import sys
import traceback

import six


class ErrorFromWorker(object):
    """Wrapper class to report an error from a worker process"""
    def __init__(self):
        """Create an error object from an exception raised from
        the worker process.

        The attributes of the process error objects are all strings
        as they are easy to send over a pipe.

        Args:
            exc: exception raised from the worker process
        """
        self.pid = os.getpid()
        exc_cls, exc, tb = sys.exc_info()
        self.error_message = "{0.__name__}: {1!s}".format(exc_cls, exc)
        buffer = six.StringIO()
        traceback.print_tb(tb, file=buffer)
        self.exc_stacktrace = buffer.getvalue()
        buffer.close()

    def __str__(self):
        msg = ("[PID={0.pid}] {0.error_message}\n"
               "TASK STACKTRACE:\n"
               "{0.exc_stacktrace}")
        return msg.format(self)


def raise_if_errors(*results):
    """Analyze results from worker Processes to search for ErrorFromWorker
    objects. If found print all of them and raise an exception.

    Args:
        *results: results from worker processes

    Raise:
        RuntimeError: if ErrorFromWorker objects are in the results
    """
    err_stream = six.StringIO()  # sys.stderr
    errors = [x for x in results if isinstance(x, ErrorFromWorker)]
    if not errors:
        return

    # Report the errors and then raise
    for error in errors:
        print(error, file=err_stream)

    print('[PARENT PROCESS]:', file=err_stream)
    traceback.print_stack(file=err_stream)
    raise RuntimeError('errors occurred in worker processes:\n{0}'.format(err_stream.getvalue()))


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
