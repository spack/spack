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


class NamespaceTrie(object):
    def __init__(self):
        self._elements = {}


    def __setitem__(self, namespace, repo):
        parts = namespace.split('.')
        cur = self._elements
        for p in parts[:-1]:
            if p not in cur:
                cur[p] = {}
            cur = cur[p]

        cur[parts[-1]] = repo


    def __getitem__(self, namespace):
        parts = namespace.split('.')
        cur = self._elements
        for p in parts:
            if p not in cur:
                raise KeyError("Can't find namespace %s in trie" % namespace)
            cur = cur[p]
        return cur


    def __contains__(self, namespace):
        parts = namespace.split('.')
        cur = self._elements
        for p in parts:
            if not isinstance(cur, dict):
                return False
            if p not in cur:
                return False
            cur  = cur[p]
        return True



class PackageFinder(object):
    """A PackageFinder is a wrapper around a list of PackageDBs.

       It functions exactly like a PackageDB, but it operates on the
       combined results of the PackageDBs in its list instead of on a
       single package repository.
    """
    def __init__(self, *repo_dirs):
        self.repos = []
        self.by_namespace = NamespaceTrie()
        self.by_path = {}

        for root in repo_dirs:
            repo = PackageDB(root)
            self.put_last(repo)


    def _check_repo(self, repo):
        if repo.root in self.by_path:
            raise DuplicateRepoError("Package repos are the same",
                                     repo, self.by_path[repo.root])

        if repo.namespace in self.by_namespace:
            tty.error("Package repos cannot have the same name",
                      repo, self.by_namespace[repo.namespace])


    def _add(self, repo):
        self._check_repo(repo)
        self.by_namespace[repo.namespace] = repo
        self.by_path[repo.root] = repo


    def put_first(self, repo):
        self._add(repo)
        self.repos.insert(0, repo)


    def put_last(self, repo):
        self._add(repo)
        self.repos.append(repo)


    def remove(self, repo):
        if repo in self.repos:
            self.repos.remove(repo)


    def swap(self, other):
        repos = self.repos
        by_namespace = self.by_namespace
        by_path = self.by_path

        self.repos = other.repos
        self.by_namespace = other.by_namespace
        self.by_pah = other.by_path

        other.repos = repos
        other.by_namespace = by_namespace
        other.by_path = by_path


    def all_package_names(self):
        all_pkgs = set()
        for repo in self.repos:
            all_pkgs.update(set(repo.all_package_names()))
        return all_pkgs


    def all_packages(self):
        for name in self.all_package_names():
            yield self.get(name)


    def providers_for(self, vpkg_name):
        # TODO: USE MORE THAN FIRST REPO
        return self.repos[0].providers_for(vpkg_name)


    def _get_spack_pkg_name(self, repo, py_module_name):
        """Allow users to import Spack packages using legal Python identifiers.

        A python identifier might map to many different Spack package
        names due to hyphen/underscore ambiguity.

        Easy example:
            num3proxy   -> 3proxy

        Ambiguous:
            foo_bar -> foo_bar, foo-bar

        More ambiguous:
            foo_bar_baz -> foo_bar_baz, foo-bar-baz, foo_bar-baz, foo-bar_baz
        """
        if py_module_name in repo:
            return py_module_name

        options = possible_spack_module_names(py_module_name)
        options.remove(py_module_name)
        for name in options:
            if name in repo:
                return name

        return None


    def find_module(self, fullname, path=None):
        if fullname in self.by_namespace:
            return self

        namespace, dot, module_name = fullname.rpartition('.')
        if namespace not in self.by_namespace:
            return None

        repo = self.by_namespace[namespace]
        name = self._get_spack_pkg_name(repo, module_name)
        if not name:
            return None

        return self


    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]

        if fullname in self.by_namespace:
            ns = self.by_namespace[fullname]
            module = imp.new_module(fullname)
            module.__file__ = "<spack-namespace>"
            module.__path__ = []
            module.__package__ = fullname

        else:
            namespace, dot, module_name = fullname.rpartition('.')
            if namespace not in self.by_namespace:
                raise ImportError(
                    "No Spack repository with namespace %s" % namespace)

            repo = self.by_namespace[namespace]
            name = self._get_spack_pkg_name(repo, module_name)
            if not name:
                raise ImportError(
                    "No module %s in Spack repository %s" % (module_name, repo))

            fullname = namespace + '.' + name
            file_path = os.path.join(repo.root, name, package_file_name)
            module = imp.load_source(fullname, file_path)
            module.__package__ = namespace

        module.__loader__ = self
        sys.modules[fullname] = module
        return module


    @_autospec
    def get(self, spec, new=False):
        for repo in self.repos:
            if spec.name in repo:
                return repo.get(spec, new)
        raise UnknownPackageError(spec.name)


    def get_repo(self, namespace):
        if namespace in self.by_namespace:
            repo = self.by_namespace[namespace]
            if isinstance(repo, PackageDB):
                return repo
        return None


    def exists(self, pkg_name):
        return any(repo.exists(pkg_name) for repo in self.repos)


    def __contains__(self, pkg_name):
        return self.exists(pkg_name)



class PackageDB(object):
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

        # These are internal cache variables.
        self._instances = {}
        self._provider_index = None


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

        if new:
            if spec in self._instances:
                del self._instances[spec]

        if not spec in self._instances:
            package_class = self.get_class_for_package_name(spec.name, spec.repo)
            try:
                copy = spec.copy()
                self._instances[copy] = package_class(copy)
            except Exception, e:
                if spack.debug:
                    sys.excepthook(*sys.exc_info())
                raise FailedConstructorError(spec.name, *sys.exc_info())

        return self._instances[spec]


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
           package.  Packages for a pacakge DB live in
           ``$root/<package_name>/package.py``

           This will return a proper package.py path even if the
           package doesn't exist yet, so callers will need to ensure
           the package exists before importing.
        """
        validate_module_name(pkg_name)
        pkg_dir = self.dirname_for_package_name(pkg_name)
        return join_path(pkg_dir, package_file_name)


    @memoized
    def all_package_names(self):
        """Generator function for all packages.  This looks for
           ``<pkg_name>/package.py`` files within the repo direcotories"""
        all_package_names = []

        for pkg_name in os.listdir(self.root):
            pkg_dir  = join_path(self.root, pkg_name)
            pkg_file = join_path(pkg_dir, package_file_name)
            if os.path.isfile(pkg_file):
                all_package_names.append(pkg_name)

        return sorted(all_package_names)


    def all_packages(self):
        for name in self.all_package_names():
            yield self.get(name)


    @memoized
    def exists(self, pkg_name):
        """Whether a package with the supplied name exists."""
        return os.path.exists(self.filename_for_package_name(pkg_name))


    @memoized
    def get_class_for_package_name(self, pkg_name, reponame = None):
        """Get an instance of the class for a particular package."""
        file_path = self.filename_for_package_name(pkg_name)

        if os.path.exists(file_path):
            if not os.path.isfile(file_path):
                tty.die("Something's wrong. '%s' is not a file!" % file_path)
            if not os.access(file_path, os.R_OK):
                tty.die("Cannot read '%s'!" % file_path)
        else:
            raise UnknownPackageError(pkg_name, self.namespace)

        class_name = mod_to_class(pkg_name)
        module = __import__(self.namespace + '.' + pkg_name, fromlist=[class_name])
        cls = getattr(module, class_name)
        if not inspect.isclass(cls):
            tty.die("%s.%s is not a class" % (pkg_name, class_name))

        return cls


    def __str__(self):
        return "<PackageDB '%s' from '%s'>" % (self.namespace, self.root)


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
    """Raised when duplicate repos are added to a PackageFinder."""
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
