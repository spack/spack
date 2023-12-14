# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libgrpp(CMakePackage):
    """A library for the evaluation of molecular integrals of the"""

    """generalized relativistic pseudopotential operator (GRPP) over Gaussian functions."""

    homepage = "https://github.com/aoleynichenko/libgrpp"
    git = "https://github.com/aoleynichenko/libgrpp.git"

    maintainers("mtaillefumier")

    version("master", branch="main")

    patch("cmake-fixes.patch")

    variant("pic", default=True, description="Compile the library with position independent code")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic")]
        return args
