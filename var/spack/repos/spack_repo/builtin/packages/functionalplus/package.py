# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Functionalplus(CMakePackage):
    """Functional Programming Library for C++. Write concise and readable C++ code."""

    homepage = "https://github.com/Dobiasd/FunctionalPlus"
    url = "https://github.com/Dobiasd/FunctionalPlus/archive/refs/tags/v0.2.25.tar.gz"

    license("BSL-1.0")

    version("0.2.25", sha256="9b5e24bbc92f43b977dc83efbc173bcf07dbe07f8718fc2670093655b56fcee3")
    version("0.2.24", sha256="446c63ac3f2045e7587f694501882a3d7c7b962b70bcc08deacf5777bdaaff8c")
    version("0.2.23", sha256="5c2d28d2ba7d0cdeab9e31bbf2e7f8a9d6f2ff6111a54bfc11d1b05422096f19")
    version("0.2.22", sha256="79378668dff6ffa8abc1abde2c2fe37dc6fe1ac040c55d5ee7886924fa6a1376")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
