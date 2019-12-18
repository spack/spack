# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# TODO: Debug erroneous/failing (install) tests: 16 failed, 1 error
# TODO: Add unit tests

# TODO: Change Installer to process multiple (explicit) package installs
# TODO:    at once (instead of one)

""" This module encapsulates package installer functionality. """

import glob
import heapq
import os
import shutil
import sys
import time

from itertools import count
from six import StringIO

import llnl.util.lock as lk
import llnl.util.tty as tty
import spack.binary_distribution as binary_distribution
import spack.compilers
import spack.hooks
import spack.package
import spack.repo
import spack.store

from llnl.util.filesystem import \
    chgrp, install, install_tree, mkdirp, touch, working_dir
from llnl.util.tty.color import colorize, cwrite
from llnl.util.tty.log import log_output
from spack.package_prefs import get_package_dir_permissions, get_package_group
from spack.util.environment import dump_environment
from spack.util.executable import which


#: Counter to support unique spec sequencing that is used to ensure packages
#: with the same priority are (initially) processed in the order in which they
#: were added (see https://docs.python.org/2/library/heapq.html).
_counter = count(0)

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


# TODO: Should the following be static methods?  If so, of which class?
# TODO: If static, which class: package or installer?
# TODO: Or keep as module functions as described in:
# TODO:   https://www.webucator.com/blog/2016/05/\
# TODO:       when-to-use-static-methods-in-python-never/
# TODO: Or "..a class with a lot of static methods might just be better off as
# TODO:    a module with top-level functions." in
# TODO:   https://frasertweedale.github.io/blog-redhat/posts/\
# TODO:       2019-02-07-staticmethod-considered-beneficial.html


def _check_install_locally(pkg, explicit):
    """
    Determine if the package is to be installed locally, registering any
    external package in the database in the process.

    Args:
        pkg (Package): the package whose installation is under consideration
        explicit (bool): the package was explicitly requested by the user
    Return:
        (bool): ``True`` if the package is to be installed locally, otherwise,
            ``False``
    """
    # For external packages the workflow is simplified, and basically
    # consists in module file generation and registration in the DB.
    if pkg.spec.external:
        _process_external_package(pkg, explicit)
        return False

    if pkg.installed_upstream:
        tty.verbose('{0} is installed in an upstream Spack instance at {1}'
                    .format(pkg.unique_name, pkg.spec.prefix))
        _print_installed_pkg(pkg.prefix)

        # This will result in skipping all post-install hooks. In the case
        # of modules this is considered correct because we want to retrieve
        # the module from the upstream Spack instance.
        return False

    return True


def _do_fake_install(pkg):
    """
    Make a fake install directory containing fake executables, headers,
    and libraries.

    Args:
        pkg (PackageBase): the package whose installation is to be faked

    Return:
    """

    command = pkg.name
    header = pkg.name
    library = pkg.name

    # Avoid double 'lib' for packages whose names already start with lib
    if not pkg.name.startswith('lib'):
        library = 'lib' + library

    dso_suffix = '.dylib' if sys.platform == 'darwin' else '.so'
    chmod = which('chmod')

    # Install fake command
    mkdirp(pkg.prefix.bin)
    touch(os.path.join(pkg.prefix.bin, command))
    chmod('+x', os.path.join(pkg.prefix.bin, command))

    # Install fake header file
    mkdirp(pkg.prefix.include)
    touch(os.path.join(pkg.prefix.include, header + '.h'))

    # Install fake shared and static libraries
    mkdirp(pkg.prefix.lib)
    for suffix in [dso_suffix, '.a']:
        touch(os.path.join(pkg.prefix.lib, library + suffix))

    # Install fake man page
    mkdirp(pkg.prefix.man.man1)

    packages_dir = spack.store.layout.build_packages_path(pkg.spec)
    dump_packages(pkg.spec, packages_dir)


def _get_bootstrap_compilers(pkg):
    """
    Retrieve uninstalled compilers

    Checks Spack's compiler configuration for a compiler that
    matches the package spec. If none are configured, installs and
    adds to the compiler configuration the compiler matching the
    CompilerSpec object.

    Args:
        pkg (Package): the package that may need its compiler installed

    Return:
        (list) list of tuples, (PackageBase, bool), for concretized
            compiler-related packages that need to be installed and bool
            values specify whether the package is the bootstrap compiler
            (``True``) or one of its dependencies (``False``)
    """
    tty.debug('Bootstrapping {0} compiler for {1}'
              .format(pkg.spec.compiler, pkg.unique_id))
    compilers = spack.compilers.compilers_for_spec(
        pkg.spec.compiler, arch_spec=pkg.spec.architecture)
    if not compilers:
        dep = spack.compilers.pkg_spec_for_compiler(pkg.spec.compiler)
        dep.architecture = pkg.spec.architecture
        # concrete CompilerSpec has less info than concrete Spec
        # concretize as Spec to add that information
        dep.concretize()
        packages = [(s.package, False) for
                    s in dep.traverse(order='post', root=False)]
        packages.append((dep.package, True))
        return packages

    return []


def _hms(seconds):
    """
    Convert seconds to hours, minutes, seconds

    Args:
        seconds (int): time to be converted in seconds

    Return:
        (str) String representation of the time as #h #m #.##fs
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    parts = []
    if h:
        parts.append("%dh" % h)
    if m:
        parts.append("%dm" % m)
    if s:
        parts.append("%.2fs" % s)
    return ' '.join(parts)


def _installed_from_cache(pkg, cache_only, explicit):
    """
    Install the package from binary cache

    Args:
        pkg (PackageBase): the package to install from the binary cache
        cache_only (bool): only install from binary cache
        explicit (bool): ``True`` if installing the package was explicitly
            requested by the user, otherwise, ``False``

    Return:
        (bool) ``True`` if the package was installed from binary cache,
            ``False`` otherwise
    """
    if _try_install_from_binary_cache(pkg, explicit):
        tty.debug('Successfully installed {0} from binary cache'
                  .format(pkg.unique_id))
        _print_installed_pkg(pkg.spec.prefix)
        spack.hooks.post_install(pkg.spec)
        return True
    elif cache_only:
        tty.die('No binary for {0} found when cache-only specified'
                .format(pkg.unique_id))

    tty.debug('No binary for {0} found: installing from source'
              .format(pkg.unique_id))
    return False


def _print_installed_pkg(message):
    """
    Output a message with a package icon.

    Args:
        message (str): message to be output
    """
    cwrite('@*g{[+]} ')
    print(message)


def _process_external_package(pkg, explicit):
    """
    Helper function to run post install hooks and register external packages.

    Args:
        pkg (Package): the external package
        explicit (bool): if the package was requested explicitly by the user,
            ``False`` if it was pulled in as a dependency of an explicit
            package.
    """
    # TODO: Should this error out?
    if not pkg.spec.external:
        return

    pre = '{s.name}@{s.version} :'.format(s=pkg.spec)
    spec = pkg.spec

    if spec.external_module:
        tty.msg('{0} has external module in {1}'
                .format(pre, spec.external_module))
        tty.msg('{0} is actually installed in {1}'
                .format(pre, spec.external_path))
    else:
        tty.msg("{0} externally installed in {1}"
                .format(pre, spec.external_path))

    try:
        # Check if the package was already registered in the DB.
        # If this is the case, then just exit.
        rec = spack.store.db.get_record(spec)
        tty.msg('{0} already registered in DB'.format(pre))

        # Update the value of rec.explicit if it is necessary
        _update_explicit_entry_in_db(pkg, rec, explicit)

    except KeyError:
        # If not, register it and generate the module file.
        # For external packages we just need to run
        # post-install hooks to generate module files.
        tty.msg('{0} generating module file'.format(pre))
        spack.hooks.post_install(spec)

        # Add to the DB
        tty.msg('{0} registering into DB'.format(pre))
        spack.store.db.add(spec, None, explicit=explicit)


def _try_install_from_binary_cache(pkg, explicit):
    """
    Try to install the package from binary cache.

    Args:
        pkg (PackageBase): the package to be installed from binary cache
        explicit (bool): the package was explicitly requested by the user
    """
    tty.debug('Searching for binary cache of {0}'.format(pkg.unique_id))
    specs = binary_distribution.get_specs()
    binary_spec = spack.spec.Spec.from_dict(pkg.spec.to_dict())
    binary_spec._mark_concrete()
    if binary_spec not in specs:
        return False

    tarball = binary_distribution.download_tarball(binary_spec)
    # see #10063 : install from source if tarball doesn't exist
    if tarball is None:
        tty.msg('{0} exists in binary cache but with different hash'
                .format(pkg.name))
        return False

    tty.msg('Installing {0} from binary cache'.format(pkg.unique_id))
    binary_distribution.extract_tarball(
        binary_spec, tarball, allow_root=False,
        unsigned=False, force=False)
    pkg.installed_from_binary_cache = True
    spack.store.db.add(pkg.spec, spack.store.layout, explicit=explicit)
    return True


def _update_explicit_entry_in_db(pkg, rec, explicit):
    """
    Ensure the spec is marked explicit in the database.

    Args:
        pkg (Package): the package whose install record is being updated
        rec (InstallRecord): the external package
        explicit (bool): if the package was requested explicitly by the user,
            ``False`` if it was pulled in as a dependency of an explicit
            package.
    """
    if explicit and not rec.explicit:
        with spack.store.db.write_transaction():
            rec = spack.store.db.get_record(pkg.spec)
            message = '{s.name}@{s.version} : marking the package explicit'
            tty.msg(message.format(s=pkg.spec))
            rec.explicit = True


def dump_packages(spec, path):
    """
    Dump all package information for a spec and its dependencies.

    This creates a package repository within path for every namespace in the
    spec DAG, and fills the repos wtih package files and patch files for every
    node in the DAG.

    Args:
        spec (Spec): the Spack spec whose package information is to be dumped
        path (str): the path to the build packages directory
    """
    mkdirp(path)

    # Copy in package.py files from any dependencies.
    # Note that we copy them in as they are in the *install* directory
    # NOT as they are in the repository, because we want a snapshot of
    # how *this* particular build was done.
    for node in spec.traverse(deptype=all):
        if node is not spec:
            # Locate the dependency package in the install tree and find
            # its provenance information.
            source = spack.store.layout.build_packages_path(node)
            source_repo_root = os.path.join(source, node.namespace)

            # There's no provenance installed for the source package.  Skip it.
            # User can always get something current from the builtin repo.
            if not os.path.isdir(source_repo_root):
                continue

            # Create a source repo and get the pkg directory out of it.
            try:
                source_repo = spack.repo.Repo(source_repo_root)
                source_pkg_dir = source_repo.dirname_for_package_name(
                    node.name)
            except spack.repo.RepoError:
                tty.warn("Warning: Couldn't copy in provenance for {0}"
                         .format(node.name))

        # Create a destination repository
        dest_repo_root = os.path.join(path, node.namespace)
        if not os.path.exists(dest_repo_root):
            spack.repo.create_repo(dest_repo_root)
        repo = spack.repo.Repo(dest_repo_root)

        # Get the location of the package in the dest repo.
        dest_pkg_dir = repo.dirname_for_package_name(node.name)
        if node is not spec:
            install_tree(source_pkg_dir, dest_pkg_dir)
        else:
            spack.repo.path.dump_provenance(node, dest_pkg_dir)


def get_install_msg(name):
    """
    Colorize the name/id of the package being installed

    Args:
        name (str): Name/id of the package being installed

    Return:
        (str) Colorized installing message
    """
    return colorize('@*{Installing} @*g{%s}' % name)


def log(pkg):
    """
    Copy provenance into the install directory on success

    Args:
        pkg (Package): the package to be installed and built
    """
    packages_dir = spack.store.layout.build_packages_path(pkg.spec)

    # Remove first if we're overwriting another build
    # (can happen with spack setup)
    try:
        # log and env install paths are inside this
        shutil.rmtree(packages_dir)
    except Exception as e:
        # FIXME : this potentially catches too many things...
        tty.debug(e)

    # Archive the whole stdout + stderr for the package
    install(pkg.log_path, pkg.install_log_path)

    # Archive the environment used for the build
    install(pkg.env_path, pkg.install_env_path)

    # Finally, archive files that are specific to each package
    with working_dir(pkg.stage.path):
        errors = StringIO()
        target_dir = os.path.join(
            spack.store.layout.metadata_path(pkg.spec), 'archived-files')

        for glob_expr in pkg.archive_files:
            # Check that we are trying to copy things that are
            # in the stage tree (not arbitrary files)
            abs_expr = os.path.realpath(glob_expr)
            if os.path.realpath(pkg.stage.path) not in abs_expr:
                errors.write('[OUTSIDE SOURCE PATH]: {0}\n'.format(glob_expr))
                continue
            # Now that we are sure that the path is within the correct
            # folder, make it relative and check for matches
            if os.path.isabs(glob_expr):
                glob_expr = os.path.relpath(glob_expr, pkg.stage.path)
            files = glob.glob(glob_expr)
            for f in files:
                try:
                    target = os.path.join(target_dir, f)
                    # We must ensure that the directory exists before
                    # copying a file in
                    mkdirp(os.path.dirname(target))
                    install(f, target)
                except Exception as e:
                    tty.debug(e)

                    # Here try to be conservative, and avoid discarding
                    # the whole install procedure because of copying a
                    # single file failed
                    errors.write('[FAILED TO ARCHIVE]: {0}'.format(f))

        if errors.getvalue():
            error_file = os.path.join(target_dir, 'errors.txt')
            mkdirp(target_dir)
            with open(error_file, 'w') as err:
                err.write(errors.getvalue())
            tty.warn('Errors occurred when archiving files.\n\t'
                     'See: {0}'.format(error_file))

    dump_packages(pkg.spec, packages_dir)


install_args_docstring = """
            cache_only (bool): Fail if binary package unavailable.
            dirty (bool): Don't clean the build environment before installing.
            explicit (bool): True if package was explicitly installed, False
                if package was implicitly installed (as a dependency).
            fake (bool): Don't really build; install fake stub files instead.
            force (bool): Install again, even if already installed.
            install_deps (bool): Install dependencies before installing this
                package
            install_source (bool): By default, source is not installed, but
                for debugging it might be useful to keep it around.
            keep_prefix (bool): Keep install prefix on failure. By default,
                destroys it.
            keep_stage (bool): By default, stage is destroyed only if there
                are no exceptions during build. Set to True to keep the stage
                even with exceptions.
            restage (bool): Force spack to restage the package source.
            skip_patch (bool): Skip patch stage of build if True.
            stop_at (InstallPhase): last installation phase to be executed
                (or None)
            tests (bool or list or set): False to run no tests, True to test
                all packages, or a list of package names to run tests for some
            use_cache (bool): Install from binary package, if available.
            verbose (bool): Display verbose build output (by default,
                suppresses it)
        """


class PackageInstaller(object):
    '''
    Class for managing distributed builds based on bottom-up DAG
    processing.
    '''

    # TODO: Eventually change to support a list of packages
    # TODO: Should the install kwargs dictionary be passed in here?
    def __init__(self, pkg):
        """
        Initialize and set up the build specs.

        Args:
            pkg (PackageBase): the package being installed, whose spec is
                concrete

        Return:
            (PackageInstaller) instance
        """
        if isinstance(pkg, spack.package.PackageBase):
            if not pkg.spec.concrete:
                raise ValueError("{0} must have a concrete spec"
                                 .format(pkg.spec.name))
        else:
            raise ValueError("{0} must be a package".format(str(pkg)))

        # Spec of the package to be built
        self.pkg = pkg

        # Priority queue of build tasks
        self.build_pq = []

        # Mapping of unique package ids to build task
        self.build_tasks = {}

        # Cache of package locks for failed packages, keyed on package's ids
        self.failed = {}

        # Cache of installed packages' unique ids
        self.installed = set()

        # Data store layout
        self.layout = spack.store.layout

        # Locks on specs being built, keyed on the package's unique id
        self.locks = {}

    def _add_bootstrap_compilers(self, pkg):
        """
        Add bootstrap compilers and dependencies to the build queue.

        Args:
            pkg (PackageBase): the package with possible compiler dependencies
        """
        compilers = _get_bootstrap_compilers(pkg)
        for (comp, is_compiler) in compilers:
            comp_pkg = comp.package
            if comp_pkg.unique_id not in self.build_tasks:
                self._push_task(comp_pkg, is_compiler, 0, 0, STATUS_ADDED)

    def _check_install_artifacts(self, task, keep_prefix, keep_stage,
                                 restage=False):
        """
        Check the database and leftover installation directories/files and
        prepare for a new install attempt.

        Args:
            pkg (PackageBase): the package being installed
            keep_prefix (bool): ``True`` if the prefix is to be kept on
                failure, otherwise ``False``
            keep_stage (bool): ``True`` if the stage is to be kept even if
                there are exceptions, otherwise ``False``
            restage (bool): ``True`` if forcing Spack to restage the package
                source, otherwise ``False``
        """
        # Make sure the package is ready to be locally installed.
        self._ensure_install_ready(task.pkg)

        # Skip file system operations if we've already gone through them for
        # this spec.
        if task.pkg.unique_id in self.installed:
            # Already determined the spec has been installed
            return

        # Determine if the spec is flagged as installed in the database
        try:
            rec = spack.store.db.get_record(task.pkg.spec)
            installed_in_db = rec.installed if rec else False
        except KeyError:
            rec = None
            installed_in_db = False

        # Make sure the installation directory is in the desired state
        # for uninstalled specs.
        partial = False
        if not installed_in_db and os.path.isdir(task.pkg.spec.prefix):
            if not keep_prefix:
                task.pkg.remove_prefix()
            else:
                tty.debug('{0} is partially installed'
                          .format(task.pkg.unique_id))
                partial = True

        # Destroy the stage for a locally installed, non-DIYStage, package
        if restage and task.pkg.stage.managed_by_spack:
            task.pkg.stage.destroy()

        if not partial and self.layout.check_installed(task.pkg.spec):
            self._update_installed(task)

            # Only update the explicit entry once for the explicit package
            if task.pkg.unique_id == self.pkg.unique_id:
                _update_explicit_entry_in_db(task.pkg, rec, True)

            # In case the stage directory has already been created, this
            # check ensures it is removed after we checked that the spec is
            # installed.
            if not keep_stage:
                task.pkg.stage.destroy()

    def _check_last_phase(self, **kwargs):
        """
        Ensures the package being installed has a valid last phase before
        proceeding with the installation.

        The ``stop_at`` argument is removed from the installation arguments.

        Args:
            kwargs:
              ``stop_at``': last installation phase to be executed (or None)
        """
        self.pkg.last_phase = kwargs.pop('stop_at', None)
        if self.pkg.last_phase is not None and \
                self.pkg.last_phase not in self.pkg.phases:
            tty.die('\'{0}\' is not an allowed phase for package {1}'
                    .format(self.pkg.last_phase, self.pkg.name))

    def _cleanup_all_tasks(self):
        """Cleanup all build tasks to include releasing their locks."""
        for pkg_id in self.locks:
            self._release_lock(pkg_id)

        for pkg_id in self.failed:
            self._cleanup_failed(pkg_id)

        ids = list(self.build_tasks.keys())
        for pkg_id in ids:
            try:
                self._remove_task(pkg_id)
            except Exception:
                pass

    def _cleanup_failed(self, pkg_id):
        """
        Cleanup any failed mark for the package

        Args:
            pkg_id (str): identifier for the failed package
        """
        if pkg_id in self.failed:
            lock = self.failed[pkg_id]
            if lock is not None:
                err = "{0} exception when removing failure mark for {1}: {2}"
                msg = 'Removing failure mark on {0}'
                try:
                    tty.verbose(msg.format(pkg_id))
                    lock.release_write()
                except AssertionError:
                    pass
                except Exception as exc:
                    tty.warn(err.format(exc.__class__.__name__, pkg_id,
                                        str(exc)))

    def _cleanup_task(self, pkg, remove_task):
        """
        Cleanup the build task for the spec

        Args:
            pkg (PackageBase): the package being installed
            remove_task (bool): ``True`` if the build task should be removed
        """
        if remove_task:
            self._remove_task(pkg.unique_id)

        # Ensure we have a read lock to prevent others from uninstalling the
        # spec during our installation.
        self._ensure_read_locked(pkg)

    def _ensure_install_ready(self, pkg):
        """
        Ensure the package is ready to install locally, which includes
        already locked.

        Args:
            pkg (PackageBase): the package being locally installed
        """
        pre = "{0} cannot be installed locally:".format(pkg.unique_id)

        # External packages cannot be installed locally.
        if pkg.spec.external:
            # TODO: If keep, use a custom exception
            raise spack.error.SpackError('{0} {1}'.format(pre, 'is external'))

        # Upstream packages cannot be installed locally.
        if pkg.installed_upstream:
            # TODO: If keep, use a custom exception
            raise spack.error.SpackError('{0} {1}'.format(pre, 'is upstream'))

        # The package must have a prefix lock at this stage.
        if pkg.unique_id not in self.locks:
            # TODO: If keep, use a custom exception
            raise spack.error.SpackError('{0} {1}'.format(pre, 'not locked'))

    def _ensure_read_locked(self, pkg):
        """
        Add a prefix read lock for the package spec, downgrading from write if
        needed.

        Args:
            pkg (PackageBase): the package whose spec is being installed
        """
        pkg_id = pkg.unique_id
        ltype, lock = self.locks[pkg_id] if pkg_id in self.locks \
            else ('read', None)
        nolock = lock is None
        if nolock or ltype == 'write':
            msg = '{0} a read lock on {1}'
            err = 'Failed to {0} a read lock for {1} due to {2}: {3}'

            try:
                if nolock:
                    tty.verbose(msg.format('Acquiring', pkg_id))
                    op = 'acquire'
                    timeout = spack.store.db.package_lock_timeout
                    lock = spack.store.db.prefix_lock(pkg.spec, timeout)
                    lock.acquire_read()
                else:
                    tty.verbose(msg.format('Downgrading to', pkg_id))
                    op = 'downgrade to'
                    lock.downgrade_write()
                tty.verbose('{0} is now read locked'.format(pkg_id))
            except (lk.LockDowngradeError, lk.LockTimeoutError) as exc:
                tty.debug(err.format(op, pkg_id, exc.__class__.__name__,
                                     str(exc)))
                lock = None
            except (Exception, KeyboardInterrupt, SystemExit) as exc:
                tty.error(err.format(op, pkg_id, exc.__class__.__name__,
                          str(exc)))
                self._cleanup_all_tasks()
                raise

            self.locks[pkg_id] = ('read', lock)

        return 'read', lock

    def _ensure_write_locked(self, pkg):
        """
        Add a prefix write lock for the package's spec, upgrading to write if
        needed.

        The lock timeout is deliberately near zero seconds in order to ensure
        the current process proceeds as quickly as possible to the next spec.

        Args:
            pkg (PackageBase): the package whose spec is being installed
        """
        pkg_id = pkg.unique_id
        ltype, lock = self.locks[pkg_id] if pkg_id in self.locks else \
            ('write', None)
        nolock = lock is None
        if nolock or ltype == 'read':
            msg = '{0} a write lock for {1}'
            err = 'Failed to {0} a write lock for {1} due to {2}: {3}'
            timeout = 1e-9  # Near 0 to iterate through install specs quickly

            try:
                if nolock:
                    tty.verbose(msg.format('Acquiring', pkg_id))
                    res = 'acquire'
                    lock = spack.store.db.prefix_lock(pkg.spec, timeout)
                    lock.acquire_write()
                else:
                    tty.verbose(msg.format('Upgrading to', pkg_id))
                    res = 'upgrade to'
                    lock.upgrade_read(timeout)
                tty.verbose('{0} is now write locked'.format(pkg_id))
            except (lk.LockTimeoutError, lk.LockUpgradeError) as exc:
                tty.debug(err.format(res, pkg_id, exc.__class__.__name__,
                                     str(exc)))
                lock = None
            except (Exception, KeyboardInterrupt, SystemExit) as exc:
                tty.error(err.format(res, pkg_id, exc.__class__.__name__,
                          str(exc)))
                self._cleanup_all_tasks()
                raise

            self.locks[pkg_id] = ('write', lock)

        return 'write', lock

    def _init_queue(self, install_deps, install_self):
        """
        Initialize the build task priority queue and spec state.

        Args:
            install_deps (bool): ``True`` if installing package dependencies,
                otherwise ``False``
            install_self (bool): ``True`` if installing the package, otherwise
                ``False``
        """
        tty.debug('Initializing the build queue for {0}'.format(self.pkg.name))
        install_compilers = spack.config.get(
            'config:install_missing_compilers', False)

        if install_deps:
            for dep in self.spec.traverse(order='post', root=False):
                dep_pkg = dep.package

                # First push any missing compilers (if requested)
                if install_compilers:
                    self._add_bootstrap_compilers(self, dep_pkg)

                if dep_pkg.unique_id not in self.build_tasks:
                    self._push_task(dep_pkg, False, 0, 0, STATUS_ADDED)

                # Clear any persistent failure markings _unless_ they are
                # associated with another process in this parallel build
                # of the spec.
                spack.store.db.clear_failure(dep, force=False)

            # Push any missing compilers (if requested) as part of the
            # package dependencies.
            if install_compilers:
                self._add_bootstrap_compilers(self, self.pkg)

        if install_self and self.pkg.unique_id not in self.build_tasks:
            # Now add the package itself, if appropriate
            self._push_task(self.pkg, False, 0, 0, STATUS_ADDED)

    def _install_task(self, task, **kwargs):
        """
        Perform the installation of the requested spec and or dependency
        represented by the build task.

        Args:
            task (BuildTask): the installation build task for a package"""

        cache_only = kwargs.get('cache_only', False)
        dirty = kwargs.get('dirty', False)
        fake = kwargs.get('fake', False)
        install_source = kwargs.get('install_source', False)
        keep_prefix = kwargs.get('keep_prefix', False)
        keep_stage = kwargs.get('keep_stage', False)
        skip_patch = kwargs.get('skip_patch', False)
        tests = kwargs.get('tests', False)
        use_cache = kwargs.get('use_cache', True)
        verbose = kwargs.get('verbose', False)

        pkg = task.pkg
        explicit = pkg.unique_id == self.pkg.unique_id

        tty.msg(get_install_msg(pkg.unique_id))
        task.start = task.start if task.start else time.time()
        task.status = STATUS_INSTALLING

        # Use the binary cache if requested
        if use_cache:
            if _installed_from_cache(pkg, cache_only, explicit):
                self._update_installed(task)
                return

        pkg.run_tests = (tests is True or tests and pkg.name in tests)

        def build_process():
            """
            This function implements the process forked for each build.

            It has its own process and python module space set up by
            build_environment.fork().

            This function's return value is returned to the parent process.
            """
            start_time = time.time()
            if not fake:
                pass
                if not skip_patch:
                    pkg.do_patch()
                else:
                    pkg.do_stage()

            tty.msg('Building {0} [{1}]'
                    .format(pkg.name, pkg.build_system_class))

            # get verbosity from do_install() parameter or saved value
            echo = verbose
            if spack.package.PackageBase._verbose is not None:
                echo = spack.package.PackageBase._verbose

            pkg.stage.keep = keep_stage

            # parent process already has a prefix write lock
            with pkg.stage:
                # Run the pre-install hook in the child process after
                # the directory is created.
                spack.hooks.pre_install(pkg.spec)
                if fake:
                    _do_fake_install(pkg)
                else:
                    source_path = pkg.stage.source_path
                    if install_source and os.path.isdir(source_path):
                        src_target = os.path.join(pkg.spec.prefix, 'share',
                                                  pkg.name, 'src')
                        tty.msg('Copying source to {0}'.format(src_target))
                        install_tree(pkg.stage.source_path, src_target)

                    # Do the real install in the source directory.
                    with working_dir(pkg.stage.source_path):
                        # Save the build environment in a file before building.
                        dump_environment(pkg.env_path)

                        # cache debug settings
                        debug_enabled = tty.is_debug()

                        # Spawn a daemon that reads from a pipe and redirects
                        # everything to log_path
                        with log_output(pkg.log_path, echo, True) as logger:
                            for phase_name, phase_attr in zip(
                                    pkg.phases, pkg._InstallPhase_phases):

                                with logger.force_echo():
                                    inner_debug = tty.is_debug()
                                    tty.set_debug(debug_enabled)
                                    tty.msg("Executing phase: '{0}'"
                                            .format(phase_name))
                                    tty.set_debug(inner_debug)

                                # Redirect stdout and stderr to daemon pipe
                                phase = getattr(pkg, phase_attr)
                                phase(pkg.spec, pkg.prefix)

                    echo = logger.echo
                    log(pkg)

                # Run post install hooks before build stage is removed.
                spack.hooks.post_install(pkg.spec)

            # Stop the timer
            pkg._total_time = time.time() - start_time
            build_time = pkg._total_time - pkg._fetch_time

            tty.msg('Successfully installed {0}'.format(pkg.unique_id),
                    'Fetch: {0}.  Build: {1}.  Total: {2}.'
                    .format(_hms(pkg._fetch_time), _hms(build_time),
                            _hms(pkg._total_time)))
            _print_installed_pkg(pkg.prefix)

            # preserve verbosity across runs
            return echo

        # hook that allows tests to inspect the Package before installation
        # see unit_test_check() docs.
        if not pkg.unit_test_check():
            return

        try:
            self._setup_install_dir(pkg)

            # Fork a child to do the actual installation.
            # Preserve verbosity settings across installs.
            spack.package.PackageBase._verbose = spack.build_environment.fork(
                pkg, build_process, dirty=dirty, fake=fake)

            self._update_installed(task)

            # If we installed then we should keep the prefix
            last_phase = getattr(pkg, 'last_phase', None)
            keep_prefix = last_phase is None or keep_prefix

            # Note: PARENT of the build process adds the new package to
            # the database, so that we don't need to re-read from file.
            spack.store.db.add(pkg.spec, spack.store.layout,
                               explicit=explicit)

            # If a compiler, ensure it is added to the configuration
            if task.compiler:
                spack.compilers.add_compilers_to_config(
                    spack.compilers.find_compilers([pkg.spec.prefix]))

            # Perform basic task cleanup for the installed spec to
            # include downgrading the write to a read lock
            self._cleanup_task(pkg, True)

        except StopIteration as e:
            # A StopIteration exception means that do_install was asked to
            # stop early from clients.
            tty.msg(e.message)
            tty.msg('Package stage directory : {0}'
                    .format(pkg.stage.source_path))
            self._cleanup_task(pkg, True)

        except spack.directory_layout.InstallDirectoryAlreadyExistsError:
            tty.warn("Keeping existing install prefix in place.")
            self._cleanup_task(pkg, True)
            # TODO: Does "best effort" installation mean raise exception here?
            raise

        except (Exception, KeyboardInterrupt, SystemExit) as exc:
            err = 'Failed to install {0} due to {1}: {2}'
            tty.error(err.format(pkg.name, exc.__class__.__name__,
                      str(exc)))
            self._cleanup_all_tasks()
            raise

        finally:
            # Remove the install prefix if anything went wrong during install.
            if not keep_prefix:
                pkg.remove_prefix()

            # The subprocess *may* have removed the build stage. Mark it
            # not created so that the next time pkg.stage is invoked, we
            # check the filesystem for it.
            pkg.stage.created = False

    _install_task.__doc__ += install_args_docstring

    def _pop_task(self):
        """
        Remove and return the lowest priority build task.

        Source: Variant of function at docs.python.org/2/library/heapq.html
        """
        while self.build_pq:
            task = heapq.heappop(self.build_pq)[1]
            if task.status != STATUS_REMOVED:
                del self.build_tasks[task.pkg_id]
                return task
        return None

    def _push_task(self, pkg, compiler, start, attempts, status):
        """
        Create and push (or queue) a build task for the package.

        Source: Customization of "add_task" function at
                docs.python.org/2/library/heapq.html
        """
        msg = '{0} a build task for {1} with status {2}'
        pkg_id = pkg.unique_id

        # Ensure do not (re-)queue installed or failed specs.
        if pkg_id in self.installed:
            tty.warn('Refusing to retry installed spec {0}'.format(pkg_id))
            return
        elif pkg_id in self.failed:
            tty.warn('Refusing to retry failed spec {0}'.format(pkg_id))
            return

        # Remove any associated build task since its sequence will change
        self._remove_task(pkg_id)
        desc = 'Queueing' if attempts == 0 else 'Requeueing'
        tty.verbose(msg.format(desc, pkg_id, status))

        # Now add the new task to the queue with a new sequence number to
        # ensure it is the last entry popped with the same priority.  This
        # is necessary in case we are re-queueing a task whose priority
        # was decremented due to the installation of one of its dependencies.
        task = BuildTask(pkg, compiler, start, attempts, status,
                         self.installed)
        self.build_tasks[pkg_id] = task
        heapq.heappush(self.build_pq, (task.key, task))

    def _release_lock(self, pkg_id):
        """
        Release any lock on the package

        Args:
            pkg_id (str): identifier for the package whose lock is be released
        """
        if pkg_id in self.locks:
            err = "{0} exception when releasing {1} lock for {2}: {3}"
            msg = 'Releasing {0} lock on {1}'
            ltype, lock = self.locks[pkg_id]
            if lock is not None:
                try:
                    tty.verbose(msg.format(ltype, pkg_id))
                    if ltype == 'read':
                        lock.release_read()
                    else:
                        lock.release_write()
                except AssertionError:
                    pass
                except Exception as exc:
                    tty.warn(err.format(exc.__class__.__name__, ltype,
                                        pkg_id, str(exc)))

    def _remove_task(self, pkg_id):
        """
        Mark the existing package build task as being removed and return it.
        Raises KeyError if not found.

        Source: Variant of function at docs.python.org/2/library/heapq.html

        Args:
            pkg_id (str): identifier for the package to be removed
        """
        if pkg_id in self.build_tasks:
            tty.verbose('Removing build task for {0} from list'
                        .format(pkg_id))
            task = self.build_tasks.pop(pkg_id)
            task.status = STATUS_REMOVED
            return task
        else:
            return None

    def _requeue_task(self, task):
        """
        Requeues a task that appears to be in progress by another process.

        Args:
            task (BuildTask): the installation build task for a package
        """
        if task.status not in [STATUS_INSTALLED, STATUS_INSTALLING]:
            tty.msg('{0} {1}'.format(get_install_msg(task.pkg.unique_id),
                                     'in progress by another process'))

        start = task.start if task.start else time.time()
        self._push_task(task.pkg, task.compiler, start, task.attempts,
                        STATUS_INSTALLING)

    def _setup_install_dir(self, pkg):
        """
        Create and ensure proper access controls for the install directory.

        Args:
            pkg (Package): the package to be installed and built
        """
        if not os.path.exists(pkg.spec.prefix):
            tty.verbose('Creating the installation directory {0}'
                        .format(pkg.spec.prefix))
            spack.store.layout.create_install_directory(pkg.spec)
        else:
            # Set the proper group for the prefix
            group = get_package_group(pkg.spec)
            if group:
                chgrp(pkg.spec.prefix, group)

            # Set the proper permissions.
            # This has to be done after group because changing groups blows
            # away the sticky group bit on the directory
            mode = os.stat(pkg.spec.prefix).st_mode
            perms = get_package_dir_permissions(pkg.spec)
            if mode != perms:
                os.chmod(pkg.spec.prefix, perms)

            # Ensure the metadata path exists as well
            mkdirp(spack.store.layout.metadata_path(pkg.spec), mode=perms)

    def _update_failed(self, task, mark=False):
        """
        Update the task and transitive dependents as failed; optionally mark
        externally as failed; and remove associated build tasks.

        Args:
            task (BuildTask): the build task for the failed package
            mark (bool): ``True`` if the package and its dependencies are to
                be marked as "failed", otherwise, ``False``
        """
        pkg_id = task.pkg.unique_id
        tty.debug('Flagging {0} as failed'.format(pkg_id))
        if mark:
            self.failed[pkg_id] = spack.store.db.mark_failed(task.spec)
        else:
            self.failed[pkg_id] = None
        task.status = STATUS_FAILED

        for dep_id in task.dependents:
            if dep_id in self.build_tasks:
                tty.warn('Skipping build of {0} since {1} failed'
                         .format(dep_id, pkg_id))
                # Ensure the dependent's uninstalled dependents are
                # up-to-date and their build tasks removed.
                dep_task = self.build_tasks[dep_id]
                self._update_failed(dep_task, mark)
                self._remove_task(dep_id)
            else:
                tty.verbose('No build task for {0} to skip since {1} failed'
                            .format(dep_id, pkg_id))

    def _update_installed(self, task):
        """
        Mark the task's spec as installed and update the dependencies of its
        dependents.

        Args:
            task (BuildTask): the build task for the installed package
        """
        pkg_id = task.pkg.unique_id
        tty.debug('Flagging {0} as installed'.format(pkg_id))

        self.installed.add(pkg_id)
        task.status = STATUS_INSTALLED
        for dep_id in task.dependents:
            tty.debug('Removing {0} from {1}\'s uninstalled dependencies.'
                      .format(pkg_id, dep_id))
            if dep_id in self.build_tasks:
                # Ensure the dependent's uninstalled dependencies are
                # up-to-date.  This will require requeueing the task.
                dep_task = self.build_tasks[dep_id]
                dep_task.flag_installed(self.installed)
                self._push_task(dep_task.pkg, dep_task.compiler,
                                dep_task.start, dep_task.attempts,
                                dep_task.status)
            else:
                tty.debug('{0} has no build task to update for {1}\'s success'
                          .format(dep_id, pkg_id))

    def install(self, **kwargs):
        """
        Install the package and or associated dependencies.

        Args:"""

        install_deps = kwargs.get('install_deps', True)
        keep_prefix = kwargs.get('keep_prefix', False)
        keep_stage = kwargs.get('keep_stage', False)
        restage = kwargs.get('restage', False)

        # install_self defaults True and is popped so that dependencies are
        # always installed regardless of whether the root was installed
        install_self = kwargs.pop('install_package', True)

        # TODO: Should this be first or after package updates?
        # TODO: It was being done AFTER external, upstream, and already
        # TODO:   installed checks in _do_install_pop_kwargs() (i.e., just
        # TODO:   before recursively installing dependencies and or bootstrap
        # TODO:   compiler.
        self._check_last_phase(**kwargs)

        # Skip out early if the spec is not being installed locally (i.e., if
        # external or upstream).
        if not _check_install_locally(self.pkg, True):
            return

        # Initialize the build task queue
        self._init_queue(install_deps, install_self)

        # Proceed with the installation
        while self.build_pq:
            task = self._pop_task()
            if task is None:
                continue

            pkg, spec = task.pkg, task.pkg.spec
            pkg_id = pkg.unique_id
            action = 'Processing' if task.attempts <= 0 else 'Reprocessing'
            tty.verbose('{0} {1}: task={2}'.format(action, pkg_id, task))

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
                          .format(pkg_id, task.uninstalled_deps))
                tty.die('Cannot proceed from {0}: {1} uninstalled dependencies'
                        .format(pkg_id, task.priority))

            # TODO: Add check to ensure no attempt is made to install the pkg
            # TODO: before any of its dependencies?

            # Skip the installation if the spec is not being installed locally
            # (i.e., if external or upstream) BUT flag it as installed since
            # some package likely depends on it.
            if pkg_id != self.pkg.unique_id and \
                    not _check_install_locally(pkg, False):
                self._update_installed(task)
                _print_installed_pkg(pkg.prefix)
                continue

            # Flag a failed spec.  Do not need an (install) prefix lock since
            # assume using a separate (failed) prefix lock file.
            if pkg_id in self.failed or spack.store.db.prefix_failed(spec):
                tty.warn('{0} failed to install'.format(pkg_id))
                self._update_failed(task)
                continue

            # Attempt to get a write lock.  If we can't get the lock then
            # another process is likely (un)installing the spec or has
            # determined the spec has already been installed (though the
            # other process may be hung).
            ltype, lock = self._ensure_write_locked(pkg)
            if lock is None:
                # Attempt to get a read lock instead.  If this fails then
                # another process has a write lock so must be (un)installing
                # the spec (or that process is hung).
                ltype, lock = self._ensure_read_locked(pkg)

            # Requeue the spec if we cannot get at least a read lock so we
            # can check the status presumably established by another process
            # -- failed, installed, or uninstalled -- on the next pass.
            if lock is None:
                self._requeue_task(task)
                continue

            # Determine state of installation artifacts and adjust accordingly.
            self._check_install_artifacts(task, keep_prefix, keep_stage,
                                          restage)

            # Flag an already installed pkg
            if pkg_id in self.installed:
                # Downgrade to a read lock to preclude another processes
                # from uninstalling the pkg until we're done.
                #
                # In the off chance we cannot get a read lock, then another
                # process has probably taken a write lock between our releasing
                # the write and acquiring the read.
                ltype, lock = self._ensure_read_locked(pkg)
                if lock is not None:
                    self._update_installed(task)
                    _print_installed_pkg(pkg.prefix)
                else:
                    # Since we cannot assess their intentions at this point,
                    # requeue the task so we can re-check the status presumably
                    # established by the other process -- failed, installed,
                    # or uninstalled -- on the next pass.
                    self._requeue_task(task)
                continue

            # Having a read lock on an uninstalled pkg may mean another
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

            # Proceed with the installation since this is the only process
            # that can work on the current pkg.
            self._install_task(task, **kwargs)

        # Cleanup, which includes releasing all of the read locks
        self._cleanup_all_tasks()

        # Ensure we report that the status of the original pkg is reported
        if self.pkg.unique_id in self.failed:
            tty.msg('Installation of {0} failed.  Review log for details'
                    .format(self.pkg.unique_id))

    install.__doc__ += install_args_docstring

    # Helper method to "smooth" the transition from the PackageBase class
    @property
    def spec(self):
        """The specification associated with the package."""
        return self.pkg.spec


class BuildTask(object):
    """Class for representing the build task for a package."""

    def __init__(self, pkg, compiler, start, attempts, status, installed):
        """
        Instantiate a build task for a package.

        Args:
            pkg (Package): the package to be installed and built
            compiler (bool): ``True`` if the task is for a bootstrap compiler,
                otherwise, ``False``
            start (int): the initial start time for the package, in seconds
            attempts (int): the number of attempts to install the package
            status (int): the installation status
            installed (list of str): the identifiers of packages that have
                been installed so far
        """

        # Ensure dealing with a package that has a concretized spec
        if isinstance(pkg, spack.package.PackageBase):
            self.pkg = pkg
            if not self.pkg.spec.concrete:
                raise ValueError("{0} must have a concrete spec"
                                 .format(self.pkg.unique_id))
        else:
            raise ValueError("{0} must be a package".format(str(pkg)))

        # Initialize the status to an active state.  The status is used to
        # ensure priority queue invariants when tasks are "removed" from the
        # queue.
        if status != STATUS_REMOVED:
            self.status = status
        else:
            msg = 'Cannot create a build task for {0} with status {1}'
            raise RuntimeError(msg.format(self.spec.name, status))

        # Package is associated with a bootstrap compiler
        self.compiler = compiler

        # The initial start time for processing the spec.
        # TODO: Should this be tied to the status?
        self.start = start

        # Number of times the task has been queued
        self.attempts = attempts + 1

        # Set of dependents
        self.dependents = set(d.package.unique_id for d
                              in self.spec.dependents())

        # Set of dependencies
        #
        # Be consistent wrt use of dependents and dependencies.  That is,
        # if use traverse for transitive dependencies, then must remove
        # transitive dependents on failure.
        self.dependencies = set(d.package.unique_id for d in
                                self.spec.dependencies() if
                                d.package.unique_id != self.pkg.unique_id)

        # List of uninstalled dependencies, which is used to establish
        # the priority of the build task.
        #
        self.uninstalled_deps = set(pkg_id for pkg_id in self.dependencies if
                                    pkg_id not in installed)

        # Ensure the task gets a unique sequence number to preserve the
        # order in which it was added.
        self.sequence = next(_counter)

    def __str__(self):
        """Returns a printable version of the build task."""
        attempts = '#attempts={0}'.format(self.attempts)
        dependents = '#dependents={0}'.format(len(self.dependents))
        dependencies = '#dependencies={0}'.format(len(self.dependencies))
        start = 'start={0}s'.format(self.start)
        status = 'status={0}'.format(self.status)
        return ('(pri={0}, seq={1}, id={2}, {3}, {4}, {5}, {6}, {7})'
                .format(self.priority, self.sequence, self.pkg_id, dependents,
                        dependencies, start, attempts, status))

    def flag_installed(self, installed):
        """
        Ensure the dependency is not considered to still be uninstalled.

        Args:
            installed (list of str): the identifiers of packages that have
                been installed so far
        """
        uninstalled = list(self.uninstalled_deps)
        for pkg_id in uninstalled:
            if pkg_id in installed:
                self.uninstalled_deps.remove(pkg_id)
                tty.debug('{0}: Removed {1} from uninstalled deps list: {2}'
                          .format(self.pkg_id, pkg_id, self.uninstalled_deps))

    @property
    def key(self):
        """The key is the tuple (# uninstalled dependencies, sequence)."""
        return (self.priority, self.sequence)

    @property
    def pkg_id(self):
        """The unique, somewhat readable id of the package being built."""
        return self.pkg.unique_id

    @property
    def priority(self):
        """The priority is based on the remaining uninstalled dependencies."""
        return len(self.uninstalled_deps)

    @property
    def spec(self):
        """The specification associated with the package."""
        return self.pkg.spec
