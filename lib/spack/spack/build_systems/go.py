# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
import os
from typing import Optional, Tuple

import llnl.util.filesystem as fs

import spack.package_base
import spack.util.url
from spack.directives import build_system, depends_on

from ._checks import BaseBuilder


class GoPackage(spack.package_base.PackageBase):
    """Specialized class for packages built using Go."""

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "GoPackage"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "go"

    depends_on("go", type="build")

    build_system("go")


@spack.builder.builder("go")
class GoBuilder(BaseBuilder):
    """The Go builder provides two phases that can be overridden if required:

    #. :py:meth:`~.GoBuilder.build`
    #. :py:meth:`~.GoBuilder.install`
    """

    #: Phases of a Go package
    phases: Tuple[str, ...] = ("build", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods = ()

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = ()

    #: Path of the main.go file
    root_main_go_dir: Optional[str] = None

    @property
    def build_directory(self):
        """Return the directory where 'main.go' resides."""
        return self.pkg.stage.source_path

    @property
    def root_main_go_dir(self):
        """The relative path to the directory containing main.go.
        Defaults to the root of the extracted tarball.
        """
        return self.pkg.stage.source_path

    @property
    def std_go_args(self):
        """Standard Go arguments provided as a property for
        convenience of package writers
        """
        std_go_args = GoBuilder.std_args(self.pkg)
        std_go_args += getattr(self.pkg, "go_flag_args", [])
        return std_go_args

    @staticmethod
    def std_args(pkg):
        """Computes the standard Go arguments for a generic package"""
        buildmode = "default"

        args = ["build", "-buildmode", buildmode]

        return args

    def go_args(self):
        """List of all the arguments that must be passed to go build."""
        return []

    def setup_build_environment(self, env):
        # Point GOPATH at the top of the staging dir for the build step.
        env.prepend_path("GOPATH", self.stage.path)

    def build(self, pkg, spec, prefix):
        """Runs ``go build`` in the source directory"""
        options = ["-C", os.path.abspath(self.root_main_go_dir)]
        options += self.std_go_args
        options += self.go_args()
        with fs.working_dir(self.build_directory, create=True):
            inspect.getmodule(self.pkg).go(*options)
