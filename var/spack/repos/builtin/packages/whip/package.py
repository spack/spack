# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Whip(CMakePackage, CudaPackage, ROCmPackage):
    """whip is a small C++ abstraction layer for CUDA and HIP."""

    homepage = "https://github.com/eth-cscs/whip/"
    url = "https://github.com/eth-cscs/whip/archive/0.0.0.tar.gz"
    git = "https://github.com/eth-cscs/whip.git"
    maintainers = ["msimberg", "rasolca"]

    version("main", branch="main")

    depends_on("cmake@3.22:", type="build")

    # Exactly one of +cuda and +rocm need to be set
    conflicts("~cuda ~rocm")
    conflicts("+cuda +rocm")

    def cmake_args(self):
        if self.spec.satisfies("+cuda"):
            return [self.define("WHIP_BACKEND", "CUDA")]
        else:
            return [self.define("WHIP_BACKEND", "HIP")]
