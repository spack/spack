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
import shutil
import glob
import tempfile
import yaml

from llnl.util.filesystem import join_path, mkdirp

import spack
import spack.spec
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

    def create_install_directory(self, spec):
        """Creates the installation directory for a spec."""
        raise NotImplementedError()

    def check_installed(self, spec):
        """Checks whether a spec is installed.

        Return the spec's prefix, if it is installed, None otherwise.

        Raise an exception if the install is inconsistent or corrupt.
        """
        raise NotImplementedError()

    def extension_map(self, spec):
        """Get a dict of currently installed extension packages for a spec.

           Dict maps { name : extension_spec }
           Modifying dict does not affect internals of this layout.
        """
        raise NotImplementedError()

    def check_extension_conflict(self, spec, ext_spec):
        """Ensure that ext_spec can be activated in spec.

           If not, raise ExtensionAlreadyInstalledError or
           ExtensionConflictError.
        """
        raise NotImplementedError()

    def check_activated(self, spec, ext_spec):
        """Ensure that ext_spec can be removed from spec.

           If not, raise NoSuchExtensionError.
        """
        raise NotImplementedError()

    def add_extension(self, spec, ext_spec):
        """Add to the list of currently installed extensions."""
        raise NotImplementedError()

    def remove_extension(self, spec, ext_spec):
        """Remove from the list of currently installed extensions."""
        raise NotImplementedError()

    def path_for_spec(self, spec):
        """Return absolute path from the root to a directory for the spec."""
        _check_concrete(spec)

        path = self.relative_path_for_spec(spec)
        assert(not path.startswith(self.root))
        return os.path.join(self.root, path)

    def remove_install_directory(self, spec):
        """Removes a prefix and any empty parent directories from the root.
           Raised RemoveFailedError if something goes wrong.
        """
        path = self.path_for_spec(spec)
        assert(path.startswith(self.root))

        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except OSError as e:
                raise RemoveFailedError(spec, path, e)

        path = os.path.dirname(path)
        while path != self.root:
            if os.path.isdir(path):
                if os.listdir(path):
                    return
                os.rmdir(path)
            path = os.path.dirname(path)


class YamlDirectoryLayout(DirectoryLayout):
    """Lays out installation directories like this::
           <install root>/
               <platform-os-target>/
                   <compiler>-<compiler version>/
                       <name>-<version>-<variants>-<hash>

       The hash here is a SHA-1 hash for the full DAG plus the build
       spec.  TODO: implement the build spec.

       To avoid special characters (like ~) in the directory name,
       only enabled variants are included in the install path.
       Disabled variants are omitted.
    """

    def __init__(self, root, **kwargs):
        super(YamlDirectoryLayout, self).__init__(root)
        self.metadata_dir   = kwargs.get('metadata_dir', '.spack')
        self.hash_len       = kwargs.get('hash_len', None)

        self.spec_file_name      = 'spec.yaml'
        self.extension_file_name = 'extensions.yaml'
        self.build_log_name      = 'build.out'  # build log.
        self.build_env_name      = 'build.env'  # build environment
        self.packages_dir        = 'repos'      # archive of package.py files

        # Cache of already written/read extension maps.
        self._extension_maps = {}

    @property
    def hidden_file_paths(self):
        return (self.metadata_dir,)

    def relative_path_for_spec(self, spec):
        _check_concrete(spec)

        if spec.external:
            return spec.external

        dir_name = "%s-%s-%s" % (
            spec.name,
            spec.version,
            spec.dag_hash(self.hash_len))

        path = join_path(
            spec.architecture,
            "%s-%s" % (spec.compiler.name, spec.compiler.version),
            dir_name)

        return path

    def write_spec(self, spec, path):
        """Write a spec out to a file."""
        _check_concrete(spec)
        with open(path, 'w') as f:
            spec.to_yaml(f)

    def read_spec(self, path):
        """Read the contents of a file and parse them as a spec"""
        try:
            with open(path) as f:
                spec = spack.spec.Spec.from_yaml(f)
        except Exception as e:
            if spack.debug:
                raise
            raise SpecReadError(
                'Unable to read file: %s' % path, 'Cause: ' + str(e))

        # Specs read from actual installations are always concrete
        spec._mark_concrete()
        return spec

    def spec_file_path(self, spec):
        """Gets full path to spec file"""
        _check_concrete(spec)
        return join_path(self.metadata_path(spec), self.spec_file_name)

    def metadata_path(self, spec):
        return join_path(self.path_for_spec(spec), self.metadata_dir)

    def build_log_path(self, spec):
        return join_path(self.path_for_spec(spec), self.metadata_dir,
                         self.build_log_name)

    def build_env_path(self, spec):
        return join_path(self.path_for_spec(spec), self.metadata_dir,
                         self.build_env_name)

    def build_packages_path(self, spec):
        return join_path(self.path_for_spec(spec), self.metadata_dir,
                         self.packages_dir)

    def create_install_directory(self, spec):
        _check_concrete(spec)

        prefix = self.check_installed(spec)
        if prefix:
            raise InstallDirectoryAlreadyExistsError(prefix)

        mkdirp(self.metadata_path(spec))
        self.write_spec(spec, self.spec_file_path(spec))

    def check_installed(self, spec):
        _check_concrete(spec)
        path = self.path_for_spec(spec)
        spec_file_path = self.spec_file_path(spec)

        if not os.path.isdir(path):
            return None

        if not os.path.isfile(spec_file_path):
            raise InconsistentInstallDirectoryError(
                'Install prefix exists but contains no spec.yaml:',
                "  " + path)

        installed_spec = self.read_spec(spec_file_path)
        if installed_spec == spec:
            return path

        # DAG hashes currently do not include build dependencies.
        #
        # TODO: remove this when we do better concretization and don't
        # ignore build-only deps in hashes.
        elif installed_spec == spec.copy(deps=('link', 'run')):
            return path

        if spec.dag_hash() == installed_spec.dag_hash():
            raise SpecHashCollisionError(spec, installed_spec)
        else:
            raise InconsistentInstallDirectoryError(
                'Spec file in %s does not match hash!' % spec_file_path)

    def all_specs(self):
        if not os.path.isdir(self.root):
            return []

        pattern = join_path(
            self.root, '*', '*', '*', self.metadata_dir, self.spec_file_name)
        spec_files = glob.glob(pattern)
        return [self.read_spec(s) for s in spec_files]

    def specs_by_hash(self):
        by_hash = {}
        for spec in self.all_specs():
            by_hash[spec.dag_hash()] = spec
        return by_hash

    def extension_file_path(self, spec):
        """Gets full path to an installed package's extension file"""
        _check_concrete(spec)
        return join_path(self.metadata_path(spec), self.extension_file_name)

    def _write_extensions(self, spec, extensions):
        path = self.extension_file_path(spec)

        # Create a temp file in the same directory as the actual file.
        dirname, basename = os.path.split(path)
        tmp = tempfile.NamedTemporaryFile(
            prefix=basename, dir=dirname, delete=False)

        # write tmp file
        with tmp:
            yaml.dump({
                'extensions': [
                    {ext.name: {
                        'hash': ext.dag_hash(),
                        'path': str(ext.prefix)
                    }} for ext in sorted(extensions.values())]
            }, tmp, default_flow_style=False)

        # Atomic update by moving tmpfile on top of old one.
        os.rename(tmp.name, path)

    def _extension_map(self, spec):
        """Get a dict<name -> spec> for all extensions currently
           installed for this package."""
        _check_concrete(spec)

        if spec not in self._extension_maps:
            path = self.extension_file_path(spec)
            if not os.path.exists(path):
                self._extension_maps[spec] = {}

            else:
                by_hash = self.specs_by_hash()
                exts = {}
                with open(path) as ext_file:
                    yaml_file = yaml.load(ext_file)
                    for entry in yaml_file['extensions']:
                        name = next(iter(entry))
                        dag_hash = entry[name]['hash']
                        prefix   = entry[name]['path']

                        if dag_hash not in by_hash:
                            raise InvalidExtensionSpecError(
                                "Spec %s not found in %s" % (dag_hash, prefix))

                        ext_spec = by_hash[dag_hash]
                        if prefix != ext_spec.prefix:
                            raise InvalidExtensionSpecError(
                                "Prefix %s does not match spec hash %s: %s"
                                % (prefix, dag_hash, ext_spec))

                        exts[ext_spec.name] = ext_spec
                self._extension_maps[spec] = exts

        return self._extension_maps[spec]

    def extension_map(self, spec):
        """Defensive copying version of _extension_map() for external API."""
        _check_concrete(spec)
        return self._extension_map(spec).copy()

    def check_extension_conflict(self, spec, ext_spec):
        exts = self._extension_map(spec)
        if ext_spec.name in exts:
            installed_spec = exts[ext_spec.name]
            if ext_spec == installed_spec:
                raise ExtensionAlreadyInstalledError(spec, ext_spec)
            else:
                raise ExtensionConflictError(spec, ext_spec, installed_spec)

    def check_activated(self, spec, ext_spec):
        exts = self._extension_map(spec)
        if (ext_spec.name not in exts) or (ext_spec != exts[ext_spec.name]):
            raise NoSuchExtensionError(spec, ext_spec)

    def add_extension(self, spec, ext_spec):
        _check_concrete(spec)
        _check_concrete(ext_spec)

        # Check whether it's already installed or if it's a conflict.
        exts = self._extension_map(spec)
        self.check_extension_conflict(spec, ext_spec)

        # do the actual adding.
        exts[ext_spec.name] = ext_spec
        self._write_extensions(spec, exts)

    def remove_extension(self, spec, ext_spec):
        _check_concrete(spec)
        _check_concrete(ext_spec)

        # Make sure it's installed before removing.
        exts = self._extension_map(spec)
        self.check_activated(spec, ext_spec)

        # do the actual removing.
        del exts[ext_spec.name]
        self._write_extensions(spec, exts)


class DirectoryLayoutError(SpackError):
    """Superclass for directory layout errors."""

    def __init__(self, message, long_msg=None):
        super(DirectoryLayoutError, self).__init__(message, long_msg)


class SpecHashCollisionError(DirectoryLayoutError):
    """Raised when there is a hash collision in an install layout."""

    def __init__(self, installed_spec, new_spec):
        super(SpecHashCollisionError, self).__init__(
            'Specs %s and %s have the same SHA-1 prefix!'
            % (installed_spec, new_spec))


class RemoveFailedError(DirectoryLayoutError):
    """Raised when a DirectoryLayout cannot remove an install prefix."""

    def __init__(self, installed_spec, prefix, error):
        super(RemoveFailedError, self).__init__(
            'Could not remove prefix %s for %s : %s'
            % (prefix, installed_spec.short_spec, error))
        self.cause = error


class InconsistentInstallDirectoryError(DirectoryLayoutError):
    """Raised when a package seems to be installed to the wrong place."""

    def __init__(self, message, long_msg=None):
        super(InconsistentInstallDirectoryError, self).__init__(
            message, long_msg)


class InstallDirectoryAlreadyExistsError(DirectoryLayoutError):
    """Raised when create_install_directory is called unnecessarily."""

    def __init__(self, path):
        super(InstallDirectoryAlreadyExistsError, self).__init__(
            "Install path %s already exists!")


class SpecReadError(DirectoryLayoutError):
    """Raised when directory layout can't read a spec."""


class InvalidExtensionSpecError(DirectoryLayoutError):
    """Raised when an extension file has a bad spec in it."""


class ExtensionAlreadyInstalledError(DirectoryLayoutError):
    """Raised when an extension is added to a package that already has it."""

    def __init__(self, spec, ext_spec):
        super(ExtensionAlreadyInstalledError, self).__init__(
            "%s is already installed in %s"
            % (ext_spec.short_spec, spec.short_spec))


class ExtensionConflictError(DirectoryLayoutError):
    """Raised when an extension is added to a package that already has it."""

    def __init__(self, spec, ext_spec, conflict):
        super(ExtensionConflictError, self).__init__(
            "%s cannot be installed in %s because it conflicts with %s"
            % (ext_spec.short_spec, spec.short_spec, conflict.short_spec))


class NoSuchExtensionError(DirectoryLayoutError):
    """Raised when an extension isn't there on deactivate."""

    def __init__(self, spec, ext_spec):
        super(NoSuchExtensionError, self).__init__(
            "%s cannot be removed from %s because it's not activated."
            % (ext_spec.short_spec, spec.short_spec))
