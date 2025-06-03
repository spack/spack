# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Rocshmem(CMakePackage):
    """rocSHMEM intra-kernel networking runtime for AMD dGPUs on the ROCm platform."""

    homepage = "https://github.com/ROCm/rocSHMEM"
    url = "https://github.com/ROCm/rocSHMEM/archive/refs/tags/rocm-6.4.0.tar.gz"

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    license("MIT")

    version("6.4.0", sha256="fbc8b6a7159901fdeda0d6cc8b97f20740c6cce59ba4a28c2050658cc1eecb81")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    for ver in ["6.4.0"]:
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"rocm-cmake@{ver}", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
        depends_on(f"rocprim@{ver}", when=f"@{ver}")
        depends_on(f"rocthrust@{ver}", when=f"@{ver}")

    depends_on("ucx@1.17: +rocm")
    depends_on("openmpi@5.0.6: fabrics=ucx")

    def cmake_args(self):
        args = [self.define("USE_GPU_IB", False)]
        return args
