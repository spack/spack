# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmCore(CMakePackage):
    """rocm-core is a utility which can be used to get ROCm release version.
       It also provides the Lmod modules files for the ROCm release.
       getROCmVersion function provides the ROCm version."""

    homepage = "https://github.com/RadeonOpenCompute/rocm-core"
    url = "https://github.com/RadeonOpenCompute/rocm-core/archive/refs/tags/rocm-5.5.0.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["librocm-core"]
    version("5.5.0", sha256="684d3312bb14f05dc280cf136f5eddff38ba340cd85c383d6a217d8e27d3d57d")

    def cmake_args(self):
        args = [self.define("ROCM_VERSION", self.spec.version)]
        return args
