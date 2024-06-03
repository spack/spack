# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmCore(CMakePackage):
    """rocm-core is a utility which can be used to get ROCm release version.
    It also provides the Lmod modules files for the ROCm release.
    getROCmVersion function provides the ROCm version."""

    homepage = "https://github.com/ROCm/rocm-core"
    url = "https://github.com/ROCm/rocm-core/archive/refs/tags/rocm-6.0.0.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["librocm-core"]

    license("MIT")
    version("6.1.1", sha256="a27bebdd1ba9d387f33b82a67f64c55cb565b482fe5017d5b5726d68da1ab839")
    version("6.1.0", sha256="9dfe542d1647c42993b06f594c316dad63ba6d6fb2a7398bd72c5768fd1d7b5b")
    version("6.0.2", sha256="04f01dca2862f0bf781de8afb74aabefc3c9b1d9f01bc8cadb2eb3d7395119cc")
    version("6.0.0", sha256="d950ee4b63336f34579b6e1dda2d05966b7afa9c84bcdc13874991d1147dc788")
    version("5.7.1", sha256="fc4915019ddfd126e8ef6a15006bce3aa7bd5fd11dc8eb04ce2ee6bdf9c6ae7f")
    version("5.7.0", sha256="722689bfec46c35f5428a41c5aacfc31efec2294fc3b0112861c562f8a71ac93")
    version("5.6.1", sha256="eeef75e16e05380ccbc8df17a02dc141a66dddaadb444a97f7278f78067c498c")
    version("5.6.0", sha256="3c3d47c8b774968d768d42810a3fed42d058b7d6da248d5295df2a7ffb262568")
    version("5.5.1", sha256="bc73060432ffdc2e210394835d383890b9652476074ef4708d447473f273ce76")
    version("5.5.0", sha256="684d3312bb14f05dc280cf136f5eddff38ba340cd85c383d6a217d8e27d3d57d")

    def cmake_args(self):
        args = [self.define("ROCM_VERSION", self.spec.version)]
        return args
