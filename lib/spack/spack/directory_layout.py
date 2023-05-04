# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import glob
import os
import posixpath
import re
import shutil
import sys
from contextlib import contextmanager

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.config
import spack.hash_types as ht
import spack.spec
import spack.util.spack_json as sjson
from spack.error import SpackError

# Note: Posixpath is used here as opposed to
# os.path.join due to spack.spec.Spec.format
# requiring forward slash path seperators at this stage
default_projections = {
    "all": posixpath.join(
        "{architecture}", "{compiler.name}-{compiler.version}", "{name}-{version}-{hash}"
    )
}


def _check_concrete(spec):
    """If the spec is not concrete, raise a ValueError"""
    if not spec.concrete:
        raise ValueError("Specs passed to a DirectoryLayout must be concrete!")


class DirectoryLayout(object):
    """A directory layout is used to associate unique paths with specs.
    Different installations are going to want different layouts for their
    install, and they can use this to customize the nesting structure of
    spack installs. The default layout is:

    * <install root>/

      * <platform-os-target>/

        * <compiler>-<compiler version>/

          * <name>-<version>-<hash>

    The hash here is a SHA-1 hash for the full DAG plus the build
    spec.

    The installation directory projections can be modified with the
    projections argument.
    """

    def __init__(self, root, **kwargs):
        self.root = root
        self.check_upstream = True
        projections = kwargs.get("projections") or default_projections
        self.projections = dict(
            (key, projection.lower()) for key, projection in projections.items()
        )

        # apply hash length as appropriate
        self.hash_length = kwargs.get("hash_length", None)
        if self.hash_length is not None:
            for when_spec, projection in self.projections.items():
                if "{hash}" not in projection:
                    if "{hash" in projection:
                        raise InvalidDirectoryLayoutParametersError(
                            "Conflicting options for installation layout hash" " length"
                        )
                    else:
                        raise InvalidDirectoryLayoutParametersError(
                            "Cannot specify hash length when the hash is not"
                            " part of all install_tree projections"
                        )
                self.projections[when_spec] = projection.replace(
                    "{hash}", "{hash:%d}" % self.hash_length
                )

        # If any of these paths change, downstream databases may not be able to
        # locate files in older upstream databases
        self.metadata_dir = ".spack"
        self.deprecated_dir = "deprecated"
        self.spec_file_name = "spec.json"
        # Use for checking yaml and deprecated types
        self._spec_file_name_yaml = "spec.yaml"
        self.extension_file_name = "extensions.yaml"
        self.packages_dir = "repos"  # archive of package.py files
        self.manifest_file_name = "install_manifest.json"

    @property
    def hidden_file_regexes(self):
        return ("^{0}$".format(re.escape(self.metadata_dir)),)

    def relative_path_for_spec(self, spec):
        _check_concrete(spec)

        projection = spack.projections.get_projection(self.projections, spec)
        path = spec.format(projection)
        return path

    def write_spec(self, spec, path):
        """Write a spec out to a file."""
        _check_concrete(spec)
        with open(path, "w") as f:
            # The hash of the projection is the DAG hash which contains
            # the full provenance, so it's availabe if we want it later
            spec.to_json(f, hash=ht.dag_hash)

    def write_host_environment(self, spec):
        """The host environment is a json file with os, kernel, and spack
        versioning. We use it in the case that an analysis later needs to
        easily access this information.
        """
        from spack.util.environment import get_host_environment_metadata

        env_file = self.env_metadata_path(spec)
        environ = get_host_environment_metadata()
        with open(env_file, "w") as fd:
            sjson.dump(environ, fd)

    def read_spec(self, path):
        """Read the contents of a file and parse them as a spec"""
        try:
            with open(path) as f:
                extension = os.path.splitext(path)[-1].lower()
                if extension == ".json":
                    spec = spack.spec.Spec.from_json(f)
                elif extension == ".yaml":
                    # Too late for conversion; spec_file_path() already called.
                    spec = spack.spec.Spec.from_yaml(f)
                else:
                    raise SpecReadError(
                        "Did not recognize spec file extension:" " {0}".format(extension)
                    )
        except Exception as e:
            if spack.config.get("config:debug"):
                raise
            raise SpecReadError("Unable to read file: %s" % path, "Cause: " + str(e))

        # Specs read from actual installations are always concrete
        spec._mark_concrete()
        return spec

    def spec_file_path(self, spec):
        """Gets full path to spec file"""
        _check_concrete(spec)
        # Attempts to convert to JSON if possible.
        # Otherwise just returns the YAML.
        yaml_path = os.path.join(self.metadata_path(spec), self._spec_file_name_yaml)
        json_path = os.path.join(self.metadata_path(spec), self.spec_file_name)
        if os.path.exists(yaml_path) and fs.can_write_to_dir(yaml_path):
            self.write_spec(spec, json_path)
            try:
                os.remove(yaml_path)
            except OSError as err:
                tty.debug("Could not remove deprecated {0}".format(yaml_path))
                tty.debug(err)
        elif os.path.exists(yaml_path):
            return yaml_path
        return json_path

    def deprecated_file_path(self, deprecated_spec, deprecator_spec=None):
        """Gets full path to spec file for deprecated spec

        If the deprecator_spec is provided, use that. Otherwise, assume
        deprecated_spec is already deprecated and its prefix links to the
        prefix of its deprecator."""
        _check_concrete(deprecated_spec)
        if deprecator_spec:
            _check_concrete(deprecator_spec)

        # If deprecator spec is None, assume deprecated_spec already deprecated
        # and use its link to find the file.
        base_dir = (
            self.path_for_spec(deprecator_spec)
            if deprecator_spec
            else os.readlink(deprecated_spec.prefix)
        )

        yaml_path = os.path.join(
            base_dir,
            self.metadata_dir,
            self.deprecated_dir,
            deprecated_spec.dag_hash() + "_" + self._spec_file_name_yaml,
        )

        json_path = os.path.join(
            base_dir,
            self.metadata_dir,
            self.deprecated_dir,
            deprecated_spec.dag_hash() + "_" + self.spec_file_name,
        )

        if os.path.exists(yaml_path) and fs.can_write_to_dir(yaml_path):
            self.write_spec(deprecated_spec, json_path)
            try:
                os.remove(yaml_path)
            except (IOError, OSError) as err:
                tty.debug("Could not remove deprecated {0}".format(yaml_path))
                tty.debug(err)
        elif os.path.exists(yaml_path):
            return yaml_path

        return json_path

    @contextmanager
    def disable_upstream_check(self):
        self.check_upstream = False
        yield
        self.check_upstream = True

    def metadata_path(self, spec):
        return os.path.join(spec.prefix, self.metadata_dir)

    def env_metadata_path(self, spec):
        return os.path.join(self.metadata_path(spec), "install_environment.json")

    def build_packages_path(self, spec):
        return os.path.join(self.metadata_path(spec), self.packages_dir)

    def create_install_directory(self, spec):
        _check_concrete(spec)

        # Create install directory with properly configured permissions
        # Cannot import at top of file
        from spack.package_prefs import get_package_dir_permissions, get_package_group

        # Each package folder can have its own specific permissions, while
        # intermediate folders (arch/compiler) are set with access permissions
        # equivalent to the root permissions of the layout.
        group = get_package_group(spec)
        perms = get_package_dir_permissions(spec)

        fs.mkdirp(spec.prefix, mode=perms, group=group, default_perms="parents")
        fs.mkdirp(self.metadata_path(spec), mode=perms, group=group)  # in prefix

        self.write_spec(spec, self.spec_file_path(spec))

    def ensure_installed(self, spec):
        """
        Throws InconsistentInstallDirectoryError if:
        1. spec prefix does not exist
        2. spec prefix does not contain a spec file, or
        3. We read a spec with the wrong DAG hash out of an existing install directory.
        """
        _check_concrete(spec)
        path = self.path_for_spec(spec)
        spec_file_path = self.spec_file_path(spec)

        if not os.path.isdir(path):
            raise InconsistentInstallDirectoryError(
                "Install prefix {0} does not exist.".format(path)
            )

        if not os.path.isfile(spec_file_path):
            raise InconsistentInstallDirectoryError(
                "Install prefix exists but contains no spec.json:", "  " + path
            )

        installed_spec = self.read_spec(spec_file_path)
        if installed_spec.dag_hash() != spec.dag_hash():
            raise InconsistentInstallDirectoryError(
                "Spec file in %s does not match hash!" % spec_file_path
            )

    def all_specs(self):
        if not os.path.isdir(self.root):
            return []

        specs = []
        for _, path_scheme in self.projections.items():
            path_elems = ["*"] * len(path_scheme.split(posixpath.sep))
            # NOTE: Does not validate filename extension; should happen later
            path_elems += [self.metadata_dir, "spec.json"]
            pattern = os.path.join(self.root, *path_elems)
            spec_files = glob.glob(pattern)
            if not spec_files:  # we're probably looking at legacy yaml...
                path_elems += [self.metadata_dir, "spec.yaml"]
                pattern = os.path.join(self.root, *path_elems)
                spec_files = glob.glob(pattern)
            specs.extend([self.read_spec(s) for s in spec_files])
        return specs

    def all_deprecated_specs(self):
        if not os.path.isdir(self.root):
            return []

        deprecated_specs = set()
        for _, path_scheme in self.projections.items():
            path_elems = ["*"] * len(path_scheme.split(posixpath.sep))
            # NOTE: Does not validate filename extension; should happen later
            path_elems += [
                self.metadata_dir,
                self.deprecated_dir,
                "*_spec.*",
            ]  # + self.spec_file_name]
            pattern = os.path.join(self.root, *path_elems)
            spec_files = glob.glob(pattern)
            get_depr_spec_file = lambda x: os.path.join(
                os.path.dirname(os.path.dirname(x)), self.spec_file_name
            )
            deprecated_specs |= set(
                (self.read_spec(s), self.read_spec(get_depr_spec_file(s))) for s in spec_files
            )
        return deprecated_specs

    def specs_by_hash(self):
        by_hash = {}
        for spec in self.all_specs():
            by_hash[spec.dag_hash()] = spec
        return by_hash

    def path_for_spec(self, spec):
        """Return absolute path from the root to a directory for the spec."""
        _check_concrete(spec)

        if spec.external:
            return spec.external_path
        if self.check_upstream:
            upstream, record = spack.store.db.query_by_spec_hash(spec.dag_hash())
            if upstream:
                raise SpackError(
                    "Internal error: attempted to call path_for_spec on"
                    " upstream-installed package."
                )

        path = self.relative_path_for_spec(spec)
        assert not path.startswith(self.root)
        return os.path.join(self.root, path)

    def remove_install_directory(self, spec, deprecated=False):
        """Removes a prefix and any empty parent directories from the root.
        Raised RemoveFailedError if something goes wrong.
        """
        path = self.path_for_spec(spec)
        assert path.startswith(self.root)

        # Windows readonly files cannot be removed by Python
        # directly, change permissions before attempting to remove
        if sys.platform == "win32":
            kwargs = {
                "ignore_errors": False,
                "onerror": fs.readonly_file_handler(ignore_errors=False),
            }
        else:
            kwargs = {}  # the default value for ignore_errors is false

        if deprecated:
            if os.path.exists(path):
                try:
                    metapath = self.deprecated_file_path(spec)
                    os.unlink(path)
                    os.remove(metapath)
                except OSError as e:
                    raise RemoveFailedError(spec, path, e) from e
        elif os.path.exists(path):
            try:
                shutil.rmtree(path, **kwargs)
            except OSError as e:
                raise RemoveFailedError(spec, path, e) from e

        path = os.path.dirname(path)
        while path != self.root:
            if os.path.isdir(path):
                try:
                    os.rmdir(path)
                except OSError as e:
                    if e.errno == errno.ENOENT:
                        # already deleted, continue with parent
                        pass
                    elif e.errno == errno.ENOTEMPTY:
                        # directory wasn't empty, done
                        return
                    else:
                        raise e
            path = os.path.dirname(path)


class DirectoryLayoutError(SpackError):
    """Superclass for directory layout errors."""

    def __init__(self, message, long_msg=None):
        super(DirectoryLayoutError, self).__init__(message, long_msg)


class RemoveFailedError(DirectoryLayoutError):
    """Raised when a DirectoryLayout cannot remove an install prefix."""

    def __init__(self, installed_spec, prefix, error):
        super(RemoveFailedError, self).__init__(
            "Could not remove prefix %s for %s : %s" % (prefix, installed_spec.short_spec, error)
        )
        self.cause = error


class InconsistentInstallDirectoryError(DirectoryLayoutError):
    """Raised when a package seems to be installed to the wrong place."""

    def __init__(self, message, long_msg=None):
        super(InconsistentInstallDirectoryError, self).__init__(message, long_msg)


class SpecReadError(DirectoryLayoutError):
    """Raised when directory layout can't read a spec."""


class InvalidDirectoryLayoutParametersError(DirectoryLayoutError):
    """Raised when a invalid directory layout parameters are supplied"""

    def __init__(self, message, long_msg=None):
        super(InvalidDirectoryLayoutParametersError, self).__init__(message, long_msg)


class InvalidExtensionSpecError(DirectoryLayoutError):
    """Raised when an extension file has a bad spec in it."""


class ExtensionAlreadyInstalledError(DirectoryLayoutError):
    """Raised when an extension is added to a package that already has it."""

    def __init__(self, spec, ext_spec):
        super(ExtensionAlreadyInstalledError, self).__init__(
            "%s is already installed in %s" % (ext_spec.short_spec, spec.short_spec)
        )


class ExtensionConflictError(DirectoryLayoutError):
    """Raised when an extension is added to a package that already has it."""

    def __init__(self, spec, ext_spec, conflict):
        super(ExtensionConflictError, self).__init__(
            "%s cannot be installed in %s because it conflicts with %s"
            % (ext_spec.short_spec, spec.short_spec, conflict.short_spec)
        )
