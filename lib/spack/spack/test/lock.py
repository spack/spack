##############################################################################
# Copyright (c) 2013-2015, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""
These tests ensure that our lock works correctly.
"""
import unittest
import os
import tempfile
import shutil
from multiprocessing import Process

from llnl.util.lock import *
from llnl.util.filesystem import join_path, touch

from spack.util.multiproc import Barrier

# This is the longest a failed test will take, as the barriers will
# time out and raise an exception.
barrier_timeout = 5


class LockTest(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.lock_path = join_path(self.tempdir, 'lockfile')
        touch(self.lock_path)


    def tearDown(self):
         shutil.rmtree(self.tempdir, ignore_errors=True)


    def multiproc_test(self, *functions):
        """Order some processes using simple barrier synchronization."""
        b = Barrier(len(functions), timeout=barrier_timeout)
        procs = [Process(target=f, args=(b,)) for f in functions]
        for p in procs: p.start()
        for p in procs:
            p.join()
            self.assertEqual(p.exitcode, 0)


    #
    # Process snippets below can be composed into tests.
    #
    def acquire_write(self, barrier):
        lock = Lock(self.lock_path)
        lock.acquire_write()  # grab exclusive lock
        barrier.wait()
        barrier.wait() # hold the lock until exception raises in other procs.

    def acquire_read(self, barrier):
        lock = Lock(self.lock_path)
        lock.acquire_read()  # grab shared lock
        barrier.wait()
        barrier.wait() # hold the lock until exception raises in other procs.

    def timeout_write(self, barrier):
        lock = Lock(self.lock_path)
        barrier.wait() # wait for lock acquire in first process
        self.assertRaises(LockError, lock.acquire_write, 0.1)
        barrier.wait()

    def timeout_read(self, barrier):
        lock = Lock(self.lock_path)
        barrier.wait() # wait for lock acquire in first process
        self.assertRaises(LockError, lock.acquire_read, 0.1)
        barrier.wait()


    #
    # Test that exclusive locks on other processes time out when an
    # exclusive lock is held.
    #
    def test_write_lock_timeout_on_write(self):
        self.multiproc_test(self.acquire_write, self.timeout_write)

    def test_write_lock_timeout_on_write_2(self):
        self.multiproc_test(self.acquire_write, self.timeout_write, self.timeout_write)

    def test_write_lock_timeout_on_write_3(self):
        self.multiproc_test(self.acquire_write, self.timeout_write, self.timeout_write, self.timeout_write)


    #
    # Test that shared locks on other processes time out when an
    # exclusive lock is held.
    #
    def test_read_lock_timeout_on_write(self):
        self.multiproc_test(self.acquire_write, self.timeout_read)

    def test_read_lock_timeout_on_write_2(self):
        self.multiproc_test(self.acquire_write, self.timeout_read, self.timeout_read)

    def test_read_lock_timeout_on_write_3(self):
        self.multiproc_test(self.acquire_write, self.timeout_read, self.timeout_read, self.timeout_read)


    #
    # Test that exclusive locks time out when shared locks are held.
    #
    def test_write_lock_timeout_on_read(self):
        self.multiproc_test(self.acquire_read, self.timeout_write)

    def test_write_lock_timeout_on_read_2(self):
        self.multiproc_test(self.acquire_read, self.timeout_write, self.timeout_write)

    def test_write_lock_timeout_on_read_3(self):
        self.multiproc_test(self.acquire_read, self.timeout_write, self.timeout_write, self.timeout_write)


    #
    # Test that exclusive locks time while lots of shared locks are held.
    #
    def test_write_lock_timeout_with_multiple_readers_2_1(self):
        self.multiproc_test(self.acquire_read, self.acquire_read, self.timeout_write)

    def test_write_lock_timeout_with_multiple_readers_2_2(self):
        self.multiproc_test(self.acquire_read, self.acquire_read, self.timeout_write, self.timeout_write)

    def test_write_lock_timeout_with_multiple_readers_3_1(self):
        self.multiproc_test(self.acquire_read, self.acquire_read, self.acquire_read, self.timeout_write)

    def test_write_lock_timeout_with_multiple_readers_3_2(self):
        self.multiproc_test(self.acquire_read, self.acquire_read, self.acquire_read, self.timeout_write, self.timeout_write)


    #
    # Longer test case that ensures locks are reusable. Ordering is
    # enforced by barriers throughout -- steps are shown with numbers.
    #
    def test_complex_acquire_and_release_chain(self):
        def p1(barrier):
            lock = Lock(self.lock_path)

            lock.acquire_write()
            barrier.wait() # ---------------------------------------- 1
            # others test timeout
            barrier.wait() # ---------------------------------------- 2
            lock.release_write()   # release and others acquire read
            barrier.wait() # ---------------------------------------- 3
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            lock.acquire_read()
            barrier.wait() # ---------------------------------------- 4
            lock.release_read()
            barrier.wait() # ---------------------------------------- 5

            # p2 upgrades read to write
            barrier.wait() # ---------------------------------------- 6
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            self.assertRaises(LockError, lock.acquire_read, 0.1)
            barrier.wait() # ---------------------------------------- 7
            # p2 releases write and read
            barrier.wait() # ---------------------------------------- 8

            # p3 acquires read
            barrier.wait() # ---------------------------------------- 9
            # p3 upgrades read to write
            barrier.wait() # ---------------------------------------- 10
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            self.assertRaises(LockError, lock.acquire_read, 0.1)
            barrier.wait() # ---------------------------------------- 11
            # p3 releases locks
            barrier.wait() # ---------------------------------------- 12
            lock.acquire_read()
            barrier.wait() # ---------------------------------------- 13
            lock.release_read()


        def p2(barrier):
            lock = Lock(self.lock_path)

            # p1 acquires write
            barrier.wait() # ---------------------------------------- 1
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            self.assertRaises(LockError, lock.acquire_read, 0.1)
            barrier.wait() # ---------------------------------------- 2
            lock.acquire_read()
            barrier.wait() # ---------------------------------------- 3
            # p1 tests shared read
            barrier.wait() # ---------------------------------------- 4
            # others release reads
            barrier.wait() # ---------------------------------------- 5

            lock.acquire_write() # upgrade read to write
            barrier.wait() # ---------------------------------------- 6
            # others test timeout
            barrier.wait() # ---------------------------------------- 7
            lock.release_write()  # release read AND write (need both)
            lock.release_read()
            barrier.wait() # ---------------------------------------- 8

            # p3 acquires read
            barrier.wait() # ---------------------------------------- 9
            # p3 upgrades read to write
            barrier.wait() # ---------------------------------------- 10
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            self.assertRaises(LockError, lock.acquire_read, 0.1)
            barrier.wait() # ---------------------------------------- 11
            # p3 releases locks
            barrier.wait() # ---------------------------------------- 12
            lock.acquire_read()
            barrier.wait() # ---------------------------------------- 13
            lock.release_read()


        def p3(barrier):
            lock = Lock(self.lock_path)

            # p1 acquires write
            barrier.wait() # ---------------------------------------- 1
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            self.assertRaises(LockError, lock.acquire_read, 0.1)
            barrier.wait() # ---------------------------------------- 2
            lock.acquire_read()
            barrier.wait() # ---------------------------------------- 3
            # p1 tests shared read
            barrier.wait() # ---------------------------------------- 4
            lock.release_read()
            barrier.wait() # ---------------------------------------- 5

            # p2 upgrades read to write
            barrier.wait() # ---------------------------------------- 6
            self.assertRaises(LockError, lock.acquire_write, 0.1)
            self.assertRaises(LockError, lock.acquire_read, 0.1)
            barrier.wait() # ---------------------------------------- 7
            # p2 releases write & read
            barrier.wait() # ---------------------------------------- 8

            lock.acquire_read()
            barrier.wait() # ---------------------------------------- 9
            lock.acquire_write()
            barrier.wait() # ---------------------------------------- 10
            # others test timeout
            barrier.wait() # ---------------------------------------- 11
            lock.release_read()   # release read AND write in opposite
            lock.release_write()  # order from before on p2
            barrier.wait() # ---------------------------------------- 12
            lock.acquire_read()
            barrier.wait() # ---------------------------------------- 13
            lock.release_read()

        self.multiproc_test(p1, p2, p3)
