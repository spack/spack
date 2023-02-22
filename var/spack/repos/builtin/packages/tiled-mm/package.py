# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TiledMm(CMakePackage, CudaPackage, ROCmPackage):
    """Matrix multiplication on GPUs for matrices stored on a CPU. Similar to cublasXt,
    but ported to both NVIDIA and AMD GPUs."""

    maintainers = ["mtaillefumier", "simonpintarelli"]
    homepage = "https://github.com/eth-cscs/Tiled-MM/"
    url = "https://github.com/eth-cscs/Tiled-MM/archive/refs/tags/v2.0.tar.gz"
    git = "https://github.com/eth-cscs/Tiled-MM.git"

    version("master", branch="master")
    version("2.2", sha256="6d0b49c9588ece744166822fd44a7bc5bec3dc666b836de8bf4bf1a7bb675aac")
    version("2.0", sha256="ea554aea8c53d7c8e40044e6d478c0e8137d7e8b09d7cb9650703430d92cf32e")

    variant("shared", default=True)
    variant("examples", default=False)
    variant("tests", default=False)

    depends_on("rocblas", when="+rocm")
    depends_on("cxxopts", when="+tests")
    depends_on("cxxopts", when="+examples")

    conflicts("~cuda~rocm")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("TIELDMM_WITH_EXAMPLES", "examples"),
            self.define_from_variant("TIELDMM_WITH_TESTS", "tests"),
        ]

        if "+rocm" in self.spec:
            args.extend([self.define("TILEDMM_GPU_BACKEND", "ROCM")])

        if "+cuda" in self.spec:
            args.extend([self.define("TILEDMM_GPU_BACKEND", "CUDA")])

        return args
