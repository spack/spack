# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Common utilities for managing intel oneapi packages."""
import getpass
import os
import platform
import shutil
from os.path import basename, dirname, isdir

from llnl.util.filesystem import find_headers, find_libraries, join_path
from llnl.util.link_tree import LinkTree

from spack.directives import conflicts, variant
from spack.package import mkdirp
from spack.util.environment import EnvironmentModifications
from spack.util.executable import Executable

from .generic import Package


class IntelOneApiPackage(Package):
    """Base class for Intel oneAPI packages."""

    homepage = "https://software.intel.com/oneapi"

    # oneAPI license does not allow mirroring outside of the
    # organization (e.g. University/Company).
    redistribute_source = False

    for c in [
        "target=ppc64:",
        "target=ppc64le:",
        "target=aarch64:",
        "platform=darwin:",
        "platform=cray:",
        "platform=windows:",
    ]:
        conflicts(c, msg="This package in only available for x86_64 and Linux")

    # Add variant to toggle environment modifications from vars.sh
    variant("envmods", default=True, description="Toggles environment modifications")

    @staticmethod
    def update_description(cls):
        """Updates oneapi package descriptions with common text."""

        text = """ LICENSE INFORMATION: By downloading and using this software, you agree to the terms
        and conditions of the software license agreements at https://intel.ly/393CijO."""
        cls.__doc__ = cls.__doc__ + text
        return cls

    @property
    def component_dir(self):
        """Subdirectory for this component in the install prefix."""
        raise NotImplementedError

    @property
    def component_prefix(self):
        """Path to component <prefix>/<component>/<version>."""
        return self.prefix.join(join_path(self.component_dir, self.spec.version))

    def install(self, spec, prefix):
        self.install_component(basename(self.url_for_version(spec.version)))

    def install_component(self, installer_path):
        """Shared install method for all oneapi packages."""

        if platform.system() == "Linux":
            # Intel installer assumes and enforces that all components
            # are installed into a single prefix. Spack wants to
            # install each component in a separate prefix. The
            # installer mechanism is implemented by saving install
            # information in a directory called installercache for
            # future runs. The location of the installercache depends
            # on the userid. For root it is always in /var/intel. For
            # non-root it is in $HOME/intel.
            #
            # The method for preventing this install from interfering
            # with other install depends on the userid. For root, we
            # delete the installercache before and after install. For
            # non root we redefine the HOME environment variable.
            if getpass.getuser() == "root":
                shutil.rmtree("/var/intel/installercache", ignore_errors=True)

            bash = Executable("bash")

            # Installer writes files in ~/intel set HOME so it goes to prefix
            bash.add_default_env("HOME", self.prefix)
            # Installer checks $XDG_RUNTIME_DIR/.bootstrapper_lock_file as well
            bash.add_default_env("XDG_RUNTIME_DIR", join_path(self.stage.path, "runtime"))

            bash(
                installer_path,
                "-s",
                "-a",
                "-s",
                "--action",
                "install",
                "--eula",
                "accept",
                "--install-dir",
                self.prefix,
            )

            if getpass.getuser() == "root":
                shutil.rmtree("/var/intel/installercache", ignore_errors=True)

        # Some installers have a bug and do not return an error code when failing
        if not isdir(join_path(self.prefix, self.component_dir)):
            raise RuntimeError("install failed")

    def setup_run_environment(self, env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source {prefix}/{component}/{version}/env/vars.sh
        """
        # Only if environment modifications are desired (default is +envmods)
        if "~envmods" not in self.spec:
            env.extend(
                EnvironmentModifications.from_sourcing_file(
                    join_path(self.component_prefix, "env", "vars.sh")
                )
            )

    def symlink_dir(self, src, dest):
        # Taken from: https://github.com/spack/spack/pull/31285/files
        # oneapi bin/lib directories are 2 or 3 levels below the
        # prefix, but it is more typical to have them directly in the
        # prefix. The location has changed over time. Rather than make
        # every package that needs to know where include/lib are
        # located be aware of this, put in symlinks to conform. This
        # is good enough for some, but not all packages.

        # If we symlink top-level directories directly, files won't
        # show up in views Create real dirs and symlink files instead

        # Create a real directory at dest
        mkdirp(dest)

        # Symlink all files in src to dest keeping directories as dirs
        for entry in os.listdir(src):
            src_path = join_path(src, entry)
            dest_path = join_path(dest, entry)
            if isdir(src_path) and os.access(src_path, os.X_OK):
                link_tree = LinkTree(src_path)
                link_tree.merge(dest_path)
            else:
                os.symlink(src_path, dest_path)


class IntelOneApiLibraryPackage(IntelOneApiPackage):
    """Base class for Intel oneAPI library packages.

    Contains some convenient default implementations for libraries.
    Implement the method directly in the package if something
    different is needed.

    """

    @property
    def headers(self):
        include_path = join_path(self.component_prefix, "include")
        return find_headers("*", include_path, recursive=True)

    @property
    def libs(self):
        lib_path = join_path(self.component_prefix, "lib", "intel64")
        lib_path = lib_path if isdir(lib_path) else dirname(lib_path)
        return find_libraries("*", root=lib_path, shared=True, recursive=True)


class IntelOneApiStaticLibraryList:
    """Provides ld_flags when static linking is needed

    Oneapi puts static and dynamic libraries in the same directory, so
    -l will default to finding the dynamic library. Use absolute
    paths, as recommended by oneapi documentation.

    Allow both static and dynamic libraries to be supplied by the
    package.
    """

    def __init__(self, static_libs, dynamic_libs):
        self.static_libs = static_libs
        self.dynamic_libs = dynamic_libs

    @property
    def directories(self):
        return self.dynamic_libs.directories

    @property
    def search_flags(self):
        return self.dynamic_libs.search_flags

    @property
    def link_flags(self):
        return "-Wl,--start-group {0} -Wl,--end-group {1}".format(
            " ".join(self.static_libs.libraries), self.dynamic_libs.link_flags
        )

    @property
    def ld_flags(self):
        return "{0} {1}".format(self.search_flags, self.link_flags)
