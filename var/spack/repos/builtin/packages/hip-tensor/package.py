# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class HipTensor(CMakePackage, ROCmPackage):
    """AMD’s C++ library for accelerating tensor primitives"""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipTensor"
    git = "https://github.com/ROCmSoftwarePlatform/hipTensor.git"
    url = "https://github.com/ROCmSoftwarePlatform/hipTensor/archive/refs/tags/rocm-5.7.1.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "afzpatel")

    version("develop", branch="develop")
    version("master", branch="master")
    version("5.7.1", sha256="96743d4e695fe865aef4097ae31d9b4e42a2d5a92135a005b0d187d9c0b17645")
    version("5.7.0", sha256="4b17f6d43b17fe2dc1d0c61e9663d4752006f7898cc94231206444a1663eb252")

    for ver in ["5.7.0", "5.7.1", "master", "develop"]:
        depends_on("composable-kernel@" + ver, when="@" + ver)

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        args = []
        return args
