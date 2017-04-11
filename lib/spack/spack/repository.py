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
import os
import stat
import shutil
import errno
import sys
import inspect
import imp
import re
import traceback
from bisect import bisect_left
from types import ModuleType

import yaml

import llnl.util.tty as tty
from llnl.util.filesystem import *

import spack
import spack.error
import spack.spec
from spack.provider_index import ProviderIndex
from spack.util.path import canonicalize_path
from spack.util.naming import *

#
# Super-namespace for all packages.
# Package modules are imported as spack.pkg.<namespace>.<pkg-name>.
#
repo_namespace     = 'spack.pkg'

#
# These names describe how repos should be laid out in the filesystem.
#
repo_config_name   = 'repo.yaml'   # Top-level filename for repo config.
repo_index_name    = 'index.yaml'  # Top-level filename for repository index.
packages_dir_name  = 'packages'    # Top-level repo directory containing pkgs.
package_file_name  = 'package.py'  # Filename for packages in a repository.

# Guaranteed unused default value for some functions.
NOT_PROVIDED = object()


def _autospec(function):
    """Decorator that automatically converts the argument of a single-arg
       function to a Spec."""

    def converter(self, spec_like, *args, **kwargs):
        if not isinstance(spec_like, spack.spec.Spec):
            spec_like = spack.spec.Spec(spec_like)
        return function(self, spec_like, *args, **kwargs)
    return converter


class SpackNamespace(ModuleType):
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
        setattr(self, name, __import__(submodule))
        return getattr(self, name)


class RepoPath(object):
    """A RepoPath is a list of repos that function as one.

       It functions exactly like a Repo, but it operates on the
       combined results of the Repos in its list instead of on a
       single package repository.
    """

    def __init__(self, *repo_dirs, **kwargs):
        # super-namespace for all packages in the RepoPath
        self.super_namespace = kwargs.get('namespace', repo_namespace)

        self.repos = []
        self.by_namespace = NamespaceTrie()
        self.by_path = {}

        self._all_package_names = None
        self._provider_index = None

        # If repo_dirs is empty, just use the configuration
        if not repo_dirs:
            import spack.config
            repo_dirs = spack.config.get_config('repos')
            if not repo_dirs:
                raise NoRepoConfiguredError(
                    "Spack configuration contains no package repositories.")

        # Add each repo to this path.
        for root in repo_dirs:
            try:
                repo = Repo(root, self.super_namespace)
                self.put_last(repo)
            except RepoError as e:
                tty.warn("Failed to initialize repository at '%s'." % root,
                         e.message,
                         "To remove the bad repository, run this command:",
                         "    spack repo rm %s" % root)

    def swap(self, other):
        """Convenience function to make swapping repositories easier.

        This is currently used by mock tests.
        TODO: Maybe there is a cleaner way.

        """
        attrs = ['repos',
                 'by_namespace',
                 'by_path',
                 '_all_package_names',
                 '_provider_index']
        for attr in attrs:
            tmp = getattr(self, attr)
            setattr(self, attr, getattr(other, attr))
            setattr(other, attr, tmp)

    def _add(self, repo):
        """Add a repository to the namespace and path indexes.

        Checks for duplicates -- two repos can't have the same root
        directory, and they provide have the same namespace.

        """
        if repo.root in self.by_path:
            raise DuplicateRepoError("Duplicate repository: '%s'" % repo.root)

        if repo.namespace in self.by_namespace:
            raise DuplicateRepoError(
                "Package repos '%s' and '%s' both provide namespace %s"
                % (repo.root, self.by_namespace[repo.namespace].root,
                   repo.namespace))

        # Add repo to the pkg indexes
        self.by_namespace[repo.full_namespace] = repo
        self.by_path[repo.root] = repo

    def put_first(self, repo):
        """Add repo first in the search path."""
        self._add(repo)
        self.repos.insert(0, repo)

    def put_last(self, repo):
        """Add repo last in the search path."""
        self._add(repo)
        self.repos.append(repo)

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
        fullspace = '%s.%s' % (self.super_namespace, namespace)
        if fullspace not in self.by_namespace:
            if default == NOT_PROVIDED:
                raise UnknownNamespaceError(namespace)
            return default
        return self.by_namespace[fullspace]

    def first_repo(self):
        """Get the first repo in precedence order."""
        return self.repos[0] if self.repos else None

    def all_package_names(self):
        """Return all unique package names in all repositories."""
        if self._all_package_names is None:
            all_pkgs = set()
            for repo in self.repos:
                for name in repo.all_package_names():
                    all_pkgs.add(name)
            self._all_package_names = sorted(all_pkgs, key=lambda n: n.lower())
        return self._all_package_names

    def all_packages(self):
        for name in self.all_package_names():
            yield self.get(name)

    @property
    def provider_index(self):
        """Merged ProviderIndex from all Repos in the RepoPath."""
        if self._provider_index is None:
            self._provider_index = ProviderIndex()
            for repo in reversed(self.repos):
                self._provider_index.merge(repo.provider_index)

        return self._provider_index

    @_autospec
    def providers_for(self, vpkg_spec):
        providers = self.provider_index.providers_for(vpkg_spec)
        if not providers:
            raise UnknownPackageError(vpkg_spec.name)
        return providers

    @_autospec
    def extensions_for(self, extendee_spec):
        return [p for p in self.all_packages() if p.extends(extendee_spec)]

    def find_module(self, fullname, path=None):
        """Implements precedence for overlaid namespaces.

        Loop checks each namespace in self.repos for packages, and
        also handles loading empty containing namespaces.

        """
        # namespaces are added to repo, and package modules are leaves.
        namespace, dot, module_name = fullname.rpartition('.')

        # If it's a module in some repo, or if it is the repo's
        # namespace, let the repo handle it.
        for repo in self.repos:
            if namespace == repo.full_namespace:
                if repo.real_name(module_name):
                    return repo
            elif fullname == repo.full_namespace:
                return repo

        # No repo provides the namespace, but it is a valid prefix of
        # something in the RepoPath.
        if self.by_namespace.is_prefix(fullname):
            return self

        return None

    def load_module(self, fullname):
        """Handles loading container namespaces when necessary.

        See ``Repo`` for how actual package modules are loaded.
        """
        if fullname in sys.modules:
            return sys.modules[fullname]

        if not self.by_namespace.is_prefix(fullname):
            raise ImportError("No such Spack repo: %s" % fullname)

        module = SpackNamespace(fullname)
        module.__loader__ = self
        sys.modules[fullname] = module
        return module

    @_autospec
    def repo_for_pkg(self, spec):
        """Given a spec, get the repository for its package."""
        # If the spec already has a namespace, then return the
        # corresponding repo if we know about it.
        if spec.namespace:
            fullspace = '%s.%s' % (self.super_namespace, spec.namespace)
            if fullspace not in self.by_namespace:
                raise UnknownNamespaceError(spec.namespace)
            return self.by_namespace[fullspace]

        # If there's no namespace, search in the RepoPath.
        for repo in self.repos:
            if spec.name in repo:
                return repo

        # If the package isn't in any repo, return the one with
        # highest precedence.  This is for commands like `spack edit`
        # that can operate on packages that don't exist yet.
        return self.first_repo()

    @_autospec
    def get(self, spec, new=False):
        """Find a repo that contains the supplied spec's package.

           Raises UnknownPackageError if not found.
        """
        return self.repo_for_pkg(spec).get(spec)

    def get_pkg_class(self, pkg_name):
        """Find a class for the spec's package and return the class object."""
        return self.repo_for_pkg(pkg_name).get_pkg_class(pkg_name)

    @_autospec
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

    def is_virtual(self, pkg_name):
        """True if the package with this name is virtual, False otherwise."""
        return pkg_name in self.provider_index

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

    def __init__(self, root, namespace=repo_namespace):
        """Instantiate a package repository from a filesystem path.

        Arguments:
        root        The root directory of the repository.

        namespace   A super-namespace that will contain the repo-defined
                    namespace (this is generally jsut `spack.pkg`). The
                    super-namespace is Spack's way of separating repositories
                    from other python namespaces.

        """
        # Root directory, containing _repo.yaml and package dirs
        # Allow roots to by spack-relative by starting with '$spack'
        self.root = canonicalize_path(root)

        # super-namespace for all packages in the Repo
        self.super_namespace = namespace

        # check and raise BadRepoError on fail.
        def check(condition, msg):
            if not condition:
                raise BadRepoError(msg)

        # Validate repository layout.
        self.config_file = join_path(self.root, repo_config_name)
        check(os.path.isfile(self.config_file),
              "No %s found in '%s'" % (repo_config_name, root))

        self.packages_path = join_path(self.root, packages_dir_name)
        check(os.path.isdir(self.packages_path),
              "No directory '%s' found in '%s'" % (repo_config_name, root))

        # Read configuration and validate namespace
        config = self._read_config()
        check('namespace' in config, '%s must define a namespace.'
              % join_path(root, repo_config_name))

        self.namespace = config['namespace']
        check(re.match(r'[a-zA-Z][a-zA-Z0-9_.]+', self.namespace),
              ("Invalid namespace '%s' in repo '%s'. "
               % (self.namespace, self.root)) +
              "Namespaces must be valid python identifiers separated by '.'")

        # Set up 'full_namespace' to include the super-namespace
        if self.super_namespace:
            self.full_namespace = "%s.%s" % (
                self.super_namespace, self.namespace)
        else:
            self.full_namespace = self.namespace

        # Keep name components around for checking prefixes.
        self._names = self.full_namespace.split('.')

        # These are internal cache variables.
        self._modules = {}
        self._classes = {}
        self._instances = {}

        # list of packages that are newer than the index.
        self._needs_update = []

        # Index of virtual dependencies
        self._provider_index = None

        # Cached list of package names.
        self._all_package_names = None

        # make sure the namespace for packages in this repo exists.
        self._create_namespace()

        # Unique filename for cache of virtual dependency providers
        self._cache_file = 'providers/%s-index.yaml' % self.namespace

    def _create_namespace(self):
        """Create this repo's namespace module and insert it into sys.modules.

        Ensures that modules loaded via the repo have a home, and that
        we don't get runtime warnings from Python's module system.

        """
        parent = None
        for l in range(1, len(self._names) + 1):
            ns = '.'.join(self._names[:l])

            if ns not in sys.modules:
                module = SpackNamespace(ns)
                module.__loader__ = self
                sys.modules[ns] = module

                # Ensure the namespace is an atrribute of its parent,
                # if it has not been set by something else already.
                #
                # This ensures that we can do things like:
                #    import spack.pkg.builtin.mpich as mpich
                if parent:
                    modname = self._names[l - 1]
                    setattr(parent, modname, module)
            else:
                # no need to set up a module
                module = sys.modules[ns]

            # but keep track of the parent in this loop
            parent = module

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

        options = possible_spack_module_names(import_name)
        options.remove(import_name)
        for name in options:
            if name in self:
                return name
        return None

    def is_prefix(self, fullname):
        """True if fullname is a prefix of this Repo's namespace."""
        parts = fullname.split('.')
        return self._names[:len(parts)] == parts

    def find_module(self, fullname, path=None):
        """Python find_module import hook.

        Returns this Repo if it can load the module; None if not.
        """
        if self.is_prefix(fullname):
            return self

        namespace, dot, module_name = fullname.rpartition('.')
        if namespace == self.full_namespace:
            if self.real_name(module_name):
                return self

        return None

    def load_module(self, fullname):
        """Python importer load hook.

        Tries to load the module; raises an ImportError if it can't.
        """
        if fullname in sys.modules:
            return sys.modules[fullname]

        namespace, dot, module_name = fullname.rpartition('.')

        if self.is_prefix(fullname):
            module = SpackNamespace(fullname)

        elif namespace == self.full_namespace:
            real_name = self.real_name(module_name)
            if not real_name:
                raise ImportError("No module %s in %s" % (module_name, self))
            module = self._get_pkg_module(real_name)

        else:
            raise ImportError("No module %s in %s" % (fullname, self))

        module.__loader__ = self
        sys.modules[fullname] = module
        if namespace != fullname:
            parent = sys.modules[namespace]
            if not hasattr(parent, module_name):
                setattr(parent, module_name, module)

        return module

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

    @_autospec
    def get(self, spec, new=False):
        if spec.virtual:
            raise UnknownPackageError(spec.name)

        if spec.namespace and spec.namespace != self.namespace:
            raise UnknownPackageError(
                "Repository %s does not contain package %s"
                % (self.namespace, spec.fullname))

        key = hash(spec)
        if new or key not in self._instances:
            package_class = self.get_pkg_class(spec.name)
            try:
                copy = spec.copy()  # defensive copy.  Package owns its spec.
                self._instances[key] = package_class(copy)
            except Exception:
                if spack.debug:
                    sys.excepthook(*sys.exc_info())
                raise FailedConstructorError(spec.fullname, *sys.exc_info())

        return self._instances[key]

    @_autospec
    def dump_provenance(self, spec, path):
        """Dump provenance information for a spec to a particular path.

           This dumps the package file and any associated patch files.
           Raises UnknownPackageError if not found.
        """
        # Some preliminary checks.
        if spec.virtual:
            raise UnknownPackageError(spec.name)

        if spec.namespace and spec.namespace != self.namespace:
            raise UnknownPackageError(
                "Repository %s does not contain package %s."
                % (self.namespace, spec.fullname))

        # Install any patch files needed by packages.
        mkdirp(path)
        for spec, patches in spec.package.patches.items():
            for patch in patches:
                if patch.path:
                    if os.path.exists(patch.path):
                        install(patch.path, path)
                    else:
                        tty.warn("Patch file did not exist: %s" % patch.path)

        # Install the package.py file itself.
        install(self.filename_for_package_name(spec), path)

    def purge(self):
        """Clear entire package instance cache."""
        self._instances.clear()

    def _update_provider_index(self):
        # Check modification dates of all packages
        self._fast_package_check()

        def read():
            with open(self.index_file) as f:
                self._provider_index = ProviderIndex.from_yaml(f)

        # Read the old ProviderIndex, or make a new one.
        key = self._cache_file
        index_existed = spack.misc_cache.init_entry(key)
        if index_existed and not self._needs_update:
            with spack.misc_cache.read_transaction(key) as f:
                self._provider_index = ProviderIndex.from_yaml(f)
        else:
            with spack.misc_cache.write_transaction(key) as (old, new):
                if old:
                    self._provider_index = ProviderIndex.from_yaml(old)
                else:
                    self._provider_index = ProviderIndex()

                for pkg_name in self._needs_update:
                    namespaced_name = '%s.%s' % (self.namespace, pkg_name)
                    self._provider_index.remove_provider(namespaced_name)
                    self._provider_index.update(namespaced_name)

                self._provider_index.to_yaml(new)

    @property
    def provider_index(self):
        """A provider index with names *specific* to this repo."""
        if self._provider_index is None:
            self._update_provider_index()
        return self._provider_index

    @_autospec
    def providers_for(self, vpkg_spec):
        providers = self.provider_index.providers_for(vpkg_spec)
        if not providers:
            raise UnknownPackageError(vpkg_spec.name)
        return providers

    @_autospec
    def extensions_for(self, extendee_spec):
        return [p for p in self.all_packages() if p.extends(extendee_spec)]

    def _check_namespace(self, spec):
        """Check that the spec's namespace is the same as this repository's."""
        if spec.namespace and spec.namespace != self.namespace:
            raise UnknownNamespaceError(spec.namespace)

    @_autospec
    def dirname_for_package_name(self, spec):
        """Get the directory name for a particular package.  This is the
           directory that contains its package.py file."""
        self._check_namespace(spec)
        return join_path(self.packages_path, spec.name)

    @_autospec
    def filename_for_package_name(self, spec):
        """Get the filename for the module we should load for a particular
           package.  Packages for a Repo live in
           ``$root/<package_name>/package.py``

           This will return a proper package.py path even if the
           package doesn't exist yet, so callers will need to ensure
           the package exists before importing.
        """
        self._check_namespace(spec)
        pkg_dir = self.dirname_for_package_name(spec.name)
        return join_path(pkg_dir, package_file_name)

    def _fast_package_check(self):
        """List packages in the repo and check whether index is up to date.

        Both of these opreations require checking all `package.py`
        files so we do them at the same time.  We list the repo
        directory and look at package.py files, and we compare the
        index modification date with the ost recently modified package
        file, storing the result.

        The implementation here should try to minimize filesystem
        calls.  At the moment, it is O(number of packages) and makes
        about one stat call per package.  This is resonably fast, and
        avoids actually importing packages in Spack, which is slow.

        """
        if self._all_package_names is None:
            self._all_package_names = []

            # Get index modification time.
            index_mtime = spack.misc_cache.mtime(self._cache_file)

            for pkg_name in os.listdir(self.packages_path):
                # Skip non-directories in the package root.
                pkg_dir = join_path(self.packages_path, pkg_name)

                # Warn about invalid names that look like packages.
                if not valid_module_name(pkg_name):
                    msg = ("Skipping package at %s. "
                           "'%s' is not a valid Spack module name.")
                    tty.warn(msg % (pkg_dir, pkg_name))
                    continue

                # construct the file name from the directory
                pkg_file = join_path(
                    self.packages_path, pkg_name, package_file_name)

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

                # if it's not a file, skip it.
                if stat.S_ISDIR(sinfo.st_mode):
                    continue

                # All checks passed.  Add it to the list.
                self._all_package_names.append(pkg_name)

                # record the package if it is newer than the index.
                if sinfo.st_mtime > index_mtime:
                    self._needs_update.append(pkg_name)

            self._all_package_names.sort()

        return self._all_package_names

    def all_package_names(self):
        """Returns a sorted list of all package names in the Repo."""
        self._fast_package_check()
        return self._all_package_names

    def all_packages(self):
        """Iterator over all packages in the repository.

        Use this with care, because loading packages is slow.

        """
        for name in self.all_package_names():
            yield self.get(name)

    def exists(self, pkg_name):
        """Whether a package with the supplied name exists."""
        if self._all_package_names:
            # This does a binary search in the sorted list.
            idx = bisect_left(self.all_package_names(), pkg_name)
            return (idx < len(self._all_package_names) and
                    self._all_package_names[idx] == pkg_name)

        # If we haven't generated the full package list, don't.
        # Just check whether the file exists.
        filename = self.filename_for_package_name(pkg_name)
        return os.path.exists(filename)

    def is_virtual(self, pkg_name):
        """True if the package with this name is virtual, False otherwise."""
        return self.provider_index.contains(pkg_name)

    def _get_pkg_module(self, pkg_name):
        """Create a module for a particular package.

        This caches the module within this Repo *instance*.  It does
        *not* add it to ``sys.modules``.  So, you can construct
        multiple Repos for testing and ensure that the module will be
        loaded once per repo.

        """
        if pkg_name not in self._modules:
            file_path = self.filename_for_package_name(pkg_name)

            if not os.path.exists(file_path):
                raise UnknownPackageError(pkg_name, self)

            if not os.path.isfile(file_path):
                tty.die("Something's wrong. '%s' is not a file!" % file_path)

            if not os.access(file_path, os.R_OK):
                tty.die("Cannot read '%s'!" % file_path)

            # e.g., spack.pkg.builtin.mpich
            fullname = "%s.%s" % (self.full_namespace, pkg_name)

            module = imp.load_source(fullname, file_path)
            module.__package__ = self.full_namespace
            module.__loader__ = self
            self._modules[pkg_name] = module

        return self._modules[pkg_name]

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

        class_name = mod_to_class(pkg_name)
        module = self._get_pkg_module(pkg_name)

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
    root = canonicalize_path(root)
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

        mkdirp(packages_path)
        with open(config_path, 'w') as config:
            config.write("repo:\n")
            config.write("  namespace: '%s'\n" % namespace)

    except (IOError, OSError) as e:
        raise BadRepoError('Failed to create new repository in %s.' % root,
                           "Caused by %s: %s" % (type(e), e))

        # try to clean up.
        if existed:
            shutil.rmtree(config_path, ignore_errors=True)
            shutil.rmtree(packages_path, ignore_errors=True)
        else:
            shutil.rmtree(root, ignore_errors=True)

    return full_path, namespace


class RepoError(spack.error.SpackError):
    """Superclass for repository-related errors."""


class NoRepoConfiguredError(RepoError):
    """Raised when there are no repositories configured."""


class InvalidNamespaceError(RepoError):
    """Raised when an invalid namespace is encountered."""


class BadRepoError(RepoError):
    """Raised when repo layout is invalid."""


class DuplicateRepoError(RepoError):
    """Raised when duplicate repos are added to a RepoPath."""


class PackageLoadError(spack.error.SpackError):
    """Superclass for errors related to loading packages."""


class UnknownPackageError(PackageLoadError):
    """Raised when we encounter a package spack doesn't have."""

    def __init__(self, name, repo=None):
        msg = None
        if repo:
            msg = "Package %s not found in repository %s" % (name, repo)
        else:
            msg = "Package %s not found." % name
        super(UnknownPackageError, self).__init__(msg)
        self.name = name


class UnknownNamespaceError(PackageLoadError):
    """Raised when we encounter an unknown namespace"""

    def __init__(self, namespace):
        super(UnknownNamespaceError, self).__init__(
            "Unknown namespace: %s" % namespace)


class FailedConstructorError(PackageLoadError):
    """Raised when a package's class constructor fails."""

    def __init__(self, name, exc_type, exc_obj, exc_tb):
        super(FailedConstructorError, self).__init__(
            "Class constructor failed for package '%s'." % name,
            '\nCaused by:\n' +
            ('%s: %s\n' % (exc_type.__name__, exc_obj)) +
            ''.join(traceback.format_tb(exc_tb)))
        self.name = name
