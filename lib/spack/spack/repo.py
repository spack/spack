# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import abc
import contextlib
import errno
import functools
import importlib
import inspect
import itertools
import os
import os.path
import re
import shutil
import stat
import sys
import tempfile
import traceback
import types
from typing import Dict  # novm

import ruamel.yaml as yaml
import six

import llnl.util.filesystem as fs
import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.compat import Mapping

import spack.caches
import spack.config
import spack.error
import spack.patch
import spack.provider_index
import spack.spec
import spack.tag
import spack.util.naming as nm
import spack.util.path

#: Package modules are imported as spack.pkg.<repo-namespace>.<pkg-name>
ROOT_PYTHON_NAMESPACE = 'spack.pkg'


def python_package_for_repo(namespace):
    """Returns the full namespace of a repository, given its relative one

    For instance:

        python_package_for_repo('builtin') == 'spack.pkg.builtin'

    Args:
        namespace (str): repo namespace
    """
    return '{0}.{1}'.format(ROOT_PYTHON_NAMESPACE, namespace)


def namespace_from_fullname(fullname):
    """Return the repository namespace only for the full module name.

    For instance:

        namespace_from_fullname('spack.pkg.builtin.hdf5') == 'builtin'

    Args:
        fullname (str): full name for the Python module
    """
    namespace, dot, module = fullname.rpartition('.')
    prefix_and_dot = '{0}.'.format(ROOT_PYTHON_NAMESPACE)
    if namespace.startswith(prefix_and_dot):
        namespace = namespace[len(prefix_and_dot):]
    return namespace


# The code below is needed to have a uniform Loader interface that could cover both
# Python 2.7 and Python 3.X when we load Spack packages as Python modules, e.g. when
# we do "import spack.pkg.builtin.mpich" in package recipes.
if sys.version_info[0] == 2:
    import imp

    @contextlib.contextmanager
    def import_lock():
        try:
            imp.acquire_lock()
            yield
        finally:
            imp.release_lock()

    def load_source(fullname, path, prepend=None):
        """Import a Python module from source.

        Load the source file and add it to ``sys.modules``.

        Args:
            fullname (str): full name of the module to be loaded
            path (str): path to the file that should be loaded
            prepend (str or None): some optional code to prepend to the
                loaded module; e.g., can be used to inject import statements

        Returns:
            the loaded module
        """
        with import_lock():
            with prepend_open(path, text=prepend) as f:
                return imp.load_source(fullname, path, f)

    @contextlib.contextmanager
    def prepend_open(f, *args, **kwargs):
        """Open a file for reading, but prepend with some text prepended

        Arguments are same as for ``open()``, with one keyword argument,
        ``text``, specifying the text to prepend.

        We have to write and read a tempfile for the ``imp``-based importer,
        as the ``file`` argument to ``imp.load_source()`` requires a
        low-level file handle.

        See the ``importlib``-based importer for a faster way to do this in
        later versions of python.
        """
        text = kwargs.get('text', None)

        with open(f, *args) as f:
            with tempfile.NamedTemporaryFile(mode='w+') as tf:
                if text:
                    tf.write(text + '\n')
                tf.write(f.read())
                tf.seek(0)
                yield tf.file

    class PrependFileLoader(object):
        def __init__(self, fullname, path, prepend=None):
            # Done to have a compatible interface with Python 3
            pass

        def package_module(self):
            try:
                module = load_source(
                    self.fullname, self.package_py, prepend=self._package_prepend
                )
            except SyntaxError as e:
                # SyntaxError strips the path from the filename, so we need to
                # manually construct the error message in order to give the
                # user the correct package.py where the syntax error is located
                msg = 'invalid syntax in {0:}, line {1:}'
                raise SyntaxError(msg.format(self.package_py, e.lineno))

            module.__package__ = self.repo.full_namespace
            module.__loader__ = self
            return module

        def load_module(self, fullname):
            # Compatibility method to support Python 2.7
            if fullname in sys.modules:
                return sys.modules[fullname]

            namespace, dot, module_name = fullname.rpartition('.')

            try:
                module = self.package_module()
            except Exception as e:
                raise ImportError(str(e))

            module.__loader__ = self
            sys.modules[fullname] = module
            if namespace != fullname:
                parent = sys.modules[namespace]
                if not hasattr(parent, module_name):
                    setattr(parent, module_name, module)

            return module

else:
    import importlib.machinery  # novm

    class PrependFileLoader(importlib.machinery.SourceFileLoader):  # novm
        def __init__(self, fullname, path, prepend=None):
            super(PrependFileLoader, self).__init__(fullname, path)
            self.prepend = prepend

        def path_stats(self, path):
            stats = super(PrependFileLoader, self).path_stats(path)
            if self.prepend:
                stats["size"] += len(self.prepend) + 1
            return stats

        def get_data(self, path):
            data = super(PrependFileLoader, self).get_data(path)
            if path != self.path or self.prepend is None:
                return data
            else:
                return self.prepend.encode() + b"\n" + data


class RepoLoader(PrependFileLoader):
    """Loads a Python module associated with a package in specific repository"""
    #: Code in ``_package_prepend`` is prepended to imported packages.
    #:
    #: Spack packages were originally expected to call `from spack import *`
    #: themselves, but it became difficult to manage and imports in the Spack
    #: core the top-level namespace polluted by package symbols this way.  To
    #: solve this, the top-level ``spack`` package contains very few symbols
    #: of its own, and importing ``*`` is essentially a no-op.  The common
    #: routines and directives that packages need are now in ``spack.pkgkit``,
    #: and the import system forces packages to automatically include
    #: this. This way, old packages that call ``from spack import *`` will
    #: continue to work without modification, but it's no longer required.
    _package_prepend = ('from __future__ import absolute_import;'
                        'from spack.pkgkit import *')

    def __init__(self, fullname, repo, package_name):
        self.repo = repo
        self.package_name = package_name
        self.package_py = repo.filename_for_package_name(package_name)
        self.fullname = fullname
        super(RepoLoader, self).__init__(
            self.fullname, self.package_py, prepend=self._package_prepend
        )


class SpackNamespaceLoader(object):
    def create_module(self, spec):
        return SpackNamespace(spec.name)

    def exec_module(self, module):
        module.__loader__ = self

    def load_module(self, fullname):
        # Compatibility method to support Python 2.7
        if fullname in sys.modules:
            return sys.modules[fullname]
        module = SpackNamespace(fullname)
        self.exec_module(module)

        namespace, dot, module_name = fullname.rpartition('.')
        sys.modules[fullname] = module
        if namespace != fullname:
            parent = sys.modules[namespace]
            if not hasattr(parent, module_name):
                setattr(parent, module_name, module)

        return module


class ReposFinder(object):
    """MetaPathFinder class that loads a Python module corresponding to a Spack package

    Return a loader based on the inspection of the current global repository list.
    """
    def find_spec(self, fullname, python_path, target=None):
        # This function is Python 3 only and will not be called by Python 2.7
        import importlib.util

        # "target" is not None only when calling importlib.reload()
        if target is not None:
            raise RuntimeError('cannot reload module "{0}"'.format(fullname))

        # Preferred API from https://peps.python.org/pep-0451/
        if not fullname.startswith(ROOT_PYTHON_NAMESPACE):
            return None

        loader = self.compute_loader(fullname)
        if loader is None:
            return None
        return importlib.util.spec_from_loader(fullname, loader)  # novm

    def compute_loader(self, fullname):
        # namespaces are added to repo, and package modules are leaves.
        namespace, dot, module_name = fullname.rpartition('.')

        # If it's a module in some repo, or if it is the repo's
        # namespace, let the repo handle it.
        for repo in path.repos:
            # We are using the namespace of the repo and the repo contains the package
            if namespace == repo.full_namespace:
                # With 2 nested conditionals we can call "repo.real_name" only once
                package_name = repo.real_name(module_name)
                if package_name:
                    return RepoLoader(fullname, repo, package_name)

            # We are importing a full namespace like 'spack.pkg.builtin'
            if fullname == repo.full_namespace:
                return SpackNamespaceLoader()

        # No repo provides the namespace, but it is a valid prefix of
        # something in the RepoPath.
        if path.by_namespace.is_prefix(fullname):
            return SpackNamespaceLoader()

        return None

    def find_module(self, fullname, python_path=None):
        # Compatibility method to support Python 2.7
        if not fullname.startswith(ROOT_PYTHON_NAMESPACE):
            return None
        return self.compute_loader(fullname)


#
# These names describe how repos should be laid out in the filesystem.
#
repo_config_name   = 'repo.yaml'   # Top-level filename for repo config.
repo_index_name    = 'index.yaml'  # Top-level filename for repository index.
packages_dir_name  = 'packages'    # Top-level repo directory containing pkgs.
package_file_name  = 'package.py'  # Filename for packages in a repository.

#: Guaranteed unused default value for some functions.
NOT_PROVIDED = object()


def autospec(function):
    """Decorator that automatically converts the first argument of a
    function to a Spec.
    """
    @functools.wraps(function)
    def converter(self, spec_like, *args, **kwargs):
        if not isinstance(spec_like, spack.spec.Spec):
            spec_like = spack.spec.Spec(spec_like)
        return function(self, spec_like, *args, **kwargs)
    return converter


def is_package_file(filename):
    """Determine whether we are in a package file from a repo."""
    # Package files are named `package.py` and are not in lib/spack/spack
    # We have to remove the file extension because it can be .py and can be
    # .pyc depending on context, and can differ between the files
    import spack.package  # break cycle
    filename_noext = os.path.splitext(filename)[0]
    packagebase_filename_noext = os.path.splitext(
        inspect.getfile(spack.package.PackageBase))[0]
    return (filename_noext != packagebase_filename_noext and
            os.path.basename(filename_noext) == 'package')


class SpackNamespace(types.ModuleType):
    """ Allow lazy loading of modules."""

    def __init__(self, namespace):
        super(SpackNamespace, self).__init__(namespace)
        self.__file__ = "(spack namespace)"
        self.__path__ = []
        self.__name__ = namespace
        self.__package__ = namespace
        self.__modules = {}

    def __getattr__(self, name):
        """Getattr lazily loads modules if they're not already loaded."""
        submodule = self.__package__ + '.' + name
        try:
            setattr(self, name, __import__(submodule))
        except ImportError:
            msg = "'{0}' object has no attribute {1}"
            raise AttributeError(msg.format(type(self), name))
        return getattr(self, name)


class FastPackageChecker(Mapping):
    """Cache that maps package names to the stats obtained on the
    'package.py' files associated with them.

    For each repository a cache is maintained at class level, and shared among
    all instances referring to it. Update of the global cache is done lazily
    during instance initialization.
    """
    #: Global cache, reused by every instance
    _paths_cache = {}  # type: Dict[str, Dict[str, os.stat_result]]

    def __init__(self, packages_path):
        # The path of the repository managed by this instance
        self.packages_path = packages_path

        # If the cache we need is not there yet, then build it appropriately
        if packages_path not in self._paths_cache:
            self._paths_cache[packages_path] = self._create_new_cache()

        #: Reference to the appropriate entry in the global cache
        self._packages_to_stats = self._paths_cache[packages_path]

    def invalidate(self):
        """Regenerate cache for this checker."""
        self._paths_cache[self.packages_path] = self._create_new_cache()
        self._packages_to_stats = self._paths_cache[self.packages_path]

    def _create_new_cache(self):  # type: () -> Dict[str, os.stat_result]
        """Create a new cache for packages in a repo.

        The implementation here should try to minimize filesystem
        calls.  At the moment, it is O(number of packages) and makes
        about one stat call per package.  This is reasonably fast, and
        avoids actually importing packages in Spack, which is slow.
        """
        # Create a dictionary that will store the mapping between a
        # package name and its stat info
        cache = {}  # type: Dict[str, os.stat_result]
        for pkg_name in os.listdir(self.packages_path):
            # Skip non-directories in the package root.
            pkg_dir = os.path.join(self.packages_path, pkg_name)

            # Warn about invalid names that look like packages.
            if not nm.valid_module_name(pkg_name):
                if not pkg_name.startswith('.'):
                    tty.warn('Skipping package at {0}. "{1}" is not '
                             'a valid Spack module name.'.format(
                                 pkg_dir, pkg_name))
                continue

            # Construct the file name from the directory
            pkg_file = os.path.join(
                self.packages_path, pkg_name, package_file_name
            )

            # Use stat here to avoid lots of calls to the filesystem.
            try:
                sinfo = os.stat(pkg_file)
            except OSError as e:
                if e.errno == errno.ENOENT:
                    # No package.py file here.
                    continue
                elif e.errno == errno.EACCES:
                    tty.warn("Can't read package file %s." % pkg_file)
                    continue
                raise e

            # If it's not a file, skip it.
            if stat.S_ISDIR(sinfo.st_mode):
                continue

            # If it is a file, then save the stats under the
            # appropriate key
            cache[pkg_name] = sinfo

        return cache

    def last_mtime(self):
        return max(
            sinfo.st_mtime for sinfo in self._packages_to_stats.values())

    def __getitem__(self, item):
        return self._packages_to_stats[item]

    def __iter__(self):
        return iter(self._packages_to_stats)

    def __len__(self):
        return len(self._packages_to_stats)


@six.add_metaclass(abc.ABCMeta)
class Indexer(object):
    """Adaptor for indexes that need to be generated when repos are updated."""

    def create(self):
        self.index = self._create()

    @abc.abstractmethod
    def _create(self):
        """Create an empty index and return it."""

    def needs_update(self, pkg):
        """Whether an update is needed when the package file hasn't changed.

        Returns:
            (bool): ``True`` if this package needs its index
                updated, ``False`` otherwise.

        We already automatically update indexes when package files
        change, but other files (like patches) may change underneath the
        package file. This method can be used to check additional
        package-specific files whenever they're loaded, to tell the
        RepoIndex to update the index *just* for that package.

        """
        return False

    @abc.abstractmethod
    def read(self, stream):
        """Read this index from a provided file object."""

    @abc.abstractmethod
    def update(self, pkg_fullname):
        """Update the index in memory with information about a package."""

    @abc.abstractmethod
    def write(self, stream):
        """Write the index to a file object."""


class TagIndexer(Indexer):
    """Lifecycle methods for a TagIndex on a Repo."""
    def _create(self):
        return spack.tag.TagIndex()

    def read(self, stream):
        self.index = spack.tag.TagIndex.from_json(stream)

    def update(self, pkg_fullname):
        self.index.update_package(pkg_fullname)

    def write(self, stream):
        self.index.to_json(stream)


class ProviderIndexer(Indexer):
    """Lifecycle methods for virtual package providers."""
    def _create(self):
        return spack.provider_index.ProviderIndex()

    def read(self, stream):
        self.index = spack.provider_index.ProviderIndex.from_json(stream)

    def update(self, pkg_fullname):
        name = pkg_fullname.split('.')[-1]
        if spack.repo.path.is_virtual(name, use_index=False):
            return
        self.index.remove_provider(pkg_fullname)
        self.index.update(pkg_fullname)

    def write(self, stream):
        self.index.to_json(stream)


class PatchIndexer(Indexer):
    """Lifecycle methods for patch cache."""
    def _create(self):
        return spack.patch.PatchCache()

    def needs_update(self):
        # TODO: patches can change under a package and we should handle
        # TODO: it, but we currently punt. This should be refactored to
        # TODO: check whether patches changed each time a package loads,
        # TODO: tell the RepoIndex to reindex them.
        return False

    def read(self, stream):
        self.index = spack.patch.PatchCache.from_json(stream)

    def write(self, stream):
        self.index.to_json(stream)

    def update(self, pkg_fullname):
        self.index.update_package(pkg_fullname)


class RepoIndex(object):
    """Container class that manages a set of Indexers for a Repo.

    This class is responsible for checking packages in a repository for
    updates (using ``FastPackageChecker``) and for regenerating indexes
    when they're needed.

    ``Indexers`` should be added to the ``RepoIndex`` using
    ``add_index(name, indexer)``, and they should support the interface
    defined by ``Indexer``, so that the ``RepoIndex`` can read, generate,
    and update stored indices.

    Generated indexes are accessed by name via ``__getitem__()``.

    """
    def __init__(self, package_checker, namespace):
        self.checker = package_checker
        self.packages_path = self.checker.packages_path
        if sys.platform == 'win32':
            self.packages_path = \
                spack.util.path.convert_to_posix_path(self.packages_path)
        self.namespace = namespace

        self.indexers = {}
        self.indexes = {}

    def add_indexer(self, name, indexer):
        """Add an indexer to the repo index.

        Arguments:
            name (str): name of this indexer

            indexer (object): an object that supports create(), read(),
                write(), and get_index() operations

        """
        self.indexers[name] = indexer

    def __getitem__(self, name):
        """Get the index with the specified name, reindexing if needed."""
        indexer = self.indexers.get(name)
        if not indexer:
            raise KeyError('no such index: %s' % name)

        if name not in self.indexes:
            self._build_all_indexes()

        return self.indexes[name]

    def _build_all_indexes(self):
        """Build all the indexes at once.

        We regenerate *all* indexes whenever *any* index needs an update,
        because the main bottleneck here is loading all the packages.  It
        can take tens of seconds to regenerate sequentially, and we'd
        rather only pay that cost once rather than on several
        invocations.

        """
        for name, indexer in self.indexers.items():
            self.indexes[name] = self._build_index(name, indexer)

    def _build_index(self, name, indexer):
        """Determine which packages need an update, and update indexes."""

        # Filename of the provider index cache (we assume they're all json)
        cache_filename = '{0}/{1}-index.json'.format(name, self.namespace)

        # Compute which packages needs to be updated in the cache
        misc_cache = spack.caches.misc_cache
        index_mtime = misc_cache.mtime(cache_filename)

        needs_update = [
            x for x, sinfo in self.checker.items()
            if sinfo.st_mtime > index_mtime
        ]

        index_existed = misc_cache.init_entry(cache_filename)
        if index_existed and not needs_update:
            # If the index exists and doesn't need an update, read it
            with misc_cache.read_transaction(cache_filename) as f:
                indexer.read(f)

        else:
            # Otherwise update it and rewrite the cache file
            with misc_cache.write_transaction(cache_filename) as (old, new):
                indexer.read(old) if old else indexer.create()

                for pkg_name in needs_update:
                    namespaced_name = '%s.%s' % (self.namespace, pkg_name)
                    indexer.update(namespaced_name)

                indexer.write(new)

        return indexer.index


class RepoPath(object):
    """A RepoPath is a list of repos that function as one.

    It functions exactly like a Repo, but it operates on the combined
    results of the Repos in its list instead of on a single package
    repository.

    Args:
        repos (list): list Repo objects or paths to put in this RepoPath
    """

    def __init__(self, *repos):
        self.repos = []
        self.by_namespace = nm.NamespaceTrie()

        self._provider_index = None
        self._patch_index = None
        self._tag_index = None

        # Add each repo to this path.
        for repo in repos:
            try:
                if isinstance(repo, six.string_types):
                    repo = Repo(repo)
                self.put_last(repo)
            except RepoError as e:
                tty.warn("Failed to initialize repository: '%s'." % repo,
                         e.message,
                         "To remove the bad repository, run this command:",
                         "    spack repo rm %s" % repo)

    def put_first(self, repo):
        """Add repo first in the search path."""
        if isinstance(repo, RepoPath):
            for r in reversed(repo.repos):
                self.put_first(r)
            return

        self.repos.insert(0, repo)
        self.by_namespace[repo.full_namespace] = repo

    def put_last(self, repo):
        """Add repo last in the search path."""
        if isinstance(repo, RepoPath):
            for r in repo.repos:
                self.put_last(r)
            return

        self.repos.append(repo)

        # don't mask any higher-precedence repos with same namespace
        if repo.full_namespace not in self.by_namespace:
            self.by_namespace[repo.full_namespace] = repo

    def remove(self, repo):
        """Remove a repo from the search path."""
        if repo in self.repos:
            self.repos.remove(repo)

    def get_repo(self, namespace, default=NOT_PROVIDED):
        """Get a repository by namespace.

        Arguments:

            namespace:

                Look up this namespace in the RepoPath, and return it if found.

        Optional Arguments:

            default:

                If default is provided, return it when the namespace
                isn't found.  If not, raise an UnknownNamespaceError.
        """
        full_namespace = python_package_for_repo(namespace)
        if full_namespace not in self.by_namespace:
            if default == NOT_PROVIDED:
                raise UnknownNamespaceError(namespace)
            return default
        return self.by_namespace[full_namespace]

    def first_repo(self):
        """Get the first repo in precedence order."""
        return self.repos[0] if self.repos else None

    @llnl.util.lang.memoized
    def _all_package_names(self, include_virtuals):
        """Return all unique package names in all repositories."""
        all_pkgs = set()
        for repo in self.repos:
            for name in repo.all_package_names(include_virtuals):
                all_pkgs.add(name)
        return sorted(all_pkgs, key=lambda n: n.lower())

    def all_package_names(self, include_virtuals=False):
        return self._all_package_names(include_virtuals)

    def packages_with_tags(self, *tags):
        r = set()
        for repo in self.repos:
            r |= set(repo.packages_with_tags(*tags))
        return sorted(r)

    def all_packages(self):
        for name in self.all_package_names():
            yield self.get(name)

    def all_package_classes(self):
        for name in self.all_package_names():
            yield self.get_pkg_class(name)

    @property
    def provider_index(self):
        """Merged ProviderIndex from all Repos in the RepoPath."""
        if self._provider_index is None:
            self._provider_index = spack.provider_index.ProviderIndex()
            for repo in reversed(self.repos):
                self._provider_index.merge(repo.provider_index)

        return self._provider_index

    @property
    def tag_index(self):
        """Merged TagIndex from all Repos in the RepoPath."""
        if self._tag_index is None:
            self._tag_index = spack.tag.TagIndex()
            for repo in reversed(self.repos):
                self._tag_index.merge(repo.tag_index)

        return self._tag_index

    @property
    def patch_index(self):
        """Merged PatchIndex from all Repos in the RepoPath."""
        if self._patch_index is None:
            self._patch_index = spack.patch.PatchCache()
            for repo in reversed(self.repos):
                self._patch_index.update(repo.patch_index)

        return self._patch_index

    @autospec
    def providers_for(self, vpkg_spec):
        providers = self.provider_index.providers_for(vpkg_spec)
        if not providers:
            raise UnknownPackageError(vpkg_spec.fullname)
        return providers

    @autospec
    def extensions_for(self, extendee_spec):
        return [p for p in self.all_packages() if p.extends(extendee_spec)]

    def last_mtime(self):
        """Time a package file in this repo was last updated."""
        return max(repo.last_mtime() for repo in self.repos)

    def repo_for_pkg(self, spec):
        """Given a spec, get the repository for its package."""
        # We don't @_autospec this function b/c it's called very frequently
        # and we want to avoid parsing str's into Specs unnecessarily.
        namespace = None
        if isinstance(spec, spack.spec.Spec):
            namespace = spec.namespace
            name = spec.name
        else:
            # handle strings directly for speed instead of @_autospec'ing
            namespace, _, name = spec.rpartition('.')

        # If the spec already has a namespace, then return the
        # corresponding repo if we know about it.
        if namespace:
            fullspace = python_package_for_repo(namespace)
            if fullspace not in self.by_namespace:
                raise UnknownNamespaceError(namespace)
            return self.by_namespace[fullspace]

        # If there's no namespace, search in the RepoPath.
        for repo in self.repos:
            if name in repo:
                return repo

        # If the package isn't in any repo, return the one with
        # highest precedence.  This is for commands like `spack edit`
        # that can operate on packages that don't exist yet.
        return self.first_repo()

    @autospec
    def get(self, spec):
        """Returns the package associated with the supplied spec."""
        return self.repo_for_pkg(spec).get(spec)

    def get_pkg_class(self, pkg_name):
        """Find a class for the spec's package and return the class object."""
        return self.repo_for_pkg(pkg_name).get_pkg_class(pkg_name)

    @autospec
    def dump_provenance(self, spec, path):
        """Dump provenance information for a spec to a particular path.

           This dumps the package file and any associated patch files.
           Raises UnknownPackageError if not found.
        """
        return self.repo_for_pkg(spec).dump_provenance(spec, path)

    def dirname_for_package_name(self, pkg_name):
        return self.repo_for_pkg(pkg_name).dirname_for_package_name(pkg_name)

    def filename_for_package_name(self, pkg_name):
        return self.repo_for_pkg(pkg_name).filename_for_package_name(pkg_name)

    def exists(self, pkg_name):
        """Whether package with the give name exists in the path's repos.

        Note that virtual packages do not "exist".
        """
        return any(repo.exists(pkg_name) for repo in self.repos)

    def is_virtual(self, pkg_name, use_index=True):
        """True if the package with this name is virtual, False otherwise.

        Set `use_index` False when calling from a code block that could
        be run during the computation of the provider index."""
        have_name = pkg_name is not None
        if have_name and not isinstance(pkg_name, str):
            raise ValueError(
                "is_virtual(): expected package name, got %s" % type(pkg_name))
        if use_index:
            return have_name and pkg_name in self.provider_index
        else:
            return have_name and (not self.exists(pkg_name) or
                                  self.get_pkg_class(pkg_name).virtual)

    def __contains__(self, pkg_name):
        return self.exists(pkg_name)


class Repo(object):
    """Class representing a package repository in the filesystem.

    Each package repository must have a top-level configuration file
    called `repo.yaml`.

    Currently, `repo.yaml` this must define:

    `namespace`:
        A Python namespace where the repository's packages should live.

    """

    def __init__(self, root):
        """Instantiate a package repository from a filesystem path.

        Args:
            root: the root directory of the repository
        """
        # Root directory, containing _repo.yaml and package dirs
        # Allow roots to by spack-relative by starting with '$spack'
        self.root = spack.util.path.canonicalize_path(root)

        # check and raise BadRepoError on fail.
        def check(condition, msg):
            if not condition:
                raise BadRepoError(msg)

        # Validate repository layout.
        self.config_file = os.path.join(self.root, repo_config_name)
        check(os.path.isfile(self.config_file),
              "No %s found in '%s'" % (repo_config_name, root))

        self.packages_path = os.path.join(self.root, packages_dir_name)
        check(os.path.isdir(self.packages_path),
              "No directory '%s' found in '%s'" % (packages_dir_name, root))

        # Read configuration and validate namespace
        config = self._read_config()
        check('namespace' in config, '%s must define a namespace.'
              % os.path.join(root, repo_config_name))

        self.namespace = config['namespace']
        check(re.match(r'[a-zA-Z][a-zA-Z0-9_.]+', self.namespace),
              ("Invalid namespace '%s' in repo '%s'. "
               % (self.namespace, self.root)) +
              "Namespaces must be valid python identifiers separated by '.'")

        # Set up 'full_namespace' to include the super-namespace
        self.full_namespace = python_package_for_repo(self.namespace)

        # Keep name components around for checking prefixes.
        self._names = self.full_namespace.split('.')

        # These are internal cache variables.
        self._modules = {}
        self._classes = {}
        self._instances = {}

        # Maps that goes from package name to corresponding file stat
        self._fast_package_checker = None

        # Indexes for this repository, computed lazily
        self._repo_index = None

    def real_name(self, import_name):
        """Allow users to import Spack packages using Python identifiers.

        A python identifier might map to many different Spack package
        names due to hyphen/underscore ambiguity.

        Easy example:
            num3proxy   -> 3proxy

        Ambiguous:
            foo_bar -> foo_bar, foo-bar

        More ambiguous:
            foo_bar_baz -> foo_bar_baz, foo-bar-baz, foo_bar-baz, foo-bar_baz
        """
        if import_name in self:
            return import_name

        options = nm.possible_spack_module_names(import_name)
        options.remove(import_name)
        for name in options:
            if name in self:
                return name
        return None

    def is_prefix(self, fullname):
        """True if fullname is a prefix of this Repo's namespace."""
        parts = fullname.split('.')
        return self._names[:len(parts)] == parts

    def _read_config(self):
        """Check for a YAML config file in this db's root directory."""
        try:
            with open(self.config_file) as reponame_file:
                yaml_data = yaml.load(reponame_file)

                if (not yaml_data or 'repo' not in yaml_data or
                        not isinstance(yaml_data['repo'], dict)):
                    tty.die("Invalid %s in repository %s" % (
                        repo_config_name, self.root))

                return yaml_data['repo']

        except IOError:
            tty.die("Error reading %s when opening %s"
                    % (self.config_file, self.root))

    @autospec
    def get(self, spec):
        """Returns the package associated with the supplied spec."""
        # NOTE: we only check whether the package is None here, not whether it
        # actually exists, because we have to load it anyway, and that ends up
        # checking for existence. We avoid constructing FastPackageChecker,
        # which will stat all packages.
        if spec.name is None:
            raise UnknownPackageError(None, self)

        if spec.namespace and spec.namespace != self.namespace:
            raise UnknownPackageError(spec.name, self.namespace)

        package_class = self.get_pkg_class(spec.name)
        try:
            return package_class(spec)
        except spack.error.SpackError:
            # pass these through as their error messages will be fine.
            raise
        except Exception as e:
            tty.debug(e)

            # Make sure other errors in constructors hit the error
            # handler by wrapping them
            if spack.config.get('config:debug'):
                sys.excepthook(*sys.exc_info())
            raise FailedConstructorError(spec.fullname, *sys.exc_info())

    @autospec
    def dump_provenance(self, spec, path):
        """Dump provenance information for a spec to a particular path.

           This dumps the package file and any associated patch files.
           Raises UnknownPackageError if not found.
        """
        if spec.namespace and spec.namespace != self.namespace:
            raise UnknownPackageError(
                "Repository %s does not contain package %s."
                % (self.namespace, spec.fullname))

        # Install patch files needed by the package.
        fs.mkdirp(path)
        for patch in itertools.chain.from_iterable(
                spec.package.patches.values()):

            if patch.path:
                if os.path.exists(patch.path):
                    fs.install(patch.path, path)
                else:
                    tty.warn("Patch file did not exist: %s" % patch.path)

        # Install the package.py file itself.
        fs.install(self.filename_for_package_name(spec.name), path)

    def purge(self):
        """Clear entire package instance cache."""
        self._instances.clear()

    @property
    def index(self):
        """Construct the index for this repo lazily."""
        if self._repo_index is None:
            self._repo_index = RepoIndex(self._pkg_checker, self.namespace)
            self._repo_index.add_indexer('providers', ProviderIndexer())
            self._repo_index.add_indexer('tags', TagIndexer())
            self._repo_index.add_indexer('patches', PatchIndexer())
        return self._repo_index

    @property
    def provider_index(self):
        """A provider index with names *specific* to this repo."""
        return self.index['providers']

    @property
    def tag_index(self):
        """Index of tags and which packages they're defined on."""
        return self.index['tags']

    @property
    def patch_index(self):
        """Index of patches and packages they're defined on."""
        return self.index['patches']

    @autospec
    def providers_for(self, vpkg_spec):
        providers = self.provider_index.providers_for(vpkg_spec)
        if not providers:
            raise UnknownPackageError(vpkg_spec.fullname)
        return providers

    @autospec
    def extensions_for(self, extendee_spec):
        return [p for p in self.all_packages() if p.extends(extendee_spec)]

    def dirname_for_package_name(self, pkg_name):
        """Get the directory name for a particular package.  This is the
           directory that contains its package.py file."""
        return os.path.join(self.packages_path, pkg_name)

    def filename_for_package_name(self, pkg_name):
        """Get the filename for the module we should load for a particular
           package.  Packages for a Repo live in
           ``$root/<package_name>/package.py``

           This will return a proper package.py path even if the
           package doesn't exist yet, so callers will need to ensure
           the package exists before importing.
        """
        pkg_dir = self.dirname_for_package_name(pkg_name)
        return os.path.join(pkg_dir, package_file_name)

    @property
    def _pkg_checker(self):
        if self._fast_package_checker is None:
            self._fast_package_checker = FastPackageChecker(self.packages_path)
        return self._fast_package_checker

    def all_package_names(self, include_virtuals=False):
        """Returns a sorted list of all package names in the Repo."""
        names = sorted(self._pkg_checker.keys())
        if include_virtuals:
            return names
        return [x for x in names if not self.is_virtual(x)]

    def packages_with_tags(self, *tags):
        v = set(self.all_package_names())
        index = self.tag_index

        for t in tags:
            t = t.lower()
            v &= set(index[t])

        return sorted(v)

    def all_packages(self):
        """Iterator over all packages in the repository.

        Use this with care, because loading packages is slow.

        """
        for name in self.all_package_names():
            yield self.get(name)

    def all_package_classes(self):
        """Iterator over all package *classes* in the repository.

        Use this with care, because loading packages is slow.
        """
        for name in self.all_package_names():
            yield self.get_pkg_class(name)

    def exists(self, pkg_name):
        """Whether a package with the supplied name exists."""
        if pkg_name is None:
            return False

        # if the FastPackageChecker is already constructed, use it
        if self._fast_package_checker:
            return pkg_name in self._pkg_checker

        # if not, check for the package.py file
        path = self.filename_for_package_name(pkg_name)
        return os.path.exists(path)

    def last_mtime(self):
        """Time a package file in this repo was last updated."""
        return self._pkg_checker.last_mtime()

    def is_virtual(self, pkg_name):
        """True if the package with this name is virtual, False otherwise."""
        return pkg_name in self.provider_index

    def get_pkg_class(self, pkg_name):
        """Get the class for the package out of its module.

        First loads (or fetches from cache) a module for the
        package. Then extracts the package class from the module
        according to Spack's naming convention.
        """
        namespace, _, pkg_name = pkg_name.rpartition('.')
        if namespace and (namespace != self.namespace):
            raise InvalidNamespaceError('Invalid namespace for %s repo: %s'
                                        % (self.namespace, namespace))

        class_name = nm.mod_to_class(pkg_name)

        fullname = "{0}.{1}".format(self.full_namespace, pkg_name)
        try:
            module = importlib.import_module(fullname)
        except ImportError:
            raise UnknownPackageError(pkg_name)

        cls = getattr(module, class_name)
        if not inspect.isclass(cls):
            tty.die("%s.%s is not a class" % (pkg_name, class_name))

        return cls

    def __str__(self):
        return "[Repo '%s' at '%s']" % (self.namespace, self.root)

    def __repr__(self):
        return self.__str__()

    def __contains__(self, pkg_name):
        return self.exists(pkg_name)


def create_repo(root, namespace=None):
    """Create a new repository in root with the specified namespace.

       If the namespace is not provided, use basename of root.
       Return the canonicalized path and namespace of the created repository.
    """
    root = spack.util.path.canonicalize_path(root)
    if not namespace:
        namespace = os.path.basename(root)

    if not re.match(r'\w[\.\w-]*', namespace):
        raise InvalidNamespaceError(
            "'%s' is not a valid namespace." % namespace)

    existed = False
    if os.path.exists(root):
        if os.path.isfile(root):
            raise BadRepoError('File %s already exists and is not a directory'
                               % root)
        elif os.path.isdir(root):
            if not os.access(root, os.R_OK | os.W_OK):
                raise BadRepoError(
                    'Cannot create new repo in %s: cannot access directory.'
                    % root)
            if os.listdir(root):
                raise BadRepoError(
                    'Cannot create new repo in %s: directory is not empty.'
                    % root)
        existed = True

    full_path = os.path.realpath(root)
    parent = os.path.dirname(full_path)
    if not os.access(parent, os.R_OK | os.W_OK):
        raise BadRepoError(
            "Cannot create repository in %s: can't access parent!" % root)

    try:
        config_path = os.path.join(root, repo_config_name)
        packages_path = os.path.join(root, packages_dir_name)

        fs.mkdirp(packages_path)
        with open(config_path, 'w') as config:
            config.write("repo:\n")
            config.write("  namespace: '%s'\n" % namespace)

    except (IOError, OSError) as e:
        # try to clean up.
        if existed:
            shutil.rmtree(config_path, ignore_errors=True)
            shutil.rmtree(packages_path, ignore_errors=True)
        else:
            shutil.rmtree(root, ignore_errors=True)

        raise BadRepoError('Failed to create new repository in %s.' % root,
                           "Caused by %s: %s" % (type(e), e))

    return full_path, namespace


def create_or_construct(path, namespace=None):
    """Create a repository, or just return a Repo if it already exists."""
    if not os.path.exists(path):
        fs.mkdirp(path)
        create_repo(path, namespace)
    return Repo(path)


def _path(repo_dirs=None):
    """Get the singleton RepoPath instance for Spack."""
    repo_dirs = repo_dirs or spack.config.get('repos')
    if not repo_dirs:
        raise NoRepoConfiguredError(
            "Spack configuration contains no package repositories.")
    return RepoPath(*repo_dirs)


#: Singleton repo path instance
path = llnl.util.lang.Singleton(_path)

# Add the finder to sys.meta_path
sys.meta_path.append(ReposFinder())


def get(spec):
    """Convenience wrapper around ``spack.repo.get()``."""
    return path.get(spec)


def all_package_names(include_virtuals=False):
    """Convenience wrapper around ``spack.repo.all_package_names()``."""
    return path.all_package_names(include_virtuals)


@contextlib.contextmanager
def additional_repository(repository):
    """Adds temporarily a repository to the default one.

    Args:
        repository: repository to be added
    """
    path.put_first(repository)
    yield
    path.remove(repository)


@contextlib.contextmanager
def use_repositories(*paths_and_repos):
    """Use the repositories passed as arguments within the context manager.

    Args:
        *paths_and_repos: paths to the repositories to be used, or
            already constructed Repo objects

    Returns:
        Corresponding RepoPath object
    """
    global path
    path, saved = RepoPath(*paths_and_repos), path
    try:
        yield path
    finally:
        path = saved


class RepoError(spack.error.SpackError):
    """Superclass for repository-related errors."""


class NoRepoConfiguredError(RepoError):
    """Raised when there are no repositories configured."""


class InvalidNamespaceError(RepoError):
    """Raised when an invalid namespace is encountered."""


class BadRepoError(RepoError):
    """Raised when repo layout is invalid."""


class UnknownEntityError(RepoError):
    """Raised when we encounter a package spack doesn't have."""


class IndexError(RepoError):
    """Raised when there's an error with an index."""


class UnknownPackageError(UnknownEntityError):
    """Raised when we encounter a package spack doesn't have."""

    def __init__(self, name, repo=None):
        msg = None
        long_msg = None
        if name:
            if repo:
                msg = "Package '{0}' not found in repository '{1.root}'"
                msg = msg.format(name, repo)
            else:
                msg = "Package '{0}' not found.".format(name)

            # Special handling for specs that may have been intended as
            # filenames: prompt the user to ask whether they intended to write
            # './<name>'.
            if name.endswith(".yaml"):
                long_msg = "Did you mean to specify a filename with './{0}'?"
                long_msg = long_msg.format(name)
        else:
            msg = "Attempting to retrieve anonymous package."

        super(UnknownPackageError, self).__init__(msg, long_msg)
        self.name = name


class UnknownNamespaceError(UnknownEntityError):
    """Raised when we encounter an unknown namespace"""

    def __init__(self, namespace):
        super(UnknownNamespaceError, self).__init__(
            "Unknown namespace: %s" % namespace)


class FailedConstructorError(RepoError):
    """Raised when a package's class constructor fails."""

    def __init__(self, name, exc_type, exc_obj, exc_tb):
        super(FailedConstructorError, self).__init__(
            "Class constructor failed for package '%s'." % name,
            '\nCaused by:\n' +
            ('%s: %s\n' % (exc_type.__name__, exc_obj)) +
            ''.join(traceback.format_tb(exc_tb)))
        self.name = name
