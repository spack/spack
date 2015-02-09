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
import re
import os
import exceptions
import hashlib
import shutil
from contextlib import closing

import llnl.util.tty as tty
from llnl.util.filesystem import join_path, mkdirp

import spack
from spack.spec import Spec
from spack.error import SpackError


def _check_concrete(spec):
    """If the spec is not concrete, raise a ValueError"""
    if not spec.concrete:
        raise ValueError('Specs passed to a DirectoryLayout must be concrete!')


class DirectoryLayout(object):
    """A directory layout is used to associate unique paths with specs.
       Different installations are going to want differnet layouts for their
       install, and they can use this to customize the nesting structure of
       spack installs.
    """
    def __init__(self, root):
        self.root = root


    @property
    def hidden_file_paths(self):
        """Return a list of hidden files used by the directory layout.

        Paths are relative to the root of an install directory.

        If the directory layout uses no hidden files to maintain
        state, this should return an empty container, e.g. [] or (,).

        """
        raise NotImplementedError()


    def all_specs(self):
        """To be implemented by subclasses to traverse all specs for which there is
           a directory within the root.
        """
        raise NotImplementedError()


    def relative_path_for_spec(self, spec):
        """Implemented by subclasses to return a relative path from the install
           root to a unique location for the provided spec."""
        raise NotImplementedError()


    def make_path_for_spec(self, spec):
        """Creates the installation directory for a spec."""
        raise NotImplementedError()


    def get_extensions(self, spec):
        """Get a set of currently installed extension packages for a spec."""
        raise NotImplementedError()


    def add_extension(self, spec, extension_spec):
        """Add to the list of currently installed extensions."""
        raise NotImplementedError()


    def remove_extension(self, spec, extension_spec):
        """Remove from the list of currently installed extensions."""
        raise NotImplementedError()


    def path_for_spec(self, spec):
        """Return an absolute path from the root to a directory for the spec."""
        _check_concrete(spec)

        path = self.relative_path_for_spec(spec)
        assert(not path.startswith(self.root))
        return os.path.join(self.root, path)


    def remove_path_for_spec(self, spec):
        """Removes a prefix and any empty parent directories from the root."""
        path = self.path_for_spec(spec)
        assert(path.startswith(self.root))

        if os.path.exists(path):
            shutil.rmtree(path, True)

        path = os.path.dirname(path)
        while path != self.root:
            if os.path.isdir(path):
                if os.listdir(path):
                    return
                os.rmdir(path)
            path = os.path.dirname(path)


def traverse_dirs_at_depth(root, depth, path_tuple=(), curdepth=0):
    """For each directory at <depth> within <root>, return a tuple representing
       the ancestors of that directory.
    """
    if curdepth == depth and curdepth != 0:
        yield path_tuple
    elif depth > curdepth:
        for filename in os.listdir(root):
            child = os.path.join(root, filename)
            if os.path.isdir(child):
                child_tuple = path_tuple + (filename,)
                for tup in traverse_dirs_at_depth(
                        child, depth, child_tuple, curdepth+1):
                    yield tup


class SpecHashDirectoryLayout(DirectoryLayout):
    """Lays out installation directories like this::
           <install_root>/
               <architecture>/
                   <compiler>/
                       name@version+variant-<dependency_hash>

       Where dependency_hash is a SHA-1 hash prefix for the full package spec.
       This accounts for dependencies.

       If there is ever a hash collision, you won't be able to install a new
       package unless you use a larger prefix.  However, the full spec is stored
       in a file called .spec in each directory, so you can migrate an entire
       install directory to a new hash size pretty easily.

       TODO: make a tool to migrate install directories to different hash sizes.
    """
    def __init__(self, root, **kwargs):
        """Prefix size is number of characters in the SHA-1 prefix to use
           to make each hash unique.
        """
        spec_file_name = kwargs.get('spec_file_name', '.spec')
        extension_file_name = kwargs.get('extension_file_name', '.extensions')
        super(SpecHashDirectoryLayout, self).__init__(root)
        self.spec_file_name = spec_file_name
        self.extension_file_name = extension_file_name


    @property
    def hidden_file_paths(self):
        return ('.spec', '.extensions')


    def relative_path_for_spec(self, spec):
        _check_concrete(spec)
        dir_name = spec.format('$_$@$+$#')
        return join_path(spec.architecture, spec.compiler, dir_name)


    def write_spec(self, spec, path):
        """Write a spec out to a file."""
        with closing(open(path, 'w')) as spec_file:
            spec_file.write(spec.tree(ids=False, cover='nodes'))


    def read_spec(self, path):
        """Read the contents of a file and parse them as a spec"""
        with closing(open(path)) as spec_file:
            # Specs from files are assumed normal and concrete
            spec = Spec(spec_file.read().replace('\n', ''))

        if all(spack.db.exists(s.name) for s in spec.traverse()):
            copy = spec.copy()
            copy.normalize()
            if copy.concrete:
                return copy   # These are specs spack still understands.

        # If we get here, either the spec is no longer in spack, or
        # something about its dependencies has changed. So we need to
        # just assume the read spec is correct.  We'll lose graph
        # information if we do this, but this is just for best effort
        # for commands like uninstall and find.  Currently Spack
        # doesn't do anything that needs the graph info after install.

        # TODO: store specs with full connectivity information, so
        # that we don't have to normalize or reconstruct based on
        # changing dependencies in the Spack tree.
        spec._normal = True
        spec._concrete = True
        return spec


    def spec_file_path(self, spec):
        """Gets full path to spec file"""
        _check_concrete(spec)
        return join_path(self.path_for_spec(spec), self.spec_file_name)


    def make_path_for_spec(self, spec):
        _check_concrete(spec)

        path = self.path_for_spec(spec)
        spec_file_path = self.spec_file_path(spec)

        if os.path.isdir(path):
            if not os.path.isfile(spec_file_path):
                raise InconsistentInstallDirectoryError(
                    'No spec file found at path %s' % spec_file_path)

            installed_spec = self.read_spec(spec_file_path)
            if installed_spec == self.spec:
                raise InstallDirectoryAlreadyExistsError(path)

            spec_hash = self.hash_spec(spec)
            installed_hash = self.hash_spec(installed_spec)
            if installed_spec == spec_hash:
                raise SpecHashCollisionError(installed_hash, spec_hash)
            else:
                raise InconsistentInstallDirectoryError(
                    'Spec file in %s does not match SHA-1 hash!'
                    % spec_file_path)

        mkdirp(path)
        self.write_spec(spec, spec_file_path)


    def all_specs(self):
        if not os.path.isdir(self.root):
            return

        for path in traverse_dirs_at_depth(self.root, 3):
            arch, compiler, last_dir = path
            spec_file_path = join_path(
                self.root, arch, compiler, last_dir, self.spec_file_name)
            if os.path.exists(spec_file_path):
                spec = self.read_spec(spec_file_path)
                yield spec


    def extension_file_path(self, spec):
        """Gets full path to an installed package's extension file"""
        _check_concrete(spec)
        return join_path(self.path_for_spec(spec), self.extension_file_name)


    def get_extensions(self, spec):
        _check_concrete(spec)

        extensions = set()
        path = self.extension_file_path(spec)
        if os.path.exists(path):
            with closing(open(path)) as ext_file:
                for line in ext_file:
                    try:
                        extensions.add(Spec(line.strip()))
                    except spack.error.SpackError, e:
                        raise InvalidExtensionSpecError(str(e))
        return extensions


    def write_extensions(self, spec, extensions):
        path = self.extension_file_path(spec)
        with closing(open(path, 'w')) as spec_file:
            for extension in sorted(extensions):
                spec_file.write("%s\n" % extension)


    def add_extension(self, spec, extension_spec):
        _check_concrete(spec)
        _check_concrete(extension_spec)

        exts = self.get_extensions(spec)
        if extension_spec in exts:
            raise ExtensionAlreadyInstalledError(spec, extension_spec)
        else:
            for already_installed in exts:
                if spec.name == extension_spec.name:
                    raise ExtensionConflictError(spec, extension_spec, already_installed)

        exts.add(extension_spec)
        self.write_extensions(spec, exts)


    def remove_extension(self, spec, extension_spec):
        _check_concrete(spec)
        _check_concrete(extension_spec)

        exts = self.get_extensions(spec)
        if not extension_spec in exts:
            raise NoSuchExtensionError(spec, extension_spec)

        exts.remove(extension_spec)
        self.write_extensions(spec, exts)


class DirectoryLayoutError(SpackError):
    """Superclass for directory layout errors."""
    def __init__(self, message):
        super(DirectoryLayoutError, self).__init__(message)


class SpecHashCollisionError(DirectoryLayoutError):
    """Raised when there is a hash collision in an SpecHashDirectoryLayout."""
    def __init__(self, installed_spec, new_spec):
        super(SpecHashDirectoryLayout, self).__init__(
            'Specs %s and %s have the same SHA-1 prefix!'
            % installed_spec, new_spec)


class InconsistentInstallDirectoryError(DirectoryLayoutError):
    """Raised when a package seems to be installed to the wrong place."""
    def __init__(self, message):
        super(InconsistentInstallDirectoryError, self).__init__(message)


class InstallDirectoryAlreadyExistsError(DirectoryLayoutError):
    """Raised when make_path_for_sec is called unnecessarily."""
    def __init__(self, path):
        super(InstallDirectoryAlreadyExistsError, self).__init__(
            "Install path %s already exists!")


class InvalidExtensionSpecError(DirectoryLayoutError):
    """Raised when an extension file has a bad spec in it."""
    def __init__(self, message):
        super(InvalidExtensionSpecError, self).__init__(message)


class ExtensionAlreadyInstalledError(DirectoryLayoutError):
    """Raised when an extension is added to a package that already has it."""
    def __init__(self, spec, extension_spec):
        super(ExtensionAlreadyInstalledError, self).__init__(
            "%s is already installed in %s" % (extension_spec.short_spec, spec.short_spec))


class ExtensionConflictError(DirectoryLayoutError):
    """Raised when an extension is added to a package that already has it."""
    def __init__(self, spec, extension_spec, conflict):
        super(ExtensionConflictError, self).__init__(
            "%s cannot be installed in %s because it conflicts with %s."% (
                extension_spec.short_spec, spec.short_spec, conflict.short_spec))


class NoSuchExtensionError(DirectoryLayoutError):
    """Raised when an extension isn't there on remove."""
    def __init__(self, spec, extension_spec):
        super(NoSuchExtensionError, self).__init__(
            "%s cannot be removed from %s because it's not installed."% (
                extension_spec.short_spec, spec.short_spec))
