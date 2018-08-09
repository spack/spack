##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
"""These tests ensure that our lock works correctly.

This can be run in two ways.

First, it can be run as a node-local test, with a typical invocation like
this::

    spack test lock

You can *also* run it as an MPI program, which allows you to test locks
across nodes.  So, e.g., you can run the test like this::

    mpirun -n 7 spack test lock

And it will test locking correctness among MPI processes.  Ideally, you
want the MPI processes to span across multiple nodes, so, e.g., for SLURM
you might do this::

    srun -N 7 -n 7 -m cyclic spack test lock

You can use this to test whether your shared filesystem properly supports
POSIX reader-writer locking with byte ranges through fcntl.

If you want to test on multiple filesystems, you can modify the
``locations`` list below.  By default it looks like this::

    locations = [
        tempfile.gettempdir(),  # standard tmp directory (potentially local)
        '/nfs/tmp2/%u',         # NFS tmp mount
        '/p/lscratch*/%u'       # Lustre scratch mount
    ]

Add names and paths for your preferred filesystem mounts to test on them;
the tests are parametrized to run on all the filesystems listed in this
dict.  Note that 'tmp' will be skipped for MPI testing, as it is often a
node-local filesystem, and multi-node tests will fail if the locks aren't
actually on a shared filesystem.

"""
import os
import socket
import shutil
import tempfile
import traceback
import glob
import getpass
from contextlib import contextmanager
from multiprocessing import Process, Queue

import pytest

import llnl.util.lock as lk
import llnl.util.multiproc as mp
from llnl.util.filesystem import touch


#
# This test can be run with MPI.  MPI is "enabled" if we can import
# mpi4py and the number of total MPI processes is greater than 1.
# Otherwise it just runs as a node-local test.
#
# NOTE: MPI mode is different from node-local mode in that node-local
# mode will spawn its own test processes, while MPI mode assumes you've
# run this script as a SPMD application.  In MPI mode, no additional
# processes are spawned, and you need to ensure that you mpirun the
# script with enough processes for all the multiproc_test cases below.
#
# If you don't run with enough processes, tests that require more
# processes than you currently have will be skipped.
#
mpi = False
comm = None
try:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    if comm.size > 1:
        mpi = True
except ImportError:
    pass


"""This is a list of filesystem locations to test locks in.  Paths are
expanded so that %u is replaced with the current username. '~' is also
legal and will be expanded to the user's home directory.

Tests are skipped for directories that don't exist, so you'll need to
update this with the locations of NFS, Lustre, and other mounts on your
system.
"""
locations = [
    tempfile.gettempdir(),
    os.path.join('/nfs/tmp2/', getpass.getuser()),
    os.path.join('/p/lscratch*/', getpass.getuser()),
]

"""This is the longest a failed multiproc test will take.
Barriers will time out and raise an exception after this interval.
In MPI mode, barriers don't time out (they hang).  See mpi_multiproc_test.
"""
barrier_timeout = 5

"""This is the lock timeout for expected failures.
This may need to be higher for some filesystems."""
lock_fail_timeout = 0.1


def make_readable(*paths):
    for path in paths:
        mode = 0o555 if os.path.isdir(path) else 0o444
        os.chmod(path, mode)


def make_writable(*paths):
    for path in paths:
        mode = 0o755 if os.path.isdir(path) else 0o744
        os.chmod(path, mode)


@contextmanager
def read_only(*paths):
    modes = [os.stat(p).st_mode for p in paths]
    make_readable(*paths)

    yield

    for path, mode in zip(paths, modes):
        os.chmod(path, mode)


@pytest.fixture(scope='session', params=locations)
def lock_test_directory(request):
    """This fixture causes tests to be executed for many different mounts.

    See the ``locations`` dict above for details.
    """
    return request.param


@pytest.fixture(scope='session')
def lock_dir(lock_test_directory):
    parent = next((p for p in glob.glob(lock_test_directory)
                   if os.path.exists(p) and os.access(p, os.W_OK)), None)
    if not parent:
        # Skip filesystems that don't exist or aren't writable
        pytest.skip("requires filesystem: '%s'" % lock_test_directory)
    elif mpi and parent == tempfile.gettempdir():
        # Skip local tmp test for MPI runs
        pytest.skip("skipping local tmp directory for MPI test.")

    tempdir = None
    if not mpi or comm.rank == 0:
        tempdir = tempfile.mkdtemp(dir=parent)
    if mpi:
        tempdir = comm.bcast(tempdir)

    yield tempdir

    if mpi:
        # rank 0 may get here before others, in which case it'll try to
        # remove the directory while other processes try to re-create the
        # lock.  This will give errno 39: directory not empty.  Use a
        # barrier to ensure everyone is done first.
        comm.barrier()

    if not mpi or comm.rank == 0:
        make_writable(tempdir)
        shutil.rmtree(tempdir)


@pytest.fixture
def private_lock_path(lock_dir):
    """In MPI mode, this is a private lock for each rank in a multiproc test.

    For other modes, it is the same as a shared lock.
    """
    lock_file = os.path.join(lock_dir, 'lockfile')
    if mpi:
        lock_file += '.%s' % comm.rank

    yield lock_file

    if os.path.exists(lock_file):
        make_writable(lock_dir, lock_file)
        os.unlink(lock_file)


@pytest.fixture
def lock_path(lock_dir):
    """This lock is shared among all processes in a multiproc test."""
    lock_file = os.path.join(lock_dir, 'lockfile')

    yield lock_file

    if os.path.exists(lock_file):
        make_writable(lock_dir, lock_file)
        os.unlink(lock_file)


def local_multiproc_test(*functions, **kwargs):
    """Order some processes using simple barrier synchronization."""
    b = mp.Barrier(len(functions), timeout=barrier_timeout)

    args = (b,) + tuple(kwargs.get('extra_args', ()))
    procs = [Process(target=f, args=args, name=f.__name__)
             for f in functions]

    for p in procs:
        p.start()

    for p in procs:
        p.join()

    assert all(p.exitcode == 0 for p in procs)


def mpi_multiproc_test(*functions):
    """SPMD version of multiproc test.

    This needs to be run like so:

           srun spack test lock

    Each process executes its corresponding function.  This is different
    from ``multiproc_test`` above, which spawns the processes. This will
    skip tests if there are too few processes to run them.
    """
    procs = len(functions)
    if procs > comm.size:
        pytest.skip("requires at least %d MPI processes" % procs)

    comm.Barrier()  # barrier before each MPI test

    include = comm.rank < len(functions)
    subcomm = comm.Split(include)

    class subcomm_barrier(object):
        """Stand-in for multiproc barrier for MPI-parallel jobs."""
        def wait(self):
            subcomm.Barrier()

    if include:
        try:
            functions[subcomm.rank](subcomm_barrier())
        except BaseException:
            # aborting is the best we can do for MPI tests without
            # hanging, since we're using MPI barriers. This will fail
            # early and it loses the nice pytest output, but at least it
            # gets use a stacktrace on the processes that failed.
            traceback.print_exc()
            comm.Abort()
    subcomm.Free()

    comm.Barrier()  # barrier after each MPI test.


"""``multiproc_test()`` should be called by tests below.
``multiproc_test()`` will work for either MPI runs or for local runs.
"""
multiproc_test = mpi_multiproc_test if mpi else local_multiproc_test


#
# Process snippets below can be composed into tests.
#
def acquire_write(lock_path, start=0, length=0):
    def fn(barrier):
        lock = lk.Lock(lock_path, start, length)
        lock.acquire_write()  # grab exclusive lock
        barrier.wait()
        barrier.wait()  # hold the lock until timeout in other procs.
    return fn


def acquire_read(lock_path, start=0, length=0):
    def fn(barrier):
        lock = lk.Lock(lock_path, start, length)
        lock.acquire_read()  # grab shared lock
        barrier.wait()
        barrier.wait()  # hold the lock until timeout in other procs.
    return fn


def timeout_write(lock_path, start=0, length=0):
    def fn(barrier):
        lock = lk.Lock(lock_path, start, length)
        barrier.wait()  # wait for lock acquire in first process
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        barrier.wait()
    return fn


def timeout_read(lock_path, start=0, length=0):
    def fn(barrier):
        lock = lk.Lock(lock_path, start, length)
        barrier.wait()  # wait for lock acquire in first process
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(lock_fail_timeout)
        barrier.wait()
    return fn


#
# Test that exclusive locks on other processes time out when an
# exclusive lock is held.
#
def test_write_lock_timeout_on_write(lock_path):
    multiproc_test(
        acquire_write(lock_path),
        timeout_write(lock_path))


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
        timeout_write(lock_path, 10, 1),
        timeout_write(lock_path, 32, 1))


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


def test_read_lock_on_read_only_lockfile(lock_dir, lock_path):
    """read-only directory, read-only lockfile."""
    touch(lock_path)
    with read_only(lock_path, lock_dir):
        lock = lk.Lock(lock_path)

        with lk.ReadTransaction(lock):
            pass

        with pytest.raises(lk.LockROFileError):
            with lk.WriteTransaction(lock):
                pass


def test_read_lock_read_only_dir_writable_lockfile(lock_dir, lock_path):
    """read-only directory, writable lockfile."""
    touch(lock_path)
    with read_only(lock_dir):
        lock = lk.Lock(lock_path)

        with lk.ReadTransaction(lock):
            pass

        with lk.WriteTransaction(lock):
            pass


def test_read_lock_no_lockfile(lock_dir, lock_path):
    """read-only directory, no lockfile (so can't create)."""
    with read_only(lock_dir):
        lock = lk.Lock(lock_path)

        with pytest.raises(lk.CantCreateLockError):
            with lk.ReadTransaction(lock):
                pass

        with pytest.raises(lk.CantCreateLockError):
            with lk.WriteTransaction(lock):
                pass


def test_upgrade_read_to_write(private_lock_path):
    """Test that a read lock can be upgraded to a write lock.

    Note that to upgrade a read lock to a write lock, you have the be the
    only holder of a read lock.  Client code needs to coordinate that for
    shared locks.  For this test, we use a private lock just to test that an
    upgrade is possible.
    """
    # ensure lock file exists the first time, so we open it read-only
    # to begin wtih.
    touch(private_lock_path)

    lock = lk.Lock(private_lock_path)
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


def test_upgrade_read_to_write_fails_with_readonly_file(private_lock_path):
    """Test that read-only file can be read-locked but not write-locked."""
    # ensure lock file exists the first time
    touch(private_lock_path)

    # open it read-only to begin wtih.
    with read_only(private_lock_path):
        lock = lk.Lock(private_lock_path)
        assert lock._reads == 0
        assert lock._writes == 0

        lock.acquire_read()
        assert lock._reads == 1
        assert lock._writes == 0
        assert lock._file.mode == 'r'

        # upgrade to writ here
        with pytest.raises(lk.LockROFileError):
            lock.acquire_write()


#
# Longer test case that ensures locks are reusable. Ordering is
# enforced by barriers throughout -- steps are shown with numbers.
#
def test_complex_acquire_and_release_chain(lock_path):
    def p1(barrier):
        lock = lk.Lock(lock_path)

        lock.acquire_write()
        barrier.wait()  # ---------------------------------------- 1
        # others test timeout
        barrier.wait()  # ---------------------------------------- 2
        lock.release_write()   # release and others acquire read
        barrier.wait()  # ---------------------------------------- 3
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 4
        lock.release_read()
        barrier.wait()  # ---------------------------------------- 5

        # p2 upgrades read to write
        barrier.wait()  # ---------------------------------------- 6
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(lock_fail_timeout)
        barrier.wait()  # ---------------------------------------- 7
        # p2 releases write and read
        barrier.wait()  # ---------------------------------------- 8

        # p3 acquires read
        barrier.wait()  # ---------------------------------------- 9
        # p3 upgrades read to write
        barrier.wait()  # ---------------------------------------- 10
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(lock_fail_timeout)
        barrier.wait()  # ---------------------------------------- 11
        # p3 releases locks
        barrier.wait()  # ---------------------------------------- 12
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 13
        lock.release_read()

    def p2(barrier):
        lock = lk.Lock(lock_path)

        # p1 acquires write
        barrier.wait()  # ---------------------------------------- 1
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(lock_fail_timeout)
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
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(lock_fail_timeout)
        barrier.wait()  # ---------------------------------------- 11
        # p3 releases locks
        barrier.wait()  # ---------------------------------------- 12
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 13
        lock.release_read()

    def p3(barrier):
        lock = lk.Lock(lock_path)

        # p1 acquires write
        barrier.wait()  # ---------------------------------------- 1
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(lock_fail_timeout)
        barrier.wait()  # ---------------------------------------- 2
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 3
        # p1 tests shared read
        barrier.wait()  # ---------------------------------------- 4
        lock.release_read()
        barrier.wait()  # ---------------------------------------- 5

        # p2 upgrades read to write
        barrier.wait()  # ---------------------------------------- 6
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(lock_fail_timeout)
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

    lock = lk.Lock(lock_path)
    vals = {'entered': False, 'exited': False, 'exception': False}
    with lk.ReadTransaction(lock, enter_fn, exit_fn):
        pass

    assert vals['entered']
    assert vals['exited']
    assert not vals['exception']

    vals = {'entered': False, 'exited': False, 'exception': False}
    with lk.WriteTransaction(lock, enter_fn, exit_fn):
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

    lock = lk.Lock(lock_path)

    def do_read_with_exception():
        with lk.ReadTransaction(lock, enter_fn, exit_fn):
            raise Exception()

    def do_write_with_exception():
        with lk.WriteTransaction(lock, enter_fn, exit_fn):
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

    lock = lk.Lock(lock_path)

    vals = {'entered': False, 'exited': False, 'exited_fn': False,
            'exception': False, 'exception_fn': False}
    with lk.ReadTransaction(lock, TestContextManager, exit_fn):
        pass

    assert vals['entered']
    assert vals['exited']
    assert not vals['exception']
    assert vals['exited_fn']
    assert not vals['exception_fn']

    vals = {'entered': False, 'exited': False, 'exited_fn': False,
            'exception': False, 'exception_fn': False}
    with lk.ReadTransaction(lock, TestContextManager):
        pass

    assert vals['entered']
    assert vals['exited']
    assert not vals['exception']
    assert not vals['exited_fn']
    assert not vals['exception_fn']

    vals = {'entered': False, 'exited': False, 'exited_fn': False,
            'exception': False, 'exception_fn': False}
    with lk.WriteTransaction(lock, TestContextManager, exit_fn):
        pass

    assert vals['entered']
    assert vals['exited']
    assert not vals['exception']
    assert vals['exited_fn']
    assert not vals['exception_fn']

    vals = {'entered': False, 'exited': False, 'exited_fn': False,
            'exception': False, 'exception_fn': False}
    with lk.WriteTransaction(lock, TestContextManager):
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

    lock = lk.Lock(lock_path)

    def do_read_with_exception(exit_fn):
        with lk.ReadTransaction(lock, TestContextManager, exit_fn):
            raise Exception()

    def do_write_with_exception(exit_fn):
        with lk.WriteTransaction(lock, TestContextManager, exit_fn):
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


def test_lock_debug_output(lock_path):
    host = socket.getfqdn()

    def p1(barrier, q1, q2):
        # exchange pids
        p1_pid = os.getpid()
        q1.put(p1_pid)
        p2_pid = q2.get()

        # set up lock
        lock = lk.Lock(lock_path, debug=True)

        with lk.WriteTransaction(lock):
            # p1 takes write lock and writes pid/host to file
            barrier.wait()  # ------------------------------------ 1

        assert lock.pid == p1_pid
        assert lock.host == host

        # wait for p2 to verify contents of file
        barrier.wait()  # ---------------------------------------- 2

        # wait for p2 to take a write lock
        barrier.wait()  # ---------------------------------------- 3

        # verify pid/host info again
        with lk.ReadTransaction(lock):
            assert lock.old_pid == p1_pid
            assert lock.old_host == host

            assert lock.pid == p2_pid
            assert lock.host == host

        barrier.wait()  # ---------------------------------------- 4

    def p2(barrier, q1, q2):
        # exchange pids
        p2_pid = os.getpid()
        p1_pid = q1.get()
        q2.put(p2_pid)

        # set up lock
        lock = lk.Lock(lock_path, debug=True)

        # p1 takes write lock and writes pid/host to file
        barrier.wait()  # ---------------------------------------- 1

        # verify that p1 wrote information to lock file
        with lk.ReadTransaction(lock):
            assert lock.pid == p1_pid
            assert lock.host == host

        barrier.wait()  # ---------------------------------------- 2

        # take a write lock on the file and verify pid/host info
        with lk.WriteTransaction(lock):
            assert lock.old_pid == p1_pid
            assert lock.old_host == host

            assert lock.pid == p2_pid
            assert lock.host == host

            barrier.wait()  # ------------------------------------ 3

        # wait for p1 to verify pid/host info
        barrier.wait()  # ---------------------------------------- 4

    q1, q2 = Queue(), Queue()
    local_multiproc_test(p2, p1, extra_args=(q1, q2))


def test_lock_with_no_parent_directory(tmpdir):
    """Make sure locks work even when their parent directory does not exist."""
    with tmpdir.as_cwd():
        lock = lk.Lock('foo/bar/baz/lockfile')
        with lk.WriteTransaction(lock):
            pass


def test_lock_in_current_directory(tmpdir):
    """Make sure locks work even when their parent directory does not exist."""
    with tmpdir.as_cwd():
        # test we can create a lock in the current directory
        lock = lk.Lock('lockfile')
        for i in range(10):
            with lk.ReadTransaction(lock):
                pass
            with lk.WriteTransaction(lock):
                pass

        # and that we can do the same thing after it's already there
        lock = lk.Lock('lockfile')
        for i in range(10):
            with lk.ReadTransaction(lock):
                pass
            with lk.WriteTransaction(lock):
                pass
