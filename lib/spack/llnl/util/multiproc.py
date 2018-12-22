# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This implements a parallel map operation but it can accept more values
than multiprocessing.Pool.apply() can.  For example, apply() will fail
to pickle functions if they're passed indirectly as parameters.
"""
import functools
from multiprocessing import Semaphore, Value

__all__ = ['Barrier']


def deferred(func):
    """Package a function call into something that can be invoked
    at a later moment.

    Args:
        func (callable): callable that must be deferred

    Returns:
        Deferred version of the same function
    """
    @functools.wraps(func)
    def _impl(*args, **kwargs):
        def _deferred_call():
            return func(*args, **kwargs)
        return _deferred_call
    return _impl


def invoke(f):
    return f()


def execute(command_list, executor=map):
    """Execute a list of packaged commands and return their result.

    Args:
        command_list: list of commands to be executed
        executor: object that execute each command. Must have the
            same semantic as ``map``.

    Returns:
        List of results
    """
    return executor(invoke, command_list)


class Barrier:
    """Simple reusable semaphore barrier.

    Python 2.6 doesn't have multiprocessing barriers so we implement this.

    See http://greenteapress.com/semaphores/downey08semaphores.pdf, p. 41.
    """

    def __init__(self, n, timeout=None):
        self.n = n
        self.to = timeout
        self.count = Value('i', 0)
        self.mutex = Semaphore(1)
        self.turnstile1 = Semaphore(0)
        self.turnstile2 = Semaphore(1)

    def wait(self):
        if not self.mutex.acquire(timeout=self.to):
            raise BarrierTimeoutError()
        self.count.value += 1
        if self.count.value == self.n:
            if not self.turnstile2.acquire(timeout=self.to):
                raise BarrierTimeoutError()
            self.turnstile1.release()
        self.mutex.release()

        if not self.turnstile1.acquire(timeout=self.to):
            raise BarrierTimeoutError()
        self.turnstile1.release()

        if not self.mutex.acquire(timeout=self.to):
            raise BarrierTimeoutError()
        self.count.value -= 1
        if self.count.value == 0:
            if not self.turnstile1.acquire(timeout=self.to):
                raise BarrierTimeoutError()
            self.turnstile2.release()
        self.mutex.release()

        if not self.turnstile2.acquire(timeout=self.to):
            raise BarrierTimeoutError()
        self.turnstile2.release()


class BarrierTimeoutError(Exception):
    pass
