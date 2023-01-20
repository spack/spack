# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
import os

from llnl.util.filesystem import filter_file

import spack.builder
import spack.package_base
from spack.directives import build_system, extends
from spack.package_base import PackageBase
from spack.util.executable import Executable

from ._checks import BaseBuilder, execute_build_time_tests


class PerlPackage(PackageBase):
    """Specialized class for packages that are built using Perl."""

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "PerlPackage"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "perl"

    build_system("perl")

    extends("perl", when="build_system=perl")


@spack.builder.builder("perl")
class PerlBuilder(BaseBuilder):
    """The perl builder provides four phases that can be overridden, if required:

        1. :py:meth:`~.PerlBuilder.configure`
        2. :py:meth:`~.PerlBuilder.build`
        3. :py:meth:`~.PerlBuilder.check`
        4. :py:meth:`~.PerlBuilder.install`

    The default methods use, in order of preference:
        (1) Makefile.PL,
        (2) Build.PL.

    Some packages may need to override :py:meth:`~.PerlBuilder.configure_args`,
    which produces a list of arguments for :py:meth:`~.PerlBuilder.configure`.

    Arguments should not include the installation base directory.
    """

    #: Phases of a Perl package
    phases = ("configure", "build", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods = ("configure_args", "check")

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = ()

    #: Callback names for build-time test
    build_time_test_callbacks = ["check"]

    def configure_args(self):
        """List of arguments passed to :py:meth:`~.PerlBuilder.configure`.

        Arguments should not include the installation base directory, which
        is prepended automatically.
        """
        return []

    def configure(self, pkg, spec, prefix):
        """Run Makefile.PL or Build.PL with arguments consisting of
        an appropriate installation base directory followed by the
        list returned by :py:meth:`~.PerlBuilder.configure_args`.

        Raises:
            RuntimeError: if neither Makefile.PL nor Build.PL exist
        """
        if os.path.isfile("Makefile.PL"):
            self.build_method = "Makefile.PL"
            self.build_executable = inspect.getmodule(self.pkg).make
        elif os.path.isfile("Build.PL"):
            self.build_method = "Build.PL"
            self.build_executable = Executable(os.path.join(self.pkg.stage.source_path, "Build"))
        else:
            raise RuntimeError("Unknown build_method for perl package")

        if self.build_method == "Makefile.PL":
            options = ["Makefile.PL", "INSTALL_BASE={0}".format(prefix)]
        elif self.build_method == "Build.PL":
            options = ["Build.PL", "--install_base", prefix]
        options += self.configure_args()

        inspect.getmodule(self.pkg).perl(*options)

    # It is possible that the shebang in the Build script that is created from
    # Build.PL may be too long causing the build to fail. Patching the shebang
    # does not happen until after install so set '/usr/bin/env perl' here in
    # the Build script.
    @spack.builder.run_after("configure")
    def fix_shebang(self):
        if self.build_method == "Build.PL":
            pattern = "#!{0}".format(self.spec["perl"].command.path)
            repl = "#!/usr/bin/env perl"
            filter_file(pattern, repl, "Build", backup=False)

    def build(self, pkg, spec, prefix):
        """Builds a Perl package."""
        self.build_executable()

    # Ensure that tests run after build (if requested):
    spack.builder.run_after("build")(execute_build_time_tests)

    def check(self):
        """Runs built-in tests of a Perl package."""
        self.build_executable("test")

    def install(self, pkg, spec, prefix):
        """Installs a Perl package."""
        self.build_executable("install")
