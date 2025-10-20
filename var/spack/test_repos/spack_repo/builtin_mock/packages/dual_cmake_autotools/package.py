# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin_mock.build_systems.cmake import CMakePackage

from spack.package import *


class DualCmakeAutotools(AutotoolsPackage, CMakePackage):
    """Package with two build systems."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dual-cmake-autotools-1.0.tar.gz"

    version("1.0")
    build_system("autotools", "cmake", default="autotools")
    variant(
        "generator",
        default="make",
        values=("make", "ninja"),
        description="the build system generator to use",
        when="build_system=cmake",
    )

    with when("build_system=cmake"):
        depends_on("cmake@3.5.1:", type="build")
        depends_on("cmake@3.14.0:", type="build", when="@2.1.0:")
