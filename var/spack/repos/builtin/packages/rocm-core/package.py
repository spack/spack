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

    version("5.6.1", sha256="eeef75e16e05380ccbc8df17a02dc141a66dddaadb444a97f7278f78067c498c")
    version("5.6.0", sha256="3c3d47c8b774968d768d42810a3fed42d058b7d6da248d5295df2a7ffb262568")
    version("5.5.1", sha256="bc73060432ffdc2e210394835d383890b9652476074ef4708d447473f273ce76")
    version("5.5.0", sha256="684d3312bb14f05dc280cf136f5eddff38ba340cd85c383d6a217d8e27d3d57d")

    def cmake_args(self):
        args = [self.define("ROCM_VERSION", self.spec.version)]
        return args
