# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import inspect
import os
import re

from spack.directives import extends
from spack.hooks.sbang import filter_shebang
from spack.package_base import PackageBase, run_after
from spack.util.executable import Executable
from spack.version import ver


class PerlPackage(PackageBase):
    """Specialized class for packages that are built using Perl.

    This class provides four phases that can be overridden if required:

        1. :py:meth:`~.PerlPackage.configure`
        2. :py:meth:`~.PerlPackage.build`
        3. :py:meth:`~.PerlPackage.check`
        4. :py:meth:`~.PerlPackage.install`

    The default methods use, in order of preference:
        (1) Makefile.PL,
        (2) Build.PL.

    Some packages may need to override
    :py:meth:`~.PerlPackage.configure_args`,
    which produces a list of arguments for
    :py:meth:`~.PerlPackage.configure`.
    Arguments should not include the installation base directory.
    """

    #: Phases of a Perl package
    phases = ["configure", "build", "install"]

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "PerlPackage"

    #: Callback names for build-time test
    build_time_test_callbacks = ["check"]

    extends("perl")

    def configure_args(self):
        """Produces a list containing the arguments that must be passed to
        :py:meth:`~.PerlPackage.configure`. Arguments should not include
        the installation base directory, which is prepended automatically.

        :return: list of arguments for Makefile.PL or Build.PL
        """
        return []

    def configure(self, spec, prefix):
        """Runs Makefile.PL or Build.PL with arguments consisting of
        an appropriate installation base directory followed by the
        list returned by :py:meth:`~.PerlPackage.configure_args`.

        :raise RuntimeError: if neither Makefile.PL or Build.PL exist
        """
        if os.path.isfile("Makefile.PL"):
            self.build_method = "Makefile.PL"
            self.build_executable = inspect.getmodule(self).make
        elif os.path.isfile("Build.PL"):
            self.build_method = "Build.PL"
            self.build_executable = Executable(os.path.join(self.stage.source_path, "Build"))
        else:
            raise RuntimeError("Unknown build_method for perl package")

        if self.build_method == "Makefile.PL":
            options = ["Makefile.PL", "INSTALL_BASE={0}".format(prefix)]
        elif self.build_method == "Build.PL":
            options = ["Build.PL", "--install_base", prefix]
        options += self.configure_args()

        inspect.getmodule(self).perl(*options)

    def fetch_remote_versions(self, concurrency=128):
        """Handle unfortunate versions."""
        remote_versions = super(PerlPackage, self).fetch_remote_versions(concurrency)
        if not remote_versions:
            return remote_versions
        result = {}
        for version, url in remote_versions.items():
            ver_match = re.match(r"^(\d+)\.(\d{3})(\d{3})((?:-TRIAL|_\d+)?)$", version.string)
            if not ver_match:
                ver_match = re.match(
                    r"^(\d+)\.(\d{2})(\d{2,3})((?:-TRIAL|_\d+)?)$", version.string
                )
            if ver_match:
                set_ver = ver(".".join(ver_match.group(1, 2, 3)) + ver_match.group(4))
            else:
                set_ver = version
            result[set_ver] = url
        return result

    # It is possible that the shebang in the Build script that is created from
    # Build.PL may be too long causing the build to fail. Patching the shebang
    # does not happen until after install so do it here manually.
    @run_after("configure")
    def fix_shebang(self):
        if self.build_method == "Build.PL":
            filter_shebang("Build")

    def build(self, spec, prefix):
        """Builds a Perl package."""
        self.build_executable()

    # Ensure that tests run after build (if requested):
    run_after("build")(PackageBase._run_default_build_time_test_callbacks)

    def check(self):
        """Runs built-in tests of a Perl package."""
        self.build_executable("test")

    def install(self, spec, prefix):
        """Installs a Perl package."""
        self.build_executable("install")

    # Check that self.prefix is there after installation
    run_after("install")(PackageBase.sanity_check_prefix)
