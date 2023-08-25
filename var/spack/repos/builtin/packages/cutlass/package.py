# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cutlass(CMakePackage, CudaPackage):
    """CUDA Templates for Linear Algebra Subroutines"""

    homepage = "https://github.com/NVIDIA/cutlass"
    git = homepage + ".git"
    url = "https://github.com/NVIDIA/cutlass/archive/refs/tags/v2.9.0.tar.gz"

    version("master", branch="master")
    version("2.9.1", sha256="2d6474576c08ee21d7f4f3a10fd1a47234fd9fd638efc8a2e0e64bb367f09bc1")
    version("2.9.0", sha256="ccca4685739a3185e3e518682845314b07a5d4e16d898b10a3c3a490fd742fb4")
    variant("cuda", default=True, description="Build with CUDA")
    conflicts("~cuda", msg="Cutlass requires CUDA")
    conflicts(
        "cuda_arch=none",
        msg="Must specify CUDA compute capabilities of your GPU, see "
        "https://developer.nvidia.com/cuda-gpus",
    )

    def setup_build_environment(self, env):
        env.set("CUDACXX", self.spec["cuda"].prefix.bin.nvcc)

    def cmake_args(self):
        cuda_arch = self.spec.variants["cuda_arch"].value
        return [self.define("CUTLASS_NVCC_ARCHS", ";".join(cuda_arch))]
