# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FastFloat(CMakePackage):
    """Fast and exact implementation of the C++ from_chars functions for number
    types."""

    homepage = "https://github.com/fastfloat/fast_float"
    url = "https://github.com/fastfloat/fast_float/archive/refs/tags/v6.1.4.tar.gz"

    license("Apache-2.0 OR BSL-1.0 OR MIT", checked_by="pranav-sivararamn")

    version("6.1.6", sha256="4458aae4b0eb55717968edda42987cabf5f7fc737aee8fede87a70035dba9ab0")
    version("6.1.5", sha256="597126ff5edc3ee59d502c210ded229401a30dafecb96a513135e9719fcad55f")
    version("6.1.4", sha256="12cb6d250824160ca16bcb9d51f0ca7693d0d10cb444f34f1093bc02acfce704")

    depends_on("cxx", type="build")
    depends_on("cmake@3.9:", type="build")

    depends_on("doctest", type=("link", "test"))

    def cmake_args(self):
        args = [self.define("FASTFLOAT_TEST", self.run_tests), self.define("SYSTEM_DOCTEST", True)]

        return args
