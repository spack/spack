##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
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
import os
import exceptions
import sys
import inspect
import glob
import imp
import re
import itertools
import traceback
from bisect import bisect_left
from external import yaml

import llnl.util.tty as tty
from llnl.util.filesystem import join_path
from llnl.util.lang import *

import spack.error
import spack.spec
from spack.virtual import ProviderIndex
from spack.util.naming import *

# Filename for package repo names
repo_config_filename = '_repo.yaml'

# Filename for packages in repos.
package_file_name = 'package.py'

def _autospec(function):
    """Decorator that automatically converts the argument of a single-arg
       function to a Spec."""
    def converter(self, spec_like, *args, **kwargs):
        if not isinstance(spec_like, spack.spec.Spec):
            spec_like = spack.spec.Spec(spec_like)
        return function(self, spec_like, *args, **kwargs)
    return converter


def _make_namespace_module(ns):
    module = imp.new_module(ns)
    module.__file__ = "(spack namespace)"
    module.__path__ = []
    module.__package__ = ns
    return module


class RepoPath(object):
    """A RepoPath is a list of repos that function as one.

       It functions exactly like a Repo, but it operates on the
       combined results of the Repos in its list instead of on a
       single package repository.
    """
    def __init__(self, *repo_dirs):
        self.repos = []
        self.by_namespace = NamespaceTrie()
        self.by_path = {}

        self._all_package_names = []
        self._provider_index = None

        for root in repo_dirs:
            # Try to make it a repo if it's not one.
            if not isinstance(root, Repo):
                repo = Repo(root)
            # Add the repo to the path.
            self.put_last(repo)


    def swap(self, other):
        """Convenience function to make swapping repostiories easier.

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
            raise DuplicateRepoError("Package repos are the same",
                                     repo, self.by_path[repo.root])

        if repo.namespace in self.by_namespace:
            raise DuplicateRepoError("Package repos cannot have the same name",
                                     repo, self.by_namespace[repo.namespace])

        # Add repo to the pkg indexes
        self.by_namespace[repo.namespace] = repo
        self.by_path[repo.root] = repo

        # add names to the cached name list
        new_pkgs = set(repo.all_package_names())
        new_pkgs.update(set(self._all_package_names))
        self._all_package_names = sorted(new_pkgs, key=lambda n:n.lower())


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


    def all_package_names(self):
        """Return all unique package names in all repositories."""
        return self._all_package_names


    def all_packages(self):
        for name in self.all_package_names():
            yield self.get(name)


    @_autospec
    def providers_for(self, vpkg_spec):
        if self._provider_index is None:
            self._provider_index = ProviderIndex(self.all_package_names())

        providers = self._provider_index.providers_for(vpkg_spec)
        if not providers:
            raise UnknownPackageError(vpkg_spec.name)
        return providers


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
            if namespace == repo.namespace:
                if repo.real_name(module_name):
                    return repo
            elif fullname == repo.namespace:
                return repo

        # No repo provides the namespace, but it is a valid prefix of
        # something in the RepoPath.
        if self.by_namespace.is_prefix(fullname):
            return self

        return None


    def load_module(self, fullname):
        """Loads containing namespaces when necessary.

        See ``Repo`` for how actual package modules are loaded.
        """
        if fullname in sys.modules:
            return sys.modules[fullname]

        # partition fullname into prefix and module name.
        namespace, dot, module_name = fullname.rpartition('.')

        if not self.by_namespace.is_prefix(fullname):
            raise ImportError("No such Spack repo: %s" % fullname)

        module = _make_namespace_module(namespace)
        module.__loader__ = self
        sys.modules[fullname] = module
        return module


    def repo_for_pkg(self, pkg_name):
        for repo in self.repos:
            if pkg_name in repo:
                return repo
        raise UnknownPackageError(pkg_name)


    @_autospec
    def get(self, spec, new=False):
        """Find a repo that contains the supplied spec's package.

           Raises UnknownPackageError if not found.
        """
        return self.repo_for_pkg(spec.name).get(spec)


    def dirname_for_package_name(self, pkg_name):
        return self.repo_for_pkg(pkg_name).dirname_for_package_name(pkg_name)


    def exists(self, pkg_name):
        return any(repo.exists(pkg_name) for repo in self.repos)


    def __contains__(self, pkg_name):
        return self.exists(pkg_name)



class Repo(object):
    """Class representing a package repository in the filesystem.

    Each package repository must have a top-level configuration file
    called `_repo.yaml`.

    Currently, `_repo.yaml` this must define:

    `namespace`:
        A Python namespace where the repository's packages should live.

    """
    def __init__(self, root):
        """Instantiate a package repository from a filesystem path."""
        # Root directory, containing _repo.yaml and package dirs
        self.root = root

        # Config file in <self.root>/_repo.yaml
        self.config_file = os.path.join(self.root, repo_config_filename)

        # Read configuration from _repo.yaml
        config = self._read_config()
        if not 'namespace' in config:
            tty.die('Package repo in %s must define a namespace in %s.'
                    % (self.root, repo_config_filename))

        # Check namespace in the repository configuration.
        self.namespace = config['namespace']
        if not re.match(r'[a-zA-Z][a-zA-Z0-9_.]+', self.namespace):
            tty.die(("Invalid namespace '%s' in '%s'. Namespaces must be "
                     "valid python identifiers separated by '.'")
                    % (self.namespace, self.root))
        self._names = self.namespace.split('.')

        # These are internal cache variables.
        self._modules = {}
        self._classes = {}
        self._instances = {}

        self._provider_index = None
        self._all_package_names = None

        # make sure the namespace for packages in this repo exists.
        self._create_namespace()


    def _create_namespace(self):
        """Create this repo's namespace module and insert it into sys.modules.

        Ensures that modules loaded via the repo have a home, and that
        we don't get runtime warnings from Python's module system.

        """
        for l in range(1, len(self._names)+1):
            ns = '.'.join(self._names[:l])
            if not ns in sys.modules:
                sys.modules[ns] = _make_namespace_module(ns)
                sys.modules[ns].__loader__ = self


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
        if namespace == self.namespace:
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
            module = _make_namespace_module(fullname)

        elif namespace == self.namespace:
            real_name = self.real_name(module_name)
            if not real_name:
                raise ImportError("No module %s in repo %s" % (module_name, namespace))
            module = self._get_pkg_module(real_name)

        else:
            raise ImportError("No module %s in repo %s" % (fullname, self.namespace))

        module.__loader__ = self
        sys.modules[fullname] = module
        return module


    def _read_config(self):
        """Check for a YAML config file in this db's root directory."""
        try:
            with open(self.config_file) as reponame_file:
                yaml_data = yaml.load(reponame_file)

                if (not yaml_data or 'repo' not in yaml_data or
                    not isinstance(yaml_data['repo'], dict)):
                    tty.die("Invalid %s in repository %s"
                            % (repo_config_filename, self.root))

                return yaml_data['repo']

        except exceptions.IOError, e:
            tty.die("Error reading %s when opening %s"
                    % (self.config_file, self.root))


    @_autospec
    def get(self, spec, new=False):
        if spec.virtual:
            raise UnknownPackageError(spec.name)

        if new and spec in self._instances:
            del self._instances[spec]

        if not spec in self._instances:
            PackageClass = self._get_pkg_class(spec.name)
            try:
                copy = spec.copy()
                self._instances[copy] = PackageClass(copy)
            except Exception, e:
                if spack.debug:
                    sys.excepthook(*sys.exc_info())
                raise FailedConstructorError(spec.name, *sys.exc_info())

        return self._instances[spec]


    def purge(self):
        """Clear entire package instance cache."""
        self._instances.clear()


    @_autospec
    def providers_for(self, vpkg_spec):
        if self._provider_index is None:
            self._provider_index = ProviderIndex(self.all_package_names())

        providers = self._provider_index.providers_for(vpkg_spec)
        if not providers:
            raise UnknownPackageError(vpkg_spec.name)
        return providers


    @_autospec
    def extensions_for(self, extendee_spec):
        return [p for p in self.all_packages() if p.extends(extendee_spec)]


    def dirname_for_package_name(self, pkg_name):
        """Get the directory name for a particular package.  This is the
           directory that contains its package.py file."""
        return join_path(self.root, pkg_name)


    def filename_for_package_name(self, pkg_name):
        """Get the filename for the module we should load for a particular
           package.  Packages for a Repo live in
           ``$root/<package_name>/package.py``

           This will return a proper package.py path even if the
           package doesn't exist yet, so callers will need to ensure
           the package exists before importing.
        """
        validate_module_name(pkg_name)
        pkg_dir = self.dirname_for_package_name(pkg_name)

        return join_path(pkg_dir, package_file_name)


    def all_package_names(self):
        """Returns a sorted list of all package names in the Repo."""
        if self._all_package_names is None:
            self._all_package_names = []

            for pkg_name in os.listdir(self.root):
                pkg_dir  = join_path(self.root, pkg_name)
                pkg_file = join_path(pkg_dir, package_file_name)
                if os.path.isfile(pkg_file):
                    self._all_package_names.append(pkg_name)

            self._all_package_names.sort()

        return self._all_package_names


    def all_packages(self):
        for name in self.all_package_names():
            yield self.get(name)


    def exists(self, pkg_name):
        """Whether a package with the supplied name exists."""
        # This does a binary search in the sorted list.
        idx = bisect_left(self.all_package_names(), pkg_name)
        return self._all_package_names[idx] == pkg_name


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
                raise UnknownPackageError(pkg_name, self.namespace)

            if not os.path.isfile(file_path):
                tty.die("Something's wrong. '%s' is not a file!" % file_path)

            if not os.access(file_path, os.R_OK):
                tty.die("Cannot read '%s'!" % file_path)

            fullname = "%s.%s" % (self.namespace, pkg_name)

            module = imp.load_source(fullname, file_path)
            module.__package__ = self.namespace
            module.__loader__ = self
            self._modules[pkg_name] = module

        return self._modules[pkg_name]


    def _get_pkg_class(self, pkg_name):
        """Get the class for the package out of its module.

        First loads (or fetches from cache) a module for the
        package. Then extracts the package class from the module
        according to Spack's naming convention.
        """
        class_name = mod_to_class(pkg_name)
        module = self._get_pkg_module(pkg_name)

        cls = getattr(module, class_name)
        if not inspect.isclass(cls):
            tty.die("%s.%s is not a class" % (pkg_name, class_name))

        return cls


    def __str__(self):
        return "<Repo '%s' from '%s'>" % (self.namespace, self.root)


    def __repr__(self):
        return self.__str__()


    def __contains__(self, pkg_name):
        return self.exists(pkg_name)


    #
    # Below functions deal with installed packages, and should be
    # moved to some other part of Spack (conbine with
    # directory_layout?)
    #
    @_autospec
    def get_installed(self, spec):
        """Get all the installed specs that satisfy the provided spec constraint."""
        return [s for s in self.installed_package_specs() if s.satisfies(spec)]


    @_autospec
    def installed_extensions_for(self, extendee_spec):
        for s in self.installed_package_specs():
            try:
                if s.package.extends(extendee_spec):
                    yield s.package
            except UnknownPackageError, e:
                # Skip packages we know nothing about
                continue


    def installed_package_specs(self):
        """Read installed package names straight from the install directory
           layout.
        """
        # Get specs from the directory layout but ensure that they're
        # all normalized properly.
        installed = []
        for spec in spack.install_layout.all_specs():
            spec.normalize()
            installed.append(spec)
        return installed


    def installed_known_package_specs(self):
        """Read installed package names straight from the install
           directory layout, but return only specs for which the
           package is known to this version of spack.
        """
        for spec in spack.install_layout.all_specs():
            if self.exists(spec.name):
                yield spec


class UnknownPackageError(spack.error.SpackError):
    """Raised when we encounter a package spack doesn't have."""
    def __init__(self, name, repo=None):
        msg = None
        if repo:
            msg = "Package %s not found in packagerepo %s." % (name, repo)
        else:
            msg = "Package %s not found." % name
        super(UnknownPackageError, self).__init__(msg)
        self.name = name


class DuplicateRepoError(spack.error.SpackError):
    """Raised when duplicate repos are added to a RepoPath."""
    def __init__(self, msg, repo1, repo2):
        super(UnknownPackageError, self).__init__(
            "%s: %s, %s" % (msg, repo1, repo2))


class FailedConstructorError(spack.error.SpackError):
    """Raised when a package's class constructor fails."""
    def __init__(self, name, exc_type, exc_obj, exc_tb):
        super(FailedConstructorError, self).__init__(
            "Class constructor failed for package '%s'." % name,
            '\nCaused by:\n' +
            ('%s: %s\n' % (exc_type.__name__, exc_obj)) +
            ''.join(traceback.format_tb(exc_tb)))
        self.name = name
