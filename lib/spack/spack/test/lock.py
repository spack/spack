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
These tests ensure that our lock works correctly.
"""
import os
import shutil
import tempfile
import unittest
from multiprocessing import Process

from llnl.util.filesystem import join_path, touch
from llnl.util.lock import *
from spack.util.multiproc import Barrier

# This is the longest a failed test will take, as the barriers will
# time out and raise an exception.
barrier_timeout = 5


class LockTest(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.lock_path = join_path(self.tempdir, 'lockfile')

    def tearDown(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def multiproc_test(self, *functions):
        """Order some processes using simple barrier synchronization."""
        b = Barrier(len(functions), timeout=barrier_timeout)
        procs = [Process(target=f, args=(b,)) for f in functions]

        for p in procs:
            p.start()

        for p in procs:
            p.join()
            self.assertEqual(p.exitcode, 0)

    #
    # Process snippets below can be composed into tests.
    #
    def acquire_write(self, start=0, length=0):
        def fn(barrier):
            lock = Lock(self.lock_path, start, length)
            lock.acquire_write()  # grab exclusive lock
            barrier.wait()
            barrier.wait()  # hold the lock until timeout in other procs.
        return fn

    def acquire_read(self, start=0, length=0):
        def fn(barrier):
            lock = Lock(self.lock_path, start, length)
            lock.acquire_read()  # grab shared lock
            barrier.wait()
            barrier.wait()  # hold the lock until timeout in other procs.
        return fn

    def timeout_write(self, start=0, length=0):
        def fn(barrier):
            lock = Lock(self.lock_path, start, length)
            barrier.wait()  # wait for lock acquire in first process
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            barrier.wait()
        return fn

    def timeout_read(self, start=0, length=0):
        def fn(barrier):
            lock = Lock(self.lock_path, start, length)
            barrier.wait()  # wait for lock acquire in first process
            self.assertRaises(LockError, lock.acquire_read, 0.1)
            barrier.wait()
        return fn

    #
    # Test that exclusive locks on other processes time out when an
    # exclusive lock is held.
    #
    def test_write_lock_timeout_on_write(self):
        self.multiproc_test(self.acquire_write(), self.timeout_write())

    def test_write_lock_timeout_on_write_2(self):
        self.multiproc_test(
            self.acquire_write(), self.timeout_write(), self.timeout_write())

    def test_write_lock_timeout_on_write_3(self):
        self.multiproc_test(
            self.acquire_write(), self.timeout_write(), self.timeout_write(),
            self.timeout_write())

    def test_write_lock_timeout_on_write_ranges(self):
        self.multiproc_test(
            self.acquire_write(0, 1), self.timeout_write(0, 1))

    def test_write_lock_timeout_on_write_ranges_2(self):
        self.multiproc_test(
            self.acquire_write(0, 64), self.acquire_write(65, 1),
            self.timeout_write(0, 1), self.timeout_write(63, 1))

    def test_write_lock_timeout_on_write_ranges_3(self):
        self.multiproc_test(
            self.acquire_write(0, 1), self.acquire_write(1, 1),
            self.timeout_write(), self.timeout_write(), self.timeout_write())

    def test_write_lock_timeout_on_write_ranges_4(self):
        self.multiproc_test(
            self.acquire_write(0, 1), self.acquire_write(1, 1),
            self.acquire_write(2, 456), self.acquire_write(500, 64),
            self.timeout_write(), self.timeout_write(), self.timeout_write())

    #
    # Test that shared locks on other processes time out when an
    # exclusive lock is held.
    #
    def test_read_lock_timeout_on_write(self):
        self.multiproc_test(self.acquire_write(), self.timeout_read())

    def test_read_lock_timeout_on_write_2(self):
        self.multiproc_test(
            self.acquire_write(), self.timeout_read(), self.timeout_read())

    def test_read_lock_timeout_on_write_3(self):
        self.multiproc_test(
            self.acquire_write(), self.timeout_read(), self.timeout_read(),
            self.timeout_read())

    def test_read_lock_timeout_on_write_ranges(self):
        """small write lock, read whole file."""
        self.multiproc_test(self.acquire_write(0, 1), self.timeout_read())

    def test_read_lock_timeout_on_write_ranges_2(self):
        """small write lock, small read lock"""
        self.multiproc_test(self.acquire_write(0, 1), self.timeout_read(0, 1))

    def test_read_lock_timeout_on_write_ranges_3(self):
        """two write locks, overlapping read locks"""
        self.multiproc_test(
            self.acquire_write(0, 1), self.acquire_write(64, 128),
            self.timeout_read(0, 1), self.timeout_read(128, 256))

    #
    # Test that exclusive locks time out when shared locks are held.
    #
    def test_write_lock_timeout_on_read(self):
        self.multiproc_test(self.acquire_read(), self.timeout_write())

    def test_write_lock_timeout_on_read_2(self):
        self.multiproc_test(
            self.acquire_read(), self.timeout_write(), self.timeout_write())

    def test_write_lock_timeout_on_read_3(self):
        self.multiproc_test(
            self.acquire_read(), self.timeout_write(), self.timeout_write(),
            self.timeout_write())

    def test_write_lock_timeout_on_read_ranges(self):
        self.multiproc_test(self.acquire_read(0, 1), self.timeout_write())

    def test_write_lock_timeout_on_read_ranges_2(self):
        self.multiproc_test(self.acquire_read(0, 1), self.timeout_write(0, 1))

    def test_write_lock_timeout_on_read_ranges_3(self):
        self.multiproc_test(
            self.acquire_read(0, 1), self.acquire_read(10, 1),
            self.timeout_write(0, 1), self.timeout_write(10, 1))

    def test_write_lock_timeout_on_read_ranges_4(self):
        self.multiproc_test(
            self.acquire_read(0, 64),
            self.timeout_write(10, 1), self.timeout_write(32, 1))

    def test_write_lock_timeout_on_read_ranges_5(self):
        self.multiproc_test(
            self.acquire_read(64, 128),
            self.timeout_write(65, 1), self.timeout_write(127, 1),
            self.timeout_write(90, 10))

    #
    # Test that exclusive locks time while lots of shared locks are held.
    #
    def test_write_lock_timeout_with_multiple_readers_2_1(self):
        self.multiproc_test(
            self.acquire_read(), self.acquire_read(), self.timeout_write())

    def test_write_lock_timeout_with_multiple_readers_2_2(self):
        self.multiproc_test(
            self.acquire_read(), self.acquire_read(), self.timeout_write(),
            self.timeout_write())

    def test_write_lock_timeout_with_multiple_readers_3_1(self):
        self.multiproc_test(
            self.acquire_read(), self.acquire_read(), self.acquire_read(),
            self.timeout_write())

    def test_write_lock_timeout_with_multiple_readers_3_2(self):
        self.multiproc_test(
            self.acquire_read(), self.acquire_read(), self.acquire_read(),
            self.timeout_write(), self.timeout_write())

    def test_write_lock_timeout_with_multiple_readers_2_1_ranges(self):
        self.multiproc_test(
            self.acquire_read(0, 10), self.acquire_read(5, 10),
            self.timeout_write(5, 5))

    def test_write_lock_timeout_with_multiple_readers_2_3_ranges(self):
        self.multiproc_test(
            self.acquire_read(0, 10), self.acquire_read(5, 15),
            self.timeout_write(0, 1), self.timeout_write(11, 3),
            self.timeout_write(7, 1))

    def test_write_lock_timeout_with_multiple_readers_3_1_ranges(self):
        self.multiproc_test(
            self.acquire_read(0, 5), self.acquire_read(5, 5),
            self.acquire_read(10, 5),
            self.timeout_write(0, 15))

    def test_write_lock_timeout_with_multiple_readers_3_2_ranges(self):
        self.multiproc_test(
            self.acquire_read(0, 5), self.acquire_read(5, 5),
            self.acquire_read(10, 5),
            self.timeout_write(3, 10), self.timeout_write(5, 1))

    #
    # Test that read can be upgraded to write.
    #
    def test_upgrade_read_to_write(self):
        # ensure lock file exists the first time, so we open it read-only
        # to begin wtih.
        touch(self.lock_path)

        lock = Lock(self.lock_path)
        self.assertTrue(lock._reads == 0)
        self.assertTrue(lock._writes == 0)

        lock.acquire_read()
        self.assertTrue(lock._reads == 1)
        self.assertTrue(lock._writes == 0)
        self.assertTrue(lock._file.mode == 'r+')

        lock.acquire_write()
        self.assertTrue(lock._reads == 1)
        self.assertTrue(lock._writes == 1)
        self.assertTrue(lock._file.mode == 'r+')

        lock.release_write()
        self.assertTrue(lock._reads == 1)
        self.assertTrue(lock._writes == 0)
        self.assertTrue(lock._file.mode == 'r+')

        lock.release_read()
        self.assertTrue(lock._reads == 0)
        self.assertTrue(lock._writes == 0)
        self.assertTrue(lock._file is None)

    #
    # Test that read-only file can be read-locked but not write-locked.
    #
    def test_upgrade_read_to_write_fails_with_readonly_file(self):
        # ensure lock file exists the first time, so we open it read-only
        # to begin wtih.
        touch(self.lock_path)
        os.chmod(self.lock_path, 0o444)

        lock = Lock(self.lock_path)
        self.assertTrue(lock._reads == 0)
        self.assertTrue(lock._writes == 0)

        lock.acquire_read()
        self.assertTrue(lock._reads == 1)
        self.assertTrue(lock._writes == 0)
        self.assertTrue(lock._file.mode == 'r')

        self.assertRaises(LockError, lock.acquire_write)

    #
    # Longer test case that ensures locks are reusable. Ordering is
    # enforced by barriers throughout -- steps are shown with numbers.
    #
    def test_complex_acquire_and_release_chain(self):
        def p1(barrier):
            lock = Lock(self.lock_path)

            lock.acquire_write()
            barrier.wait()  # ---------------------------------------- 1
            # others test timeout
            barrier.wait()  # ---------------------------------------- 2
            lock.release_write()   # release and others acquire read
            barrier.wait()  # ---------------------------------------- 3
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            lock.acquire_read()
            barrier.wait()  # ---------------------------------------- 4
            lock.release_read()
            barrier.wait()  # ---------------------------------------- 5

            # p2 upgrades read to write
            barrier.wait()  # ---------------------------------------- 6
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            self.assertRaises(LockError, lock.acquire_read, 0.1)
            barrier.wait()  # ---------------------------------------- 7
            # p2 releases write and read
            barrier.wait()  # ---------------------------------------- 8

            # p3 acquires read
            barrier.wait()  # ---------------------------------------- 9
            # p3 upgrades read to write
            barrier.wait()  # ---------------------------------------- 10
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            self.assertRaises(LockError, lock.acquire_read, 0.1)
            barrier.wait()  # ---------------------------------------- 11
            # p3 releases locks
            barrier.wait()  # ---------------------------------------- 12
            lock.acquire_read()
            barrier.wait()  # ---------------------------------------- 13
            lock.release_read()

        def p2(barrier):
            lock = Lock(self.lock_path)

            # p1 acquires write
            barrier.wait()  # ---------------------------------------- 1
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            self.assertRaises(LockError, lock.acquire_read, 0.1)
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
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            self.assertRaises(LockError, lock.acquire_read, 0.1)
            barrier.wait()  # ---------------------------------------- 11
            # p3 releases locks
            barrier.wait()  # ---------------------------------------- 12
            lock.acquire_read()
            barrier.wait()  # ---------------------------------------- 13
            lock.release_read()

        def p3(barrier):
            lock = Lock(self.lock_path)

            # p1 acquires write
            barrier.wait()  # ---------------------------------------- 1
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            self.assertRaises(LockError, lock.acquire_read, 0.1)
            barrier.wait()  # ---------------------------------------- 2
            lock.acquire_read()
            barrier.wait()  # ---------------------------------------- 3
            # p1 tests shared read
            barrier.wait()  # ---------------------------------------- 4
            lock.release_read()
            barrier.wait()  # ---------------------------------------- 5

            # p2 upgrades read to write
            barrier.wait()  # ---------------------------------------- 6
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            self.assertRaises(LockError, lock.acquire_read, 0.1)
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

        self.multiproc_test(p1, p2, p3)

    def test_transaction(self):
        def enter_fn():
            vals['entered'] = True

        def exit_fn(t, v, tb):
            vals['exited'] = True
            vals['exception'] = (t or v or tb)

        lock = Lock(self.lock_path)
        vals = {'entered': False, 'exited': False, 'exception': False}
        with ReadTransaction(lock, enter_fn, exit_fn):
            pass

        self.assertTrue(vals['entered'])
        self.assertTrue(vals['exited'])
        self.assertFalse(vals['exception'])

        vals = {'entered': False, 'exited': False, 'exception': False}
        with WriteTransaction(lock, enter_fn, exit_fn):
            pass

        self.assertTrue(vals['entered'])
        self.assertTrue(vals['exited'])
        self.assertFalse(vals['exception'])

    def test_transaction_with_exception(self):
        def enter_fn():
            vals['entered'] = True

        def exit_fn(t, v, tb):
            vals['exited'] = True
            vals['exception'] = (t or v or tb)

        lock = Lock(self.lock_path)

        def do_read_with_exception():
            with ReadTransaction(lock, enter_fn, exit_fn):
                raise Exception()

        def do_write_with_exception():
            with WriteTransaction(lock, enter_fn, exit_fn):
                raise Exception()

        vals = {'entered': False, 'exited': False, 'exception': False}
        self.assertRaises(Exception, do_read_with_exception)
        self.assertTrue(vals['entered'])
        self.assertTrue(vals['exited'])
        self.assertTrue(vals['exception'])

        vals = {'entered': False, 'exited': False, 'exception': False}
        self.assertRaises(Exception, do_write_with_exception)
        self.assertTrue(vals['entered'])
        self.assertTrue(vals['exited'])
        self.assertTrue(vals['exception'])

    def test_transaction_with_context_manager(self):
        class TestContextManager(object):

            def __enter__(self):
                vals['entered'] = True

            def __exit__(self, t, v, tb):
                vals['exited'] = True
                vals['exception'] = (t or v or tb)

        def exit_fn(t, v, tb):
            vals['exited_fn'] = True
            vals['exception_fn'] = (t or v or tb)

        lock = Lock(self.lock_path)

        vals = {'entered': False, 'exited': False, 'exited_fn': False,
                'exception': False, 'exception_fn': False}
        with ReadTransaction(lock, TestContextManager, exit_fn):
            pass

        self.assertTrue(vals['entered'])
        self.assertTrue(vals['exited'])
        self.assertFalse(vals['exception'])
        self.assertTrue(vals['exited_fn'])
        self.assertFalse(vals['exception_fn'])

        vals = {'entered': False, 'exited': False, 'exited_fn': False,
                'exception': False, 'exception_fn': False}
        with ReadTransaction(lock, TestContextManager):
            pass

        self.assertTrue(vals['entered'])
        self.assertTrue(vals['exited'])
        self.assertFalse(vals['exception'])
        self.assertFalse(vals['exited_fn'])
        self.assertFalse(vals['exception_fn'])

        vals = {'entered': False, 'exited': False, 'exited_fn': False,
                'exception': False, 'exception_fn': False}
        with WriteTransaction(lock, TestContextManager, exit_fn):
            pass

        self.assertTrue(vals['entered'])
        self.assertTrue(vals['exited'])
        self.assertFalse(vals['exception'])
        self.assertTrue(vals['exited_fn'])
        self.assertFalse(vals['exception_fn'])

        vals = {'entered': False, 'exited': False, 'exited_fn': False,
                'exception': False, 'exception_fn': False}
        with WriteTransaction(lock, TestContextManager):
            pass

        self.assertTrue(vals['entered'])
        self.assertTrue(vals['exited'])
        self.assertFalse(vals['exception'])
        self.assertFalse(vals['exited_fn'])
        self.assertFalse(vals['exception_fn'])

    def test_transaction_with_context_manager_and_exception(self):
        class TestContextManager(object):

            def __enter__(self):
                vals['entered'] = True

            def __exit__(self, t, v, tb):
                vals['exited'] = True
                vals['exception'] = (t or v or tb)

        def exit_fn(t, v, tb):
            vals['exited_fn'] = True
            vals['exception_fn'] = (t or v or tb)

        lock = Lock(self.lock_path)

        def do_read_with_exception(exit_fn):
            with ReadTransaction(lock, TestContextManager, exit_fn):
                raise Exception()

        def do_write_with_exception(exit_fn):
            with WriteTransaction(lock, TestContextManager, exit_fn):
                raise Exception()

        vals = {'entered': False, 'exited': False, 'exited_fn': False,
                'exception': False, 'exception_fn': False}
        self.assertRaises(Exception, do_read_with_exception, exit_fn)
        self.assertTrue(vals['entered'])
        self.assertTrue(vals['exited'])
        self.assertTrue(vals['exception'])
        self.assertTrue(vals['exited_fn'])
        self.assertTrue(vals['exception_fn'])

        vals = {'entered': False, 'exited': False, 'exited_fn': False,
                'exception': False, 'exception_fn': False}
        self.assertRaises(Exception, do_read_with_exception, None)
        self.assertTrue(vals['entered'])
        self.assertTrue(vals['exited'])
        self.assertTrue(vals['exception'])
        self.assertFalse(vals['exited_fn'])
        self.assertFalse(vals['exception_fn'])

        vals = {'entered': False, 'exited': False, 'exited_fn': False,
                'exception': False, 'exception_fn': False}
        self.assertRaises(Exception, do_write_with_exception, exit_fn)
        self.assertTrue(vals['entered'])
        self.assertTrue(vals['exited'])
        self.assertTrue(vals['exception'])
        self.assertTrue(vals['exited_fn'])
        self.assertTrue(vals['exception_fn'])

        vals = {'entered': False, 'exited': False, 'exited_fn': False,
                'exception': False, 'exception_fn': False}
        self.assertRaises(Exception, do_write_with_exception, None)
        self.assertTrue(vals['entered'])
        self.assertTrue(vals['exited'])
        self.assertTrue(vals['exception'])
        self.assertFalse(vals['exited_fn'])
        self.assertFalse(vals['exception_fn'])
