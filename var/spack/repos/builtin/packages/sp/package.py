# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sp(CMakePackage):
    """The spectral transform library splib contains FORTRAN subprograms
    to be used for a variety of spectral transform functions. This is
    part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-sp"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-sp/archive/refs/tags/v2.3.3.tar.gz"

    maintainers("t-brown", "AlexanderRichert-NOAA", "edwardhartnett", "Hang-Lei-NOAA")

    version("2.4.0", sha256="dbb4280e622d2683b68a28f8e3837744adf9bbbb1e7940856e8f4597f481c708")
    version("2.3.3", sha256="c0d465209e599de3c0193e65671e290e9f422f659f1da928505489a3edeab99f")

    variant("shared", default=False, description="Build shared library", when="@2.4:")
    variant("pic", default=False, description="Enable position-independent code (PIC)")

    def setup_run_environment(self, env):
        suffixes = ["4", "d"]
        if self.spec.satisfies("@:2.3"):
            suffixes += ["8"]
        for suffix in suffixes:
            lib = find_libraries(
                "libsp_" + suffix,
                root=self.prefix,
                shared=self.spec.satisfies("+shared"),
                recursive=True,
            )
            env.set("SP_LIB" + suffix, lib[0])
            env.set("SP_INC" + suffix, "include_" + suffix)

    def cmake_args(self):
        args = []
        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        args.append(self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"))
        return args
