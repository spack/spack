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
import spack.config
import re
from contextlib import closing

import llnl.util.tty as tty
from llnl.util.filesystem import join_path
from llnl.util.lang import *

import spack.error
import spack.spec
from spack.virtual import ProviderIndex
from spack.util.naming import mod_to_class, validate_module_name
from sets import Set
from spack.repo_loader import RepoLoader, imported_packages_module, package_file_name

# Filename for package repo names
_packagerepo_filename = 'reponame'

def _autospec(function):
    """Decorator that automatically converts the argument of a single-arg
       function to a Spec."""
    def converter(self, spec_like, **kwargs):
        if not isinstance(spec_like, spack.spec.Spec):
            spec_like = spack.spec.Spec(spec_like)
        return function(self, spec_like, **kwargs)
    return converter


class PackageDB(object):
    def __init__(self, default_root):
        """Construct a new package database from a root directory."""

        #Collect the repos from the config file and read their names from the file system
        repo_dirs = self._repo_list_from_config()
        repo_dirs.append(default_root)
        self.repos = [(self._read_reponame_from_directory(dir), dir) for dir in repo_dirs]

        # Check for duplicate repo names
        s = set()
        dups = set(r for r in self.repos if r[0] in s or s.add(r[0]))
        if dups:
            reponame = list(dups)[0][0]
            dir1 = list(dups)[0][1]
            dir2 = dict(s)[reponame]
            tty.die("Package repo %s in directory %s has the same name as the "
                      "repo in directory %s" %
                      (reponame, dir1, dir2))

        # For each repo, create a RepoLoader
        self.repo_loaders = dict([(r[0], RepoLoader(r[0], r[1])) for r in self.repos])

        self.instances = {}
        self.provider_index = None


    def _read_reponame_from_directory(self, dir):
        """For a packagerepo directory, read the repo name from the dir/reponame file"""
        path = os.path.join(dir, 'reponame')

        try:
            with closing(open(path, 'r')) as reponame_file:
                name = reponame_file.read().lstrip().rstrip()
                if not re.match(r'[a-zA-Z][a-zA-Z0-9]+', name):
                    tty.die("Package repo name '%s', read from %s, is an invalid name. "
                            "Repo names must began with a letter and only contain letters "
                            "and numbers." % (name, path))
                return name
        except exceptions.IOError, e:
            tty.die("Could not read from package repo name file %s" % path)



    def _repo_list_from_config(self):
        """Read through the spackconfig and return the list of packagerepo directories"""
        config = spack.config.get_config()
        if not config.has_option('packagerepo', 'directories'): return []
        dir_string = config.get('packagerepo', 'directories')
        return dir_string.split(':')


    @_autospec
    def get(self, spec, **kwargs):
        if spec.virtual:
            raise UnknownPackageError(spec.name)

        if kwargs.get('new', False):
            if spec in self.instances:
                del self.instances[spec]

        if not spec in self.instances:
            package_class = self.get_class_for_package_name(spec.name, spec.repo)
            try:
                copy = spec.copy()
                self.instances[copy] = package_class(copy)
            except Exception, e:
                if spack.debug:
                    sys.excepthook(*sys.exc_info())
                raise FailedConstructorError(spec.name, e)

        return self.instances[spec]


    @_autospec
    def delete(self, spec):
        """Force a package to be recreated."""
        del self.instances[spec]


    def purge(self):
        """Clear entire package instance cache."""
        self.instances.clear()


    @_autospec
    def get_installed(self, spec):
        """Get all the installed specs that satisfy the provided spec constraint."""
        return [s for s in self.installed_package_specs() if s.satisfies(spec)]


    @_autospec
    def providers_for(self, vpkg_spec):
        if self.provider_index is None:
            self.provider_index = ProviderIndex(self.all_package_names())

        providers = self.provider_index.providers_for(vpkg_spec)
        if not providers:
            raise UnknownPackageError(vpkg_spec.name)
        return providers


    @_autospec
    def extensions_for(self, extendee_spec):
        return [p for p in self.all_packages() if p.extends(extendee_spec)]


    @_autospec
    def installed_extensions_for(self, extendee_spec):
        for s in self.installed_package_specs():
            try:
                if s.package.extends(extendee_spec):
                    yield s.package
            except UnknownPackageError, e:
                # Skip packages we know nothing about
                continue
                # TODO: add some conditional way to do this instead of
                # catching exceptions.


    def repo_for_package_name(self, pkg_name, packagerepo_name=None):
        """Find the dirname for a package and the packagerepo it came from
           if packagerepo_name is not None, then search for the package in the
           specified packagerepo"""
        #Look for an existing package under any matching packagerepos
        roots = [pkgrepo for pkgrepo in self.repos
                 if not packagerepo_name or packagerepo_name == pkgrepo[0]]

        if not roots:
            tty.die("Package repo %s does not exist" % packagerepo_name)

        for pkgrepo in roots:
            path = join_path(pkgrepo[1], pkg_name)
            if os.path.exists(path):
                return (pkgrepo[0], path)

        repo_to_add_to = roots[-1]
        return (repo_to_add_to[0], join_path(repo_to_add_to[1], pkg_name))


    def dirname_for_package_name(self, pkg_name, packagerepo_name=None):
        """Get the directory name for a particular package.  This is the
           directory that contains its package.py file."""
        return self.repo_for_package_name(pkg_name, packagerepo_name)[1]


    def filename_for_package_name(self, pkg_name, packagerepo_name=None):
        """Get the filename for the module we should load for a particular
           package.  Packages for a pacakge DB live in
           ``$root/<package_name>/package.py``

           This will return a proper package.py path even if the
           package doesn't exist yet, so callers will need to ensure
           the package exists before importing.

           If a packagerepo is specified, then return existing
           or new paths in the specified packagerepo directory.  If no
           package repo is supplied, return an existing path from any
           package repo, and new paths in the default package repo.
        """
        validate_module_name(pkg_name)
        pkg_dir = self.dirname_for_package_name(pkg_name, packagerepo_name)
        return join_path(pkg_dir, package_file_name)


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


    @memoized
    def all_package_names(self):
        """Generator function for all packages.  This looks for
           ``<pkg_name>/package.py`` files within the repo direcotories"""
        all_packages = Set()
        for repo in self.repos:
            dir = repo[1]
            if not os.path.isdir(dir):
                continue
            for pkg_name in os.listdir(dir):
                pkg_dir  = join_path(dir, pkg_name)
                pkg_file = join_path(pkg_dir, package_file_name)
                if os.path.isfile(pkg_file):
                    all_packages.add(pkg_name)
        all_package_names = list(all_packages)
        all_package_names.sort()
        return all_package_names


    def all_packages(self):
        for name in self.all_package_names():
            yield self.get(name)


    @memoized
    def exists(self, pkg_name):
        """Whether a package with the supplied name exists ."""
        return os.path.exists(self.filename_for_package_name(pkg_name))


    @memoized
    def get_class_for_package_name(self, pkg_name, reponame = None):
        """Get an instance of the class for a particular package."""
        (reponame, repodir) = self.repo_for_package_name(pkg_name, reponame)
        module_name = imported_packages_module + '.' + reponame + '.' + pkg_name

        module = self.repo_loaders[reponame].get_module(pkg_name)

        class_name = mod_to_class(pkg_name)
        cls = getattr(module, class_name)
        if not inspect.isclass(cls):
            tty.die("%s.%s is not a class" % (pkg_name, class_name))

        return cls


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


class FailedConstructorError(spack.error.SpackError):
    """Raised when a package's class constructor fails."""
    def __init__(self, name, reason):
        super(FailedConstructorError, self).__init__(
            "Class constructor failed for package '%s'." % name,
            str(reason))
        self.name = name
