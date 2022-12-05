# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
from typing import List  # novm

import llnl.util.filesystem as fs

import spack.builder
import spack.package_base
from spack.directives import build_system, conflicts

from ._checks import BaseBuilder


class NMakePackage(spack.package_base.PackageBase):
    """Specialized class for packages built using a Makefiles."""

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "NmakePackage"

    build_system("nmake")
    conflicts("platform=linux", when="build_system=nmake")
    conflicts("platform=darwin", when="build_system=nmake")
    conflicts("platform=cray", when="build_system=nmake")


@spack.builder.builder("nmake")
class NMakeBuilder(BaseBuilder):
    """The NMake builder encodes the most common way of building software with
    NMake on Windows. It has three phases that can be overridden, if need be:

            1. :py:meth:`~.NMakeBuilder.edit`
            2. :py:meth:`~.NMakeBuilder.build`
            3. :py:meth:`~.NMakeBuilder.install`

    It is usually necessary to override the :py:meth:`~.NMakeBuilder.edit`
    phase (which is by default a no-op), while the other two have sensible defaults.

    For a finer tuning you may override:

            +--------------------------------------------+--------------------+
            | **Method**                                 | **Purpose**        |
            +============================================+====================+
            | :py:attr:`~.NMakeBuilder.build_targets`    | Specify ``nmake``  |
            |                                            | targets for the    |
            |                                            | build phase        |
            +--------------------------------------------+--------------------+
            | :py:attr:`~.NMakeBuilder.install_targets`  | Specify ``nmake``  |
            |                                            | targets for the    |
            |                                            | install phase      |
            +--------------------------------------------+--------------------+
            | :py:meth:`~.NMakeBuilder.build_directory`  | Directory where the|
            |                                            | Makefile is located|
            +--------------------------------------------+--------------------+
    """

    phases = ("edit", "build", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods = ("check", "installcheck")

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = (
        "build_targets",
        "install_targets",
        "build_time_test_callbacks",
        "install_time_test_callbacks",
        "build_directory",
    )

    #: Targets for ``make`` during the :py:meth:`~.NMakeBuilder.build` phase
    build_targets: List[str] = []
    #: Targets for ``make`` during the :py:meth:`~.NMakeBuilder.install` phase
    install_targets = ["install"]

    #: Callback names for build-time test
    build_time_test_callbacks = ["check"]

    #: Callback names for install-time test
    install_time_test_callbacks = ["installcheck"]

    @property
    def build_directory(self):
        """Return the directory containing the main Makefile."""
        return self.pkg.stage.source_path

    def edit(self, pkg, spec, prefix):
        """Edit the Makefile before calling make. The default is a no-op."""
        pass

    def build(self, pkg, spec, prefix):
        """Run "make" on the build targets specified by the builder."""
        with fs.working_dir(self.build_directory):
            inspect.getmodule(self.pkg).nmake(*self.build_targets)

    def install(self, pkg, spec, prefix):
        """Run "make" on the install targets specified by the builder."""
        with fs.working_dir(self.build_directory):
            inspect.getmodule(self.pkg).nmake(*self.install_targets)
