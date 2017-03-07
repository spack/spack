##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""
This implements a parallel map operation but it can accept more values
than multiprocessing.Pool.apply() can.  For example, apply() will fail
to pickle functions if they're passed indirectly as parameters.
"""
from multiprocessing import Process, Pipe, Semaphore, Value

__all__ = ['spawn', 'parmap', 'Barrier']


def spawn(f):
    def fun(pipe, x):
        pipe.send(f(x))
        pipe.close()
    return fun


def parmap(f, X):
    pipe = [Pipe() for x in X]
    proc = [Process(target=spawn(f), args=(c, x))
            for x, (p, c) in zip(X, pipe)]
    [p.start() for p in proc]
    [p.join() for p in proc]
    return [p.recv() for (p, c) in pipe]


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


class BarrierTimeoutError:
    pass
