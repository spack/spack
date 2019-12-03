#!/usr/bin/env spack-python
#
# TODO: Add the remaining install logic
# TODO: Change from spec name to dag hash since name will no longer be unique
# TODO: Add invariant check to ensure never build spec before dependencies
# TODO: Refine timing, use, and reporting of task status
#
# Inspiration:
# - Todd's skeleton at
#   https://github.com/tgamblin/experiments/blob/master/locks/bottom-up-dag.py
# - Priority Queue notes at
#   https://docs.python.org/2/library/heapq.html

import argparse
import heapq
import os
import time

from datetime import datetime
from itertools import count
from re import search

import llnl.util.tty as tty
import llnl.util.lock as lk
import spack.error
import spack.repo
import spack.store

from llnl.util.filesystem import mkdirp
from llnl.util.tty.color import colorize
# from spack.package import Package
from spack.spec import Spec
# from spack.util.crypto import bit_length


#: Time, in seconds, to mock each build (when testing)
BUILD_TIME = 5

#: Name of spec to fail (when testing)
FAIL_SPEC = ''

#: Build status indicating task has been added.
#: (TODO: Consider using an enumeration.)
STATUS_ADDED = 'queued'
#: Build status indicating the spec failed to install
STATUS_FAILED = 'failed'
#: Build status indicating the spec is being installed (possibly by another
#: process)
STATUS_INSTALLING = 'installing'
#: Build status indicating the spec was sucessfully installed
STATUS_INSTALLED = 'installed'
#: Build status indicating task has been removed (to maintain priority
#: queue invariants).
STATUS_REMOVED = 'dequeued'

#: Time to wait before attempting to retry a concretization process
WAIT_TIME = 5

#: Counter to support unique spec sequencing that is used to ensure packages
#: with the same priority are (initially) processed in the order in which they
#: were added (see https://docs.python.org/2/library/heapq.html).
counter = count(0)


def get_install_msg(name):
    return colorize('@*{Installing} @*g{%s}' % name)


def get_hms():
    return datetime.now().strftime('%H:%M:%S.%f')


# TODO: Remove this function once done with timing/plotting
def get_prefix():
    return '[{0}: {1}]'.format(os.getpid(), get_hms())


def log(msg):
    # TODO: Remove the prefix once done with timing/plotting
    tty.msg('{0} {1}'.format(get_prefix(), msg))


def concretize_spec(spec_name):
    tty.debug('Concretizing {0}'.format(spec_name))
    error_msg = '{0}: Blocked on provider{1}: {2}'
    retry_msg = '{0}: Blocked on lock timeout: will retry in {1} sec'

    prefix = 'PID {0}: {1}'.format(os.getpid(), spec_name)
    spec = None
    pid = os.getpid()
    while True:
        try:
            spec = Spec(spec_name).concretized()
            break
        except lk.LockTimeoutError:
            tty.info(retry_msg.format(prefix, WAIT_TIME))
            time.sleep(WAIT_TIME)
        except spack.repo.UnknownPackageError as err:
            match = search(r'\'.*\' not found', str(err))
            # TODO: Cache is not built consistently in parallel (e.g., on 3 or
            # TODO: more NFS nodes) so needs to be rebuilt by running "spack
            # TODO: spec <pkg>".
            fix = 'Rebuild the cache and try again'
            if match:
                pkg = match.group(0).replace(' not found', '')
                msg = ' for {0}'.format(pkg)
            else:
                msg = ''
            tty.error(error_msg.format(pid, spec_name, msg, fix))
            raise

    return spec

class BuildManager(object):
    '''
    Class for managing distributed builds based on bottom-up DAG
    processing.
    '''

    def __init__(self, spec_name, fake_install):
        """Initialize and set up the build specs."""
        # Spec of the package to be built
        self.spec = concretize_spec(spec_name)
        assert isinstance(self.spec, Spec)

        # Fake installations do not affect the database
        self.fake_install = fake_install

        # Priority queue of unbuilt specs
        self.build_pq = []

        # Mapping of build spec name to build task
        self.build_tasks = {}

        # Cache of packages that have failed to install (with locks)
        self.failed = {}

        # Cache of installed packages
        self.installed = set()

        # Data store layout
        self.layout = spack.store.layout

        # Locks on specs being built, keyed on the spec name
        self.locks = {}

    def _check_install_artifacts(self, spec, keep_prefix, restage=False):
        """
        Check the database and leftover installation directores/files and
        prepare for a new install attempt.
        """
        # A lock on the spec is required at this stage.
        if spec.name not in self.locks:
            # TODO: If keep, use a custom exception
            msg = '{0} must be locked to check for installation artifacts'
            raise spack.error.SpackError(msg.format(spec.name))

        # Skip file system operations if we've already gone through them for
        # this spec.
        if spec.name in self.installed:
            # Already determined the spec has been installed
            return

        # Fake installations do not involve the database
        # TODO: Is this (still) desirable?  Appropriate?
        if self.fake_install:
            if self.layout.check_installed(spec):
                self.installed.add(spec.name)
            return

        # Determine if the spec is flagged as installed in the database
        try:
            record = spack.store.db.get_record(spec)
            installed_in_db = record.installed if record else False
        except KeyError:
            record = None
            installed_in_db = False

        # Make sure the installation directory is in the desired state
        # for uninstalled specs.
        partial = False
        if not installed_in_db and os.path.isdir(spec.prefix):
            if not keep_prefix:
                spack.store.layout.remove_install_directory(spec)
            else:
                log('{0} is partially installed'.format(spec.name))
                partial = True

        # TODO: Need to destroy the stage if requested
        # if restage and self.stage.managed_by_spack:  # (i.e., not DIYStage)
        #     self.stage.destroy()

        if not partial and self.layout.check_installed(spec):
            msg = '{0.name} is already installed in {0.prefix}'
            log(msg.format(spec))

            # TODO: Remove spec if in Package
            if spec == self.spec:
                self._update_explicit_entry_in_db(spec, record, True)

            # In case the stage directory has already been created,
            # this ensures it's removed after we checked that the spec
            # is installed
            # TODO: Need to destroy the stage if requested
            # if not keep_stage:
            #    self.stage.destroy()

    def _cleanup_all_tasks(self):
        """Cleanup all build tasks to include releasing their locks."""
        for spec_name in self.locks:
            self._release_lock(spec_name)

        for spec_name in self.failed:
            self._cleanup_failed(spec_name)

        task_names = list(self.build_tasks.keys())
        for name in task_names:
            try:
                self._remove_task(name)
            except Exception:
                pass

    def _cleanup_failed(self, spec_name):
        """Cleanup any failed mark for the spec."""
        if spec_name in self.failed:
            err = "{0} exception when removing failure mark for {1}: {2}"
            msg = 'Removing failure mark on {0}'
            lock = self.failed[spec_name]
            if lock is not None:
                try:
                    tty.verbose(msg.format(spec_name))
                    lock.release_write()
                except AssertionError:
                    pass
                except Exception as exc:
                    tty.warn(err.format(exc.__class__.__name__, spec_name,
                                        str(exc)))

    def _cleanup_task(self, spec, remove_task):
        """Cleanup the build task for the spec."""
        name = spec.name
        if name in self.installed:
            # TODO: destroy stage if not expected to keep it
            # TODO: update the spec entry in the database
            pass

        if remove_task:
            self._remove_task(name)

        # Ensure we have a read lock to prevent others from uninstalling the
        # spec during our installation.
        self._ensure_read_locked(spec)

    def _ensure_read_locked(self, spec):
        """Add a read lock for the spec, downgrading from write if needed."""
        name = spec.name
        ltype, lock = self.locks[name] if name in self.locks \
            else ('read', None)
        nolock = lock is None
        if nolock or ltype == 'write':
            msg = '{0} a read lock on {1}'
            err = 'Failed to {0} a read lock for {1} due to {2}: {3}'

            try:
                if nolock:
                    tty.debug(msg.format('Acquiring', name))
                    op = 'acquire'
                    timeout = spack.store.db.package_lock_timeout
                    lock = spack.store.db.prefix_lock(spec, timeout)
                    lock.acquire_read()
                else:
                    tty.debug(msg.format('Downgrading to', name))
                    op = 'downgrade to'
                    lock.downgrade_write()
                tty.verbose('{0} is now read locked'.format(name))
            except (lk.LockDowngradeError, lk.LockTimeoutError) as exc:
                tty.debug(err.format(op, spec.name, exc.__class__.__name__,
                                     str(exc)))
                lock = None
            except (Exception, KeyboardInterrupt, SystemExit) as exc:
                tty.error(err.format(op, spec.name, exc.__class__.__name__,
                          str(exc)))
                self._cleanup_all_tasks()
                raise

            self.locks[name] = ('read', lock)

        return 'read', lock

    def _ensure_write_locked(self, spec):
        """Add a write lock for the spec, upgrading to write if needed."""
        name = spec.name
        ltype, lock = self.locks[name] if name in self.locks else \
            ('write', None)
        nolock = lock is None
        if nolock or ltype == 'read':
            msg = '{0} a write lock for {1}'
            err = 'Failed to {0} a write lock for {1} due to {2}: {3}'

            try:
                if nolock:
                    tty.debug(msg.format('Acquiring', name))
                    res = 'acquire'
                    timeout = spack.store.db.package_lock_timeout
                    lock = spack.store.db.prefix_lock(spec, timeout)
                    lock.acquire_write()
                else:
                    tty.debug(msg.format('Upgrading to', name))
                    res = 'upgrade to'
                    lock.upgrade_read()
                tty.verbose('{0} is now write locked'.format(name))
            except (lk.LockTimeoutError, lk.LockUpgradeError) as exc:
                tty.debug(err.format(res, spec.name, exc.__class__.__name__,
                                     str(exc)))
                lock = None
            except (Exception, KeyboardInterrupt, SystemExit) as exc:
                tty.error(err.format(res, spec.name, exc.__class__.__name__,
                          str(exc)))
                self._cleanup_all_tasks()
                raise

            self.locks[name] = ('write', lock)

        return 'write', lock

    def _init_queue(self, install_self):
        """Initialize the build task priority queue."""
        tty.debug('Initializing the build queue for {0}'.format(self.name))
        for spec in self.spec.traverse():
            if spec.name != self.name:
                self._push_task(spec, 0, 0, STATUS_ADDED)

        # TODO/TBD: How should ensuring compilers installed for self.spec
        # TODO/TBD:   fit in when only installing dependencies?  Current
        # TODO/TBD:   process adds before the check.

        if install_self:
            self._push_task(self.spec, 0, 0, STATUS_ADDED)

    def _install_spec(self, task, install_compilers):
        """Setup the installation directory and perform the install."""
        name, spec = task.name, task.spec

        log(get_install_msg(name))
        task.start = task.start if task.start else time.time()
        task.status = STATUS_INSTALLING

        # TODO: Try to use cache if use_cache is True
        # TODO: determine if tests and run self.unit_test_check()

        if install_compilers:
            log('{0} installing bootstrap compiler'.format(name))
            # Package._install_bootstrap_compiler(spec.package, **kwargs)

        try:
            prefix = spec.prefix
            if not os.path.exists(prefix):
                tty.verbose('Creating the installation directory {0}'
                            .format(prefix))
                spack.store.layout.create_install_directory(spec)
            else:
                indir = spack.store.layout.metadata_path(spec)
                tty.verbose('Setting access rights to directory {0}'
                            .format(indir))

                # TODO: Set the group and permissions, and set perms below
                mkdirp(indir)

            tty.verbose('Building {0}'.format(name))

            # TODO: Fork the current build_process
            time.sleep(BUILD_TIME)
            success = False if name == FAIL_SPEC else True

            if success:
                # TODO: Add the entry to the database

                # TODO: Remove the following message
                log('  Build of {0} completed'.format(name))
                self._update_installed(task)

                # Perform basic task cleanup for the installed spec to
                # include downgrading the write to a read lock
                self._cleanup_task(spec, True)
            else:
                # TODO: Remove the following message
                log('  Build of {0} failed'.format(name))
                self._update_failed(task, mark=True)
                spack.store.layout.remove_install_directory(spec)

        except spack.directory_layout.InstallDirectoryAlreadyExistsError:
            tty.warn("Keeping existing install prefix in place.")
            self._cleanup_task(spec, True)
            # TODO: Does "best effort" installation mean raise exception here?
            raise
        except StopIteration as e:
            log(e.message)
            # TODO: log('Package stage directory : {0}'
            # TODO:     .format(self.stage.source_path))
            self._cleanup_task(spec, True)
        except (Exception, KeyboardInterrupt, SystemExit) as exc:
            err = 'Failed to install {0} due to {1}: {2}'
            tty.error(err.format(name, exc.__class__.__name__,
                      str(exc)))
            self._cleanup_all_tasks()
            raise
        finally:
            # TODO: Remove the install prefix
            # TODO: Need to self.stage.created = False?
            pass

    def _pop_task(self):
        """
        Remove and return the lowest priority build task.

        Source: Variant of function at docs.python.org/2/library/heapq.html
        """
        while self.build_pq:
            task = heapq.heappop(self.build_pq)[1]
            if task.status != STATUS_REMOVED:
                del self.build_tasks[task.name]
                return task
        return None

    def _push_task(self, spec, start, attempts, status):
        """
        Create and push (or queue) a build task for the spec.

        Source: Customization of "add_task" function at
                docs.python.org/2/library/heapq.html
        """
        msg = '{0} a build task for {1} with status {2}'
        isspec = isinstance(spec, Spec)
        name  = spec.name if isspec else spec

        # Ensure do not (re-)queue installed or failed specs.
        if name in self.installed:
            tty.warn('Refusing to retry installed spec {0}'.format(name))
            return
        elif name in self.failed:
            tty.warn('Refusing to retry failed spec {0}'.format(name))
            return

        # Remove any associated build task since its sequence will change
        self._remove_task(name)
        desc = 'Queueing' if attempts == 0 else 'Requeueing'
        tty.verbose(msg.format(desc, name, status))

        # Now add the new task to the queue with a new sequence number to
        # ensure it is the last entry popped with the same priority.  This
        # is necessary in case we are re-queueing a task whose priority
        # was decremented due to the installation of one of its dependencies.
        task = BuildTask(spec, start, attempts, status, self.installed)
        self.build_tasks[name] = task
        heapq.heappush(self.build_pq, (task.key, task))

    def _release_lock(self, spec_name):
        """Release any lock on the spec."""
        if spec_name in self.locks:
            err = "{0} exception when releasing {1} lock for {2}: {3}"
            msg = 'Releasing {0} lock on {1}'
            ltype, lock = self.locks[spec_name]
            if lock is not None:
                try:
                    tty.verbose(msg.format(ltype, spec_name))
                    if ltype == 'read':
                        lock.release_read()
                    else:
                        lock.release_write()
                except AssertionError:
                    pass
                except Exception as exc:
                    tty.warn(err.format(exc.__class__.__name__, ltype,
                                        spec_name, str(exc)))

    def _remove_task(self, spec_name):
        """
        Mark the existing spec build task as being removed and return it.
        Raises KeyError if not found.

        Source: Variant of function at docs.python.org/2/library/heapq.html
        """
        if spec_name in self.build_tasks:
            tty.verbose('Removing build task for {0} from list'
                        .format(spec_name))
            task = self.build_tasks.pop(spec_name)
            task.status = STATUS_REMOVED
            return task
        else:
            return None

    def _requeue_task(self, task):
        """
        Requeues a task that appears to be in progress by another process.
        """
        if task.status != STATUS_INSTALLING:
            log('{0} {1}'.format(get_install_msg(task.name),
                                 'in progress by another process'))

        start = task.start if task.start else time.time()
        self._push_task(task.spec, start, task.attempts,
                        STATUS_INSTALLING)

    def _update_explicit_entry_in_db(self, spec, rec, explicit):
        if explicit and not rec.explicit:
            with spack.store.db.write_transaction():
                rec = spack.store.db.get_record(spec)
                rec.explicit = True
                # TODO: Restore message -- assumes in Package -- and remove
                # TODO: spec from args.
                # msg = '{s.name}@{s.version} : marking the package explicit'
                # log(msg.format(s=self))
                msg = '{0} is now marked explicit in the database'
                log(msg.format(spec.name))

    def _update_failed(self, task, mark=False):
        """
        Update the task and transitive dependents as failed; optionally mark
        externally as failed; and remove associated build tasks.
        """
        name = task.name
        tty.debug('Flagging {0} as failed'.format(name))
        if mark:
            self.failed[name] = spack.store.db.mark_failed(task.spec)
        else:
            self.failed[name] = None
        task.status = STATUS_FAILED
        for dep_name in task.dependents:
            if dep_name in self.build_tasks:
                tty.warn('Skipping build of {0} since {1} failed'
                         .format(dep_name, name))
                # Ensure the dependent's uninstalled dependents are
                # up-to-date and their build tasks removed.
                dep_task = self.build_tasks[dep_name]
                self._update_failed(dep_task, mark)
                self._remove_task(dep_name)
            else:
                tty.verbose('No build task for {0} to skip since {1} failed'
                            .format(dep_name, name))
            self._release_lock(dep_name)  # Should not have lock but make sure

        self._release_lock(task.name)

    def _update_installed(self, task):
        """
        Mark the task's spec as installed and update the dependencies of its
        dependents.
        """
        name = task.name
        tty.debug('Flagging {0} as installed'.format(name))
        self.installed.add(name)
        task.status = STATUS_INSTALLED
        for dep_name in task.dependents:
            tty.debug('Removing {0} from {1}\'s uninstalled dependencies.'
                      .format(name, dep_name))
            if dep_name in self.build_tasks:
                # Ensure the dependent's uninstalled dependencies are
                # up-to-date.  This will require requeueing the task.
                dep_task = self.build_tasks[dep_name]
                dep_task.flag_installed(self.installed)
                self._push_task(dep_task.spec, dep_task.start,
                                dep_task.attempts, dep_task.status)
            else:
                tty.debug('{0} has no build task to update for {1}\'s success'
                          .format(dep_name, name))

    def install(self, **kwargs):
        """Install the package and associated dependencies."""
        # TODO: extract relevant arguments from kwargs
        install_self = kwargs.get('install_package', True)

        keep_prefix = kwargs.get('keep_prefix', False)

        # TODO: process external package if external spec and return
        # TODO: warn and return if installed upstream
        # TODO: check and proceed if unfinished installation

        # Initialize the build task queue
        self._init_queue(install_self)

        # Proceed with the installation
        install_compilers = spack.config.get(
            'config:install_missing_compilers', False)

        while self.build_pq:
            task = self._pop_task()
            if task is None:
                continue

            name, spec = task.name, task.spec
            desc = 'Processing' if task.attempts <= 0 else 'Reprocessing'
            tty.verbose('{0} {1}: task={2}'.format(desc, name, task))

            # Ensure that the current spec as NO uninstalled dependencies,
            # which is assumed to be reflected directly in its priority.
            #
            # If the spec has uninstalled dependencies, then there must be
            # a bug in the code (e.g., priority queue or uninstalled
            # dependencies handling).  So terminate under the assumption that
            # all subsequent tasks will have non-zero priorities or may be
            # dependencies of this task.
            if task.priority != 0:
                tty.error('Detected uninstalled dependencies for {0}: {1}'
                          .format(name, task.uninstalled_deps))
                tty.die('Cannot proceed from {0}: {1} uninstalled dependencies'
                        .format(name, task.priority))

            # TODO: Add check to ensure no attempt is made to install the spec
            # TODO: before any of its dependencies.

            # TODO: Should we timeout if a task is taking "too long"?

            # Flag a failed spec.  Do not need an (install) prefix lock since
            # assume using a separate (failed) prefix lock file.
            if name in self.failed or spack.store.db.prefix_failed(spec):
                tty.warn('{0} failed to install'.format(name))
                self._update_failed(task)
                continue

            # Attempt to get a write lock.  If we can't get the lock then
            # another process is likely (un)installing the spec or has
            # determined the spec has already been installed (though the
            # other process may be hung).
            ltype, lock = self._ensure_write_locked(spec)
            if lock is None:
                # Attempt to get a read lock instead.  If this fails then
                # another process has a write lock so must be (un)installing
                # the spec (or that process is hung).
                ltype, lock = self._ensure_read_locked(spec)

            # Requeue the spec if we cannot get at least a read lock so we
            # can check the status presumably established by another process
            # -- failed, installed, or uninstalled -- on the next pass.
            if lock is None:
                self._requeue_task(task)
                continue

            # Determine state of installation artifacts and adjust accordingly.
            restage = False
            self._check_install_artifacts(spec, keep_prefix, restage)

            # TODO: Is it still appropriate to check the 'stop_at' option
            # TODO: for the last phase (and die) here?
            # self._do_install_pop_kwargs(kwargs)

            # Flag an already installed spec
            if name in self.installed:
                # Downgrade to a read lock to preclude another processes
                # from uninstalling the spec until we're done.
                #
                # In the off chance we cannot get a read lock, then another
                # process has probably taken a write lock between our releasing
                # the write and acquiring the read.
                ltype, lock = self._ensure_read_locked(spec)
                if lock is not None:
                    log('{0.name} is installed in {0.prefix}'.format(spec))
                    self._update_installed(task)
                else:
                    # Since we cannot assess their intentions at this point,
                    # requeue the task so we can re-check the status presumably
                    # established by the other process -- failed, installed,
                    # or uninstalled -- on the next pass.
                    self._requeue_task(task)
                continue

            # Having a read lock on an uninstalled spec may mean another
            # process completed an uninstall of the software between the
            # time we failed to acquire the write lock and the time we
            # took the read lock.
            #
            # Requeue the task so we can check the status presumably
            # established by the other process -- failed, installed, or
            # uninstalled -- on the next pass.
            if ltype == 'read':
                self._requeue_task(task)
                continue

            # TODO: What should be checked?  Originally checked prior to
            # TODO: calling "do_install" for each dependency BUT only called
            # TODO: for requested spec if installing dependents.
            if install_compilers:  
                log('{0} installing bootstrap compiler'.format(name))
                # Package._install_bootstrap_compiler(spec.package, **kwargs)

            # Proceed with the installation since this is the only process
            # that can work on the current spec.
            self._install_spec(task, install_compilers)

        # Cleanup, which includes releasing all of the read locks
        self._cleanup_all_tasks()

        # Ensure we report that the status of the original spec is reported
        if self.spec.name in self.failed:
            log('Installation of {0} failed.  Review log for details'
                .format(self.spec.name))

    @property
    def name(self):
        return self.spec.name


class BuildTask(object):
    """Class for representing the build task for a spec."""

    def __init__(self, spec, start, attempts, status, installed):
        # Ensure dealing with a concretized spec
        if isinstance(spec, Spec):
            self.spec = spec
        else:
            if isinstance(spec, str):
                self.spec = concretize_spec(spec)
                assert isinstance(self.spec, Spec)
            else:
                raise ValueError("Can only build concrete specs!")

        # Initialize the status to an active state.  The status is used to
        # ensure priority queue invariants when tasks are "removed" from the
        # queue.
        if status != STATUS_REMOVED:
            self.status = status
        else:
            msg = 'Cannot create a build task for {0} with status {1}'
            raise RuntimeError(msg.format(self.spec.name, status))

        # The initial start time for processing the spec.
        # TODO: Should this be tied to the status?
        self.start = start

        # Number of times the task has been queued
        self.attempts = attempts + 1

        # Set of dependents
        self.dependents = set(s.name for s in spec.dependents())

        # Set of dependencies
        #
        # Be consistent wrt use of dependents and dependencies.  That is,
        # if use traverse for transitive dependencies, then must remove
        # transitive dependents on failure.
        #
        # self.dependencies = set(s.name for s in spec.traverse() if
        self.dependencies = set(s.name for s in spec.dependencies() if
                                s.name != self.spec.name)

        # List of uninstalled dependencies, which is used to establish
        # the priority of the build task.
        #
        self.uninstalled_deps = set(name for name in self.dependencies if
                                    name not in installed)

        # Ensure the task gets a unique sequence number to preserve the
        # order in which it was added.
        self.sequence = next(counter)

    def __str__(self):
        attempts = '#attempts={0}'.format(self.attempts)
        dependents = '#dependents={0}'.format(len(self.dependents))
        dependencies = '#dependencies={0}'.format(len(self.dependencies))
        start = 'start={0}s'.format(self.start)
        status = 'status={0}'.format(self.status)
        return ('(pri={0}, seq={1}, spec={2}, {3}, {4}, {5}, {6}, {7})'
                .format(self.priority, self.sequence, self.name,
                        dependents, dependencies, start, attempts, status))

    def flag_installed(self, installed):
        """Ensure the dependency is not considered to still be uninstalled."""
        uninstalled = list(self.uninstalled_deps)
        for name in uninstalled:
            if name in installed:
                self.uninstalled_deps.remove(name)
                tty.debug('{0}: Removed {1} from uninstalled deps list: {2}'
                          .format(self.name, name, self.uninstalled_deps))

    @property
    def key(self):
        """The key is the tuple (# uninstalled dependencies, sequence)."""
        return (self.priority, self.sequence)

    @property
    def name(self):
        return self.spec.name

    @property
    def priority(self):
        return len(self.uninstalled_deps)


def process_args():
    parser = argparse.ArgumentParser(
        description='Demonstrate distributed, lock-based builds')

    # Options
    parser.add_argument('--build-time', type=int, default=4,  # TODO: 30 is good
                        help='mock build time (sec)')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug log messages')
    parser.add_argument('--fail', type=str, default='',
                        help='name of spec to fail during testing')
    parser.add_argument('--real', action='store_true', default=False,
                        help='attempt an actual installation')
    parser.add_argument('--timeout', type=float, default=1e-9,  # TODO: enough time?
                        help='package lock timeout (sec)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='enable verbose output')

    parser.add_argument('spec', type=str, nargs='+',
                        help='names of one or more packages to build')
    return parser.parse_args()


# -------------------------------- MAIN -------------------------------- #
def main(args):
    """Build the specified package(s)."""
    global BUILD_TIME
    global FAIL_SPEC

    BUILD_TIME = args.build_time
    FAIL_SPEC = args.fail

    tty.set_verbose(args.verbose)
    tty.set_debug(args.debug)

    spack.store.db.package_lock_timeout = args.timeout

    pid = os.getpid()
    for spec_name in args.spec:
        log('PID {0}: Began processing {1}'.format(pid, spec_name))
        mgr = BuildManager(spec_name, not args.real)
        mgr.install()


if __name__ == "__main__":
    start = time.time()
    main(process_args())
    print('\n%s: Processing time: %.2gs' % (os.getpid(), time.time() - start))
