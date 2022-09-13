# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nvcomp(CMakePackage, CudaPackage):
    """A library for fast lossless compression/decompression on NVIDIA GPUs"""

    homepage = "https://github.com/NVIDIA/nvcomp"
    url = "https://github.com/NVIDIA/nvcomp/archive/refs/tags/v2.0.2.tar.gz"
    git = homepage

    maintainers = ["robertu94"]

    version("robertu94", git="https://github.com/robertu94/nvcomp", branch="main", preferred=True)
    version("2.0.2", sha256="e75c746084e5100a4eecb8c31d546f70fe698e6f927d4fdb8326058712204f16")

    depends_on("cuda")
    conflicts("~cuda")

    def cmake_args(self):
        args = ["-DBUILD_EXAMPLES=OFF", "-DBUILD_BENCHMARKS=OFF"]
        cuda_arch_list = self.spec.variants["cuda_arch"].value
        args.append("CMAKE_CUDA_ARCHITECTURES={0}".format(";".join(cuda_arch_list)))
        return args
