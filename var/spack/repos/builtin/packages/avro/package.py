# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install avro
#
# You can edit this file again by typing:
#
#     spack edit avro
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import inspect
import os
from spack.package import *
from llnl.util import filesystem as fs




class Avro(CMakePackage):
    """Apache Avro data serialization system."""

    homepage = "https://www.apache.org/dyn/closer.cgi/avro/"
    url = "https://dlcdn.apache.org/avro/avro-1.11.3/avro-src-1.11.3.tar.gz"

    maintainers("teaguesterling")

    license("APACHE-2.0", checked_by="teaguesterling")

    version("1.11.3", sha256="6ea787a83260a11b5a899aadd22f701e24138477cd7bf789614051a449dcc034")

    variant("cxx", default=True, description="Built the C++ library")

    with when("+cxx"):
        depends_on("cxx", type="build")
        with default_args(type=("build", "link")):
            depends_on("boost@1.38:+iostreams+filesystem+system+program_options")
            depends_on("cmake@2.6:")
            depends_on("python@3")
            depends_on("doxygen")

    def cmake_variant_subdirs(self):
        return [
            ("lang/c++/build", "..", "+cxx"),
        ]

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_subdir(self, pkg, spec, prefix, builddir, listdir, variant):
        """Runs ``cmake`` in the build sub directory if variant is true"""
        if spec.satisfies(variant):
            options = self.std_cmake_args
            options += self.cmake_args()
            with fs.working_dir(builddir, create=True):
                options.append(os.path.abspath(listdir))
                inspect.getmodule(self.pkg).cmake(*options)

    def build_subdir(self, pkg, spec, prefix, builddir, variant):
        """Make the build sub targets"""
        if spec.satisfies(variant):
            with fs.working_dir(builddir):
                if self.generator == "Unix Makefiles":
                    inspect.getmodule(self.pkg).make(*self.build_targets)
                elif self.generator == "Ninja":
                    self.build_targets.append("-v")
                    inspect.getmodule(self.pkg).ninja(*self.build_targets)

    def install_subdir(self, pkg, spec, prefix, builddir, variant):
        """Make the install sub targets"""
        if spec.satisfies(variant):
            with fs.working_dir(builddir):
                if self.generator == "Unix Makefiles":
                    inspect.getmodule(self.pkg).make(*self.install_targets)
                elif self.generator == "Ninja":
                    inspect.getmodule(self.pkg).ninja(*self.install_targets)

    def cmake(self, pkg, spec, prefix):
        for builddir, listdir, variant in pkg.cmake_variant_subdirs():
            self.cmake_subdir(pkg, spec, prefix, builddir, listdir, variant)

    def build(self, pkg, spec, prefix):
        for builddir, listdir, variant in pkg.cmake_variant_subdirs():
            self.build_subdir(pkg, spec, prefix, builddir, variant)

    def install(self, pkg, spec, prefix):
        for builddir, listdir, variant in pkg.cmake_variant_subdirs():
            self.install_subdir(pkg, spec, prefix, builddir, variant)

