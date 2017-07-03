##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
These tests ensure that our lock works correctly.
"""
import os
import shutil
import functools
import tempfile
import traceback
from multiprocessing import Process

import pytest

from llnl.util.filesystem import join_path, touch, mkdirp
from llnl.util.lock import *
from spack.util.multiproc import Barrier


# This is the longest a failed test will take, as the barriers will
# time out and raise an exception.
barrier_timeout = 5


@pytest.fixture()
def lock_path():
    tempdir = tempfile.mkdtemp()
    lock_file = join_path(tempdir, 'lockfile')
    yield lock_file
    shutil.rmtree(tempdir)


def multiproc_test(*functions):
    """Order some processes using simple barrier synchronization."""
    b = Barrier(len(functions), timeout=barrier_timeout)
    procs = [Process(target=f, args=(b,)) for f in functions]

    for p in procs:
        p.start()

    for p in procs:
        p.join()
        assert p.exitcode == 0


#
# Process snippets below can be composed into tests.
#
def acquire_write(lock_path, start=0, length=0):
    def fn(barrier):
        lock = Lock(lock_path, start, length)
        lock.acquire_write()  # grab exclusive lock
        barrier.wait()
        barrier.wait()  # hold the lock until timeout in other procs.
    return fn


def acquire_read(lock_path, start=0, length=0):
    def fn(barrier):
        lock = Lock(lock_path, start, length)
        lock.acquire_read()  # grab shared lock
        barrier.wait()
        barrier.wait()  # hold the lock until timeout in other procs.
    return fn


def timeout_write(lock_path, start=0, length=0):
    def fn(barrier):
        lock = Lock(lock_path, start, length)
        barrier.wait()  # wait for lock acquire in first process
        with pytest.raises(LockError):
            lock.acquire_write(0.1)
        barrier.wait()
    return fn


def timeout_read(lock_path, start=0, length=0):
    def fn(barrier):
        lock = Lock(lock_path, start, length)
        barrier.wait()  # wait for lock acquire in first process
        with pytest.raises(LockError):
            lock.acquire_read(0.1)
        barrier.wait()
    return fn


#
# Test that exclusive locks on other processes time out when an
# exclusive lock is held.
#
def test_write_lock_timeout_on_write(lock_path):
    multiproc_test(acquire_write(lock_path), timeout_write(lock_path))


def test_write_lock_timeout_on_write_2(lock_path):
    multiproc_test(
        acquire_write(lock_path),
        timeout_write(lock_path),
        timeout_write(lock_path))


def test_write_lock_timeout_on_write_3(lock_path):
    multiproc_test(
        acquire_write(lock_path),
        timeout_write(lock_path),
        timeout_write(lock_path),
        timeout_write(lock_path))


def test_write_lock_timeout_on_write_ranges(lock_path):
    multiproc_test(
        acquire_write(lock_path, 0, 1),
        timeout_write(lock_path, 0, 1))


def test_write_lock_timeout_on_write_ranges_2(lock_path):
    multiproc_test(
        acquire_write(lock_path, 0, 64),
        acquire_write(lock_path, 65, 1),
        timeout_write(lock_path, 0, 1),
        timeout_write(lock_path, 63, 1))


def test_write_lock_timeout_on_write_ranges_3(lock_path):
    multiproc_test(
        acquire_write(lock_path, 0, 1),
        acquire_write(lock_path, 1, 1),
        timeout_write(lock_path),
        timeout_write(lock_path),
        timeout_write(lock_path))


def test_write_lock_timeout_on_write_ranges_4(lock_path):
    multiproc_test(
        acquire_write(lock_path, 0, 1),
        acquire_write(lock_path, 1, 1),
        acquire_write(lock_path, 2, 456),
        acquire_write(lock_path, 500, 64),
        timeout_write(lock_path),
        timeout_write(lock_path),
        timeout_write(lock_path))


#
# Test that shared locks on other processes time out when an
# exclusive lock is held.
#
def test_read_lock_timeout_on_write(lock_path):
    multiproc_test(
        acquire_write(lock_path),
        timeout_read(lock_path))


def test_read_lock_timeout_on_write_2(lock_path):
    multiproc_test(
        acquire_write(lock_path),
        timeout_read(lock_path),
        timeout_read(lock_path))


def test_read_lock_timeout_on_write_3(lock_path):
    multiproc_test(
        acquire_write(lock_path),
        timeout_read(lock_path),
        timeout_read(lock_path),
        timeout_read(lock_path))


def test_read_lock_timeout_on_write_ranges(lock_path):
    """small write lock, read whole file."""
    multiproc_test(
        acquire_write(lock_path, 0, 1),
        timeout_read(lock_path))


def test_read_lock_timeout_on_write_ranges_2(lock_path):
    """small write lock, small read lock"""
    multiproc_test(
        acquire_write(lock_path, 0, 1),
        timeout_read(lock_path, 0, 1))


def test_read_lock_timeout_on_write_ranges_3(lock_path):
    """two write locks, overlapping read locks"""
    multiproc_test(
        acquire_write(lock_path, 0, 1),
        acquire_write(lock_path, 64, 128),
        timeout_read(lock_path, 0, 1),
        timeout_read(lock_path, 128, 256))


#
# Test that exclusive locks time out when shared locks are held.
#
def test_write_lock_timeout_on_read(lock_path):
    multiproc_test(
        acquire_read(lock_path),
        timeout_write(lock_path))


def test_write_lock_timeout_on_read_2(lock_path):
    multiproc_test(
        acquire_read(lock_path),
        timeout_write(lock_path),
        timeout_write(lock_path))


def test_write_lock_timeout_on_read_3(lock_path):
    multiproc_test(
        acquire_read(lock_path),
        timeout_write(lock_path),
        timeout_write(lock_path),
        timeout_write(lock_path))


def test_write_lock_timeout_on_read_ranges(lock_path):
    multiproc_test(
        acquire_read(lock_path, 0, 1),
        timeout_write(lock_path))


def test_write_lock_timeout_on_read_ranges_2(lock_path):
    multiproc_test(
        acquire_read(lock_path, 0, 1),
        timeout_write(lock_path, 0, 1))


def test_write_lock_timeout_on_read_ranges_3(lock_path):
    multiproc_test(
        acquire_read(lock_path, 0, 1),
        acquire_read(lock_path, 10, 1),
        timeout_write(lock_path, 0, 1),
        timeout_write(lock_path, 10, 1))


def test_write_lock_timeout_on_read_ranges_4(lock_path):
    multiproc_test(
        acquire_read(lock_path, 0, 64),
        timeout_write(lock_path, 10, 1), timeout_write(lock_path, 32, 1))


def test_write_lock_timeout_on_read_ranges_5(lock_path):
    multiproc_test(
        acquire_read(lock_path, 64, 128),
        timeout_write(lock_path, 65, 1),
        timeout_write(lock_path, 127, 1),
        timeout_write(lock_path, 90, 10))

#
# Test that exclusive locks time while lots of shared locks are held.
#
def test_write_lock_timeout_with_multiple_readers_2_1(lock_path):
    multiproc_test(
        acquire_read(lock_path),
        acquire_read(lock_path),
        timeout_write(lock_path))


def test_write_lock_timeout_with_multiple_readers_2_2(lock_path):
    multiproc_test(
        acquire_read(lock_path),
        acquire_read(lock_path),
        timeout_write(lock_path),
        timeout_write(lock_path))


def test_write_lock_timeout_with_multiple_readers_3_1(lock_path):
    multiproc_test(
        acquire_read(lock_path),
        acquire_read(lock_path),
        acquire_read(lock_path),
        timeout_write(lock_path))


def test_write_lock_timeout_with_multiple_readers_3_2(lock_path):
    multiproc_test(
        acquire_read(lock_path),
        acquire_read(lock_path),
        acquire_read(lock_path),
        timeout_write(lock_path),
        timeout_write(lock_path))


def test_write_lock_timeout_with_multiple_readers_2_1_ranges(lock_path):
    multiproc_test(
        acquire_read(lock_path, 0, 10),
        acquire_read(lock_path, 0.5, 10),
        timeout_write(lock_path, 5, 5))


def test_write_lock_timeout_with_multiple_readers_2_3_ranges(lock_path):
    multiproc_test(
        acquire_read(lock_path, 0, 10),
        acquire_read(lock_path, 5, 15),
        timeout_write(lock_path, 0, 1),
        timeout_write(lock_path, 11, 3),
        timeout_write(lock_path, 7, 1))


def test_write_lock_timeout_with_multiple_readers_3_1_ranges(lock_path):
    multiproc_test(
        acquire_read(lock_path, 0, 5),
        acquire_read(lock_path, 5, 5),
        acquire_read(lock_path, 10, 5),
        timeout_write(lock_path, 0, 15))


def test_write_lock_timeout_with_multiple_readers_3_2_ranges(lock_path):
    multiproc_test(
        acquire_read(lock_path, 0, 5),
        acquire_read(lock_path, 5, 5),
        acquire_read(lock_path, 10, 5),
        timeout_write(lock_path, 3, 10),
        timeout_write(lock_path, 5, 1))


#
# Test that read can be upgraded to write.
#
def test_upgrade_read_to_write(lock_path):
    # ensure lock file exists the first time, so we open it read-only
    # to begin wtih.
    touch(lock_path)

    lock = Lock(lock_path)
    assert lock._reads == 0
    assert lock._writes == 0

    lock.acquire_read()
    assert lock._reads == 1
    assert lock._writes == 0
    assert lock._file.mode == 'r+'

    lock.acquire_write()
    assert lock._reads == 1
    assert lock._writes == 1
    assert lock._file.mode == 'r+'

    lock.release_write()
    assert lock._reads == 1
    assert lock._writes == 0
    assert lock._file.mode == 'r+'

    lock.release_read()
    assert lock._reads == 0
    assert lock._writes == 0
    assert lock._file is None

#
# Test that read-only file can be read-locked but not write-locked.
#
def test_upgrade_read_to_write_fails_with_readonly_file(lock_path):
    # ensure lock file exists the first time, so we open it read-only
    # to begin wtih.
    touch(lock_path)
    os.chmod(lock_path, 0o444)

    lock = Lock(lock_path)
    assert lock._reads == 0
    assert lock._writes == 0

    lock.acquire_read()
    assert lock._reads == 1
    assert lock._writes == 0
    assert lock._file.mode == 'r'

    with pytest.raises(LockError):
        lock.acquire_write()

#
# Longer test case that ensures locks are reusable. Ordering is
# enforced by barriers throughout -- steps are shown with numbers.
#
def test_complex_acquire_and_release_chain(lock_path):
    def p1(barrier):
        lock = Lock(lock_path)

        lock.acquire_write()
        barrier.wait()  # ---------------------------------------- 1
        # others test timeout
        barrier.wait()  # ---------------------------------------- 2
        lock.release_write()   # release and others acquire read
        barrier.wait()  # ---------------------------------------- 3
        with pytest.raises(LockError):
            lock.acquire_write(0.1)
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 4
        lock.release_read()
        barrier.wait()  # ---------------------------------------- 5

        # p2 upgrades read to write
        barrier.wait()  # ---------------------------------------- 6
        with pytest.raises(LockError):
            lock.acquire_write(0.1)
        with pytest.raises(LockError):
            lock.acquire_read(0.1)
        barrier.wait()  # ---------------------------------------- 7
        # p2 releases write and read
        barrier.wait()  # ---------------------------------------- 8

        # p3 acquires read
        barrier.wait()  # ---------------------------------------- 9
        # p3 upgrades read to write
        barrier.wait()  # ---------------------------------------- 10
        with pytest.raises(LockError):
            lock.acquire_write(0.1)
        with pytest.raises(LockError):
            lock.acquire_read(0.1)
        barrier.wait()  # ---------------------------------------- 11
        # p3 releases locks
        barrier.wait()  # ---------------------------------------- 12
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 13
        lock.release_read()

    def p2(barrier):
        lock = Lock(lock_path)

        # p1 acquires write
        barrier.wait()  # ---------------------------------------- 1
        with pytest.raises(LockError):
            lock.acquire_write(0.1)
        with pytest.raises(LockError):
            lock.acquire_read(0.1)
        barrier.wait()  # ---------------------------------------- 2
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 3
        # p1 tests shared read
        barrier.wait()  # ---------------------------------------- 4
        # others release reads
        barrier.wait()  # ---------------------------------------- 5

        lock.acquire_write()  # upgrade read to write
        barrier.wait()  # ---------------------------------------- 6
        # others test timeout
        barrier.wait()  # ---------------------------------------- 7
        lock.release_write()  # release read AND write (need both)
        lock.release_read()
        barrier.wait()  # ---------------------------------------- 8

        # p3 acquires read
        barrier.wait()  # ---------------------------------------- 9
        # p3 upgrades read to write
        barrier.wait()  # ---------------------------------------- 10
        with pytest.raises(LockError):
            lock.acquire_write(0.1)
        with pytest.raises(LockError):
            lock.acquire_read(0.1)
        barrier.wait()  # ---------------------------------------- 11
        # p3 releases locks
        barrier.wait()  # ---------------------------------------- 12
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 13
        lock.release_read()

    def p3(barrier):
        lock = Lock(lock_path)

        # p1 acquires write
        barrier.wait()  # ---------------------------------------- 1
        with pytest.raises(LockError):
            lock.acquire_write(0.1)
        with pytest.raises(LockError):
            lock.acquire_read(0.1)
        barrier.wait()  # ---------------------------------------- 2
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 3
        # p1 tests shared read
        barrier.wait()  # ---------------------------------------- 4
        lock.release_read()
        barrier.wait()  # ---------------------------------------- 5

        # p2 upgrades read to write
        barrier.wait()  # ---------------------------------------- 6
        with pytest.raises(LockError):
            lock.acquire_write(0.1)
        with pytest.raises(LockError):
            lock.acquire_read(0.1)
        barrier.wait()  # ---------------------------------------- 7
        # p2 releases write & read
        barrier.wait()  # ---------------------------------------- 8

        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 9
        lock.acquire_write()
        barrier.wait()  # ---------------------------------------- 10
        # others test timeout
        barrier.wait()  # ---------------------------------------- 11
        lock.release_read()   # release read AND write in opposite
        lock.release_write()  # order from before on p2
        barrier.wait()  # ---------------------------------------- 12
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 13
        lock.release_read()

    multiproc_test(p1, p2, p3)

def test_transaction(lock_path):
    def enter_fn():
        vals['entered'] = True

    def exit_fn(t, v, tb):
        vals['exited'] = True
        vals['exception'] = (t or v or tb)

    lock = Lock(lock_path)
    vals = {'entered': False, 'exited': False, 'exception': False}
    with ReadTransaction(lock, enter_fn, exit_fn):
        pass

    assert vals['entered']
    assert vals['exited']
    assert not vals['exception']

    vals = {'entered': False, 'exited': False, 'exception': False}
    with WriteTransaction(lock, enter_fn, exit_fn):
        pass

    assert vals['entered']
    assert vals['exited']
    assert not vals['exception']

def test_transaction_with_exception(lock_path):
    def enter_fn():
        vals['entered'] = True

    def exit_fn(t, v, tb):
        vals['exited'] = True
        vals['exception'] = (t or v or tb)

    lock = Lock(lock_path)

    def do_read_with_exception():
        with ReadTransaction(lock, enter_fn, exit_fn):
            raise Exception()

    def do_write_with_exception():
        with WriteTransaction(lock, enter_fn, exit_fn):
            raise Exception()

    vals = {'entered': False, 'exited': False, 'exception': False}
    with pytest.raises(Exception):
        do_read_with_exception()
    assert vals['entered']
    assert vals['exited']
    assert vals['exception']

    vals = {'entered': False, 'exited': False, 'exception': False}
    with pytest.raises(Exception):
        do_write_with_exception()
    assert vals['entered']
    assert vals['exited']
    assert vals['exception']

def test_transaction_with_context_manager(lock_path):
    class TestContextManager(object):

        def __enter__(self):
            vals['entered'] = True

        def __exit__(self, t, v, tb):
            vals['exited'] = True
            vals['exception'] = (t or v or tb)

    def exit_fn(t, v, tb):
        vals['exited_fn'] = True
        vals['exception_fn'] = (t or v or tb)

    lock = Lock(lock_path)

    vals = {'entered': False, 'exited': False, 'exited_fn': False,
            'exception': False, 'exception_fn': False}
    with ReadTransaction(lock, TestContextManager, exit_fn):
        pass

    assert vals['entered']
    assert vals['exited']
    assert not vals['exception']
    assert vals['exited_fn']
    assert not vals['exception_fn']

    vals = {'entered': False, 'exited': False, 'exited_fn': False,
            'exception': False, 'exception_fn': False}
    with ReadTransaction(lock, TestContextManager):
        pass

    assert vals['entered']
    assert vals['exited']
    assert not vals['exception']
    assert not vals['exited_fn']
    assert not vals['exception_fn']

    vals = {'entered': False, 'exited': False, 'exited_fn': False,
            'exception': False, 'exception_fn': False}
    with WriteTransaction(lock, TestContextManager, exit_fn):
        pass

    assert vals['entered']
    assert vals['exited']
    assert not vals['exception']
    assert vals['exited_fn']
    assert not vals['exception_fn']

    vals = {'entered': False, 'exited': False, 'exited_fn': False,
            'exception': False, 'exception_fn': False}
    with WriteTransaction(lock, TestContextManager):
        pass

    assert vals['entered']
    assert vals['exited']
    assert not vals['exception']
    assert not vals['exited_fn']
    assert not vals['exception_fn']

def test_transaction_with_context_manager_and_exception(lock_path):
    class TestContextManager(object):
        def __enter__(self):
            vals['entered'] = True

        def __exit__(self, t, v, tb):
            vals['exited'] = True
            vals['exception'] = (t or v or tb)

    def exit_fn(t, v, tb):
        vals['exited_fn'] = True
        vals['exception_fn'] = (t or v or tb)

    lock = Lock(lock_path)

    def do_read_with_exception(exit_fn):
        with ReadTransaction(lock, TestContextManager, exit_fn):
            raise Exception()

    def do_write_with_exception(exit_fn):
        with WriteTransaction(lock, TestContextManager, exit_fn):
            raise Exception()

    vals = {'entered': False, 'exited': False, 'exited_fn': False,
            'exception': False, 'exception_fn': False}
    with pytest.raises(Exception):
        do_read_with_exception(exit_fn)
    assert vals['entered']
    assert vals['exited']
    assert vals['exception']
    assert vals['exited_fn']
    assert vals['exception_fn']

    vals = {'entered': False, 'exited': False, 'exited_fn': False,
            'exception': False, 'exception_fn': False}
    with pytest.raises(Exception):
        do_read_with_exception(None)
    assert vals['entered']
    assert vals['exited']
    assert vals['exception']
    assert not vals['exited_fn']
    assert not vals['exception_fn']

    vals = {'entered': False, 'exited': False, 'exited_fn': False,
            'exception': False, 'exception_fn': False}
    with pytest.raises(Exception):
        do_write_with_exception(exit_fn)
    assert vals['entered']
    assert vals['exited']
    assert vals['exception']
    assert vals['exited_fn']
    assert vals['exception_fn']

    vals = {'entered': False, 'exited': False, 'exited_fn': False,
            'exception': False, 'exception_fn': False}
    with pytest.raises(Exception):
        do_write_with_exception(None)
    assert vals['entered']
    assert vals['exited']
    assert vals['exception']
    assert not vals['exited_fn']
    assert not vals['exception_fn']
