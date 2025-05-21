# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Transferbench(CMakePackage):
    """TransferBench is a utility capable of benchmarking simultaneous copies between
    user-specified devices (CPUs/GPUs)"""

    homepage = "https://github.com/ROCm/TransferBench"
    url = "https://github.com/ROCm/TransferBench/archive/refs/tags/rocm-6.4.0.tar.gz"

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    license("MIT")

    version("6.4.0", sha256="3d2d5723278774a26f4889643bd9025a883982b111321106e4343c998b229298")
    version("6.3.3", sha256="b473d47ff44501d111dd13fa2e9f723967df0035219168b490a1c013a123cbf6")
    version("6.3.2", sha256="ae2210b669416f558ec9da85b67f45f31a7705de4d553e54b0eabe2fb8e8f665")
    version("6.3.1", sha256="611fb858d4a2cb48fb8942b1a85c54ab3212fb74952327757f673551e0c507c0")
    version("6.3.0", sha256="1b67f7ac96a44ab20a02e45a94046a0991b46b84efbd9f9639b864189214ded1")

    depends_on("cxx", type="build")
    depends_on("numactl")

    for ver in ["6.3.0", "6.3.1", "6.3.2", "6.3.3", "6.4.0"]:
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"rocm-cmake@{ver}", when=f"@{ver}")

    patch("001-link-hsa-numa.patch")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)
