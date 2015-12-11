##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import sys
import inspect
import glob
import imp

import llnl.util.tty as tty
from llnl.util.filesystem import join_path
from llnl.util.lang import *

import spack.error
import spack.spec
from spack.virtual import ProviderIndex
from spack.util.naming import mod_to_class, validate_module_name

# Name of module under which packages are imported
_imported_packages_module = 'spack.packages'

# Name of the package file inside a package directory
_package_file_name = 'package.py'


def _autospec(function):
    """Decorator that automatically converts the argument of a single-arg
       function to a Spec."""
    def converter(self, spec_like, **kwargs):
        if not isinstance(spec_like, spack.spec.Spec):
            spec_like = spack.spec.Spec(spec_like)
        return function(self, spec_like, **kwargs)
    return converter


class PackageDB(object):
    def __init__(self, root):
        """Construct a new package database from a root directory."""
        self.root = root
        self.instances = {}
        self.provider_index = None


    @_autospec
    def get(self, spec, **kwargs):
        if spec.virtual:
            raise UnknownPackageError(spec.name)

        key = hash(spec)
        if kwargs.get('new', False):
            if key in self.instances:
                del self.instances[key]

        if not key in self.instances:
            package_class = self.get_class_for_package_name(spec.name)
            try:
                copy = spec.copy() # defensive copy.  Package owns its spec.
                self.instances[key] = package_class(copy)
            except Exception, e:
                if spack.debug:
                    sys.excepthook(*sys.exc_info())
                raise FailedConstructorError(spec.name, e)

        return self.instances[key]


    @_autospec
    def delete(self, spec):
        """Force a package to be recreated."""
        del self.instances[spec.dag_hash()]


    def purge(self):
        """Clear entire package instance cache."""
        self.instances.clear()


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
        return join_path(pkg_dir, _package_file_name)


    @memoized
    def all_package_names(self):
        """Generator function for all packages.  This looks for
           ``<pkg_name>/package.py`` files within the root direcotry"""
        all_package_names = []
        for pkg_name in os.listdir(self.root):
            pkg_dir  = join_path(self.root, pkg_name)
            pkg_file = join_path(pkg_dir, _package_file_name)
            if os.path.isfile(pkg_file):
                all_package_names.append(pkg_name)
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
    def get_class_for_package_name(self, pkg_name):
        """Get an instance of the class for a particular package.

           This method uses Python's ``imp`` package to load python
           source from a Spack package's ``package.py`` file.  A
           normal python import would only load each package once, but
           because we do this dynamically, the method needs to be
           memoized to ensure there is only ONE package class
           instance, per package, per database.
        """
        file_path = self.filename_for_package_name(pkg_name)

        if os.path.exists(file_path):
            if not os.path.isfile(file_path):
                tty.die("Something's wrong. '%s' is not a file!" % file_path)
            if not os.access(file_path, os.R_OK):
                tty.die("Cannot read '%s'!" % file_path)
        else:
            raise UnknownPackageError(pkg_name)

        class_name = mod_to_class(pkg_name)
        try:
            module_name = _imported_packages_module + '.' + pkg_name
            module = imp.load_source(module_name, file_path)

        except ImportError, e:
            tty.die("Error while importing %s from %s:\n%s" % (
                pkg_name, file_path, e.message))

        cls = getattr(module, class_name)
        if not inspect.isclass(cls):
            tty.die("%s.%s is not a class" % (pkg_name, class_name))

        return cls


class UnknownPackageError(spack.error.SpackError):
    """Raised when we encounter a package spack doesn't have."""
    def __init__(self, name):
        super(UnknownPackageError, self).__init__("Package '%s' not found." % name)
        self.name = name


class FailedConstructorError(spack.error.SpackError):
    """Raised when a package's class constructor fails."""
    def __init__(self, name, reason):
        super(FailedConstructorError, self).__init__(
            "Class constructor failed for package '%s'." % name,
            str(reason))
        self.name = name
