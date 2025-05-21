# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class RocprofilerSdk(CMakePackage):
    """ROCProfiler-SDK is AMD’s new and improved tooling infrastructure, providing a
    hardware-specific low-level performance analysis interface for profiling and
    tracing GPU compute applications."""

    homepage = "https://github.com/ROCm/rocprofiler-sdk"
    git = "https://github.com/ROCm/rocprofiler-sdk.git"
    url = "https://github.com/ROCm/rocprofiler-sdk/archive/refs/tags/rocm-6.3.2.tar.gz"

    tags = ["rocm"]

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    license("MIT")

    version(
        "6.3.3",
        tag="rocm-6.3.3",
        commit="95a3964ee26ac45618517f24669858bdb39ea7d2",
        submodules=True,
    )
    version(
        "6.3.2",
        tag="rocm-6.3.2",
        commit="f5d3fd3d3460c74cb8935f0021e31f0bff5cb305",
        submodules=True,
    )
    version(
        "6.3.1",
        tag="rocm-6.3.1",
        commit="38ac1c8f7d62cbb702f53c7085be16bf1943369a",
        submodules=True,
    )
    version(
        "6.3.0",
        tag="rocm-6.3.0",
        commit="38ac1c8f7d62cbb702f53c7085be16bf1943369a",
        submodules=True,
    )
    version(
        "6.2.4",
        tag="rocm-6.2.4",
        commit="03fe8df3622a97161699439dfe933ef8e9e7db8a",
        submodules=True,
    )
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    for ver in ["6.2.4", "6.3.0", "6.3.1", "6.3.2", "6.3.3"]:
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"rocm-cmake@{ver}", when=f"@{ver}")
        depends_on(f"aqlprofile@{ver}", when=f"@{ver}")
        depends_on(f"rccl@{ver}", when=f"@{ver}")
        depends_on(f"rocprofiler-register@{ver}", when=f"@{ver}")
