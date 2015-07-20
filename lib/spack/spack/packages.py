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
import itertools
import traceback
from external import yaml

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
repo_config = 'repo.yaml'

def _autospec(function):
    """Decorator that automatically converts the argument of a single-arg
       function to a Spec."""
    def converter(self, spec_like, **kwargs):
        if not isinstance(spec_like, spack.spec.Spec):
            spec_like = spack.spec.Spec(spec_like)
        return function(self, spec_like, **kwargs)
    return converter


def sliding_window(seq, n):
    it = iter(seq)
    result = tuple(itertools.islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


class PackageDB(object):
    def __init__(self, *repo_dirs):
        """Construct a new package database from a list of directories.

        Args:
          repo_dirs   List of directories containing packages.

        If ``repo_dirs`` is empty, gets repository list from Spack configuration.
        """
        if not repo_dirs:
            repo_dirs = spack.config.get_repos_config()
            if not repo_dirs:
                tty.die("Spack configuration contains no package repositories.")

        # Collect the repos from the config file and read their names
        # from the file system
        repo_dirs = [spack.config.substitute_spack_prefix(rd) for rd in repo_dirs]

        self.repos = []
        for rdir in repo_dirs:
            rname = self._read_reponame_from_directory(rdir)
            if rname:
                self.repos.append((self._read_reponame_from_directory(rdir), rdir))


        by_path = sorted(self.repos, key=lambda r:r[1])
        by_name = sorted(self.repos, key=lambda r:r[0])

        for r1, r2 in by_path:
            if r1[1] == r2[1]:
                tty.die("Package repos are the same:",
                        "  %20s  %s" % r1, "  %20s %s" % r2)

        for r1, r2 in by_name:
            if r1[0] == r2[0]:
                tty.die("Package repos cannot have the same name:",
                        "  %20s  %s" % r1, "  %20s %s" % r2)

        # For each repo, create a RepoLoader
        self.repo_loaders = dict((name, RepoLoader(name, path))
                                 for name, path in self.repos)

        self.instances = {}
        self.provider_index = None


    def _read_reponame_from_directory(self, dir):
        """For a packagerepo directory, read the repo name from the
        $root/repo.yaml file"""
        path = os.path.join(dir, repo_config)

        try:
            with open(path) as reponame_file:
                yaml_data = yaml.load(reponame_file)

                if (not yaml_data or
                    'repo' not in yaml_data or
                    'namespace' not in yaml_data['repo']):
                    tty.die("Invalid %s in %s" % (repo_config, dir))

                name = yaml_data['repo']['namespace']
                if not re.match(r'[a-zA-Z][a-zA-Z0-9_.]+', name):
                    tty.die(
                        "Package repo name '%s', read from %s, is an invalid name. "
                        "Repo names must began with a letter and only contain "
                        "letters and numbers." % (name, path))
                return name
        except exceptions.IOError, e:
            tty.die("Error reading %s when opening %s" % (repo_config, dir))


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
                raise FailedConstructorError(spec.name, *sys.exc_info())

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
    def __init__(self, name, exc_type, exc_obj, exc_tb):
        super(FailedConstructorError, self).__init__(
            "Class constructor failed for package '%s'." % name,
            '\nCaused by:\n' +
            ('%s: %s\n' % (exc_type.__name__, exc_obj)) +
            ''.join(traceback.format_tb(exc_tb)))
        self.name = name
