# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Datatransferkit(CMakePackage):
    """DataTransferKit is an open-source software library of
    parallel solution transfer services for multiphysics simulations"""

    homepage = "https://datatransferkit.readthedoc.io"
    url = "https://github.com/ORNL-CEES/DataTransferKit/archive/3.1-rc3.tar.gz"
    git = "https://github.com/ORNL-CEES/DataTransferKit.git"

    tags = ["e4s"]

    maintainers("Rombur")

    version("master", branch="master", submodules=True)
    version("3.1-rc3", commit="691d5a1540f7cd42141a3b3d2a7c8370cbc3560a", submodules=True)
    version("3.1-rc2", commit="1abc1a43b33dffc7a16d7497b4185d09d865e36a", submodules=True)

    variant(
        "external-arborx",
        default=False,
        description="use an external ArborX library instead of the submodule",
    )
    variant("openmp", default=False, description="enable OpenMP backend")
    variant("serial", default=True, description="enable Serial backend (default)")
    variant("shared", default=True, description="enable the build of shared lib")

    depends_on("arborx@1.0:", when="+external-arborx")
    depends_on("boost")
    depends_on("cmake", type="build")
    depends_on("trilinos+intrepid2+shards~dtk")
    depends_on("trilinos+openmp", when="+openmp")
    depends_on("trilinos+stratimikos+belos", when="@master")
    depends_on("trilinos@13:", when="@3.1-rc2:")

    def cmake_args(self):
        spec = self.spec
        from_variant = self.define_from_variant

        options = [
            from_variant("BUILD_SHARED_LIBS", "shared"),
            "-DDataTransferKit_ENABLE_DataTransferKit=ON",
            from_variant("DataTransferKit_ENABLE_ArborX_TPL", "external-arborx"),
            "-DDataTransferKit_ENABLE_TESTS=OFF",
            "-DDataTransferKit_ENABLE_EXAMPLES=OFF",
            "-DCMAKE_CXX_EXTENSIONS=OFF",
            "-DCMAKE_CXX_STANDARD=14",
        ]

        if "+openmp" in spec:
            options.append("-DDataTransferKit_ENABLE_OpenMP=ON")

        return options
