# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Rccl(CMakePackage):
    """RCCL (pronounced "Rickle") is a stand-alone library
    of standard collective communication routines for GPUs,
    implementing all-reduce, all-gather, reduce, broadcast,
    and reduce-scatter."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rccl"
    git = "https://github.com/ROCmSoftwarePlatform/rccl.git"
    url = "https://github.com/ROCmSoftwarePlatform/rccl/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["librccl"]

    version("5.4.3", sha256="a2524f602bd7b3b6afeb8ba9aff660216ee807fa836e46442d068b5ed5f51a4d")
    version("5.4.0", sha256="213f4f3d75389be588673e43f563e5c0d6908798228b0b6a71f27138fd4ed0c7")
    version("5.3.3", sha256="8995a2d010ad0748fc85ac06e8da7e8d110ba996db04d42b77526c9c059c05bb")
    version("5.3.0", sha256="51da5099fa58c2be882319cebe9ceabe2062feebcc0c5849e8c109030882c10a")
    version("5.2.3", sha256="ecba09f4c95b4b2dae81b88231a972ac956d29909b5e712e21cf2a74bd251ff4")
    version("5.2.1", sha256="cfd17dc003f19900e44928d81111570d3720d4905321f2a18c909909c4bee822")
    version("5.2.0", sha256="6ee3a04da0d16eb53f768a088633a7d8ecc4416a2d0c07f7ba8426ab7892b060")
    version("5.1.3", sha256="56491257f27b48bf85f4b91434a2a6e49a448337c889db181b02c8a4a260a4bc")
    version("5.1.0", sha256="02b0180857e615326f9cab775573436b9162899ad8e526830f54392b8a51b1f5")
    version(
        "5.0.2",
        sha256="a2377ad2332b93d3443a8ee74f4dd9f965ae8cbbfad473f8f57ca17905389a39",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="80eb70243f11b80e215458a67c278cd5a655f6e486289962b92ba3504e50af5c",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="36de0d3f3ffad491758d89c208ef72c5be5e0db766053a9c766e9c5c6a33a487",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="f806f9f65c490abddc562cb4812e12701582bbb449e41cc4797d00e0dedf084e",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="c5db71423dc654e8d2c3111e142e65c89436bc636827d95d41a09a87f44fe246",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="b5231d8c5ab034a583feceebcef68d0cc0b05ec5a683f802fc7747c89f27d5f6",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="2829fae40ebc1d8be201856d2193a941c87e9cf38dca0a2f4414e675c1742f20",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="88ec9b43c31cb054fe6aa28bcc0f4b510213635268f951939d6980eee5bb3680",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="0632a15b3d6b5981c05377cf4aeb51546f4c4901fd7c37fb0c98071851ad531a",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="d9dd0b0d8b9d056fc5e6c7b814520800190952acd30dac3a7c462c4cb6f42bb3",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="ff9d03154d668093309ff814a33788f2cc093b3c627e78e42ae246e6017408b0",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="0b6676d06bdb1f65d511a95db9f842a3443def83d75759dfdf812b5e62d8c910",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="8273878ff71aac2e7adf5cc8562d2933034c6c6b3652f88fbe3cd4f2691036e3",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="290b57a66758dce47d0bfff3f5f8317df24764e858af67f60ddcdcadb9337253",
        deprecated=True,
    )

    amdgpu_targets = ROCmPackage.amdgpu_targets

    variant("amdgpu_target", values=auto_or_any_combination_of(*amdgpu_targets), sticky=True)
    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    patch("0001-Fix-numactl-path-issue.patch", when="@3.7.0:4.3.2")
    patch("0002-Fix-numactl-rocm-smi-path-issue.patch", when="@4.5.0:5.2.1")
    patch("0003-Fix-numactl-rocm-smi-path-issue.patch", when="@5.2.3:")

    depends_on("cmake@3.5:", type="build")
    for ver in [
        "3.5.0",
        "3.7.0",
        "3.8.0",
        "3.9.0",
        "3.10.0",
        "4.0.0",
        "4.1.0",
        "4.2.0",
        "4.3.0",
        "4.3.1",
        "4.5.0",
        "4.5.2",
        "5.0.0",
        "5.0.2",
        "5.1.0",
        "5.1.3",
        "5.2.0",
        "5.2.1",
        "5.2.3",
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
    ]:
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("comgr@" + ver, when="@" + ver)
        depends_on("hsa-rocr-dev@" + ver, when="@" + ver)

    for ver in [
        "3.7.0",
        "3.8.0",
        "3.9.0",
        "3.10.0",
        "4.0.0",
        "4.1.0",
        "4.2.0",
        "4.3.0",
        "4.3.1",
        "4.5.0",
        "4.5.2",
        "5.0.0",
        "5.0.2",
        "5.1.0",
        "5.1.3",
        "5.2.0",
        "5.2.1",
        "5.2.3",
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
    ]:
        depends_on("numactl@2:", when="@" + ver)
    for ver in [
        "4.5.0",
        "4.5.2",
        "5.0.0",
        "5.0.2",
        "5.1.0",
        "5.1.3",
        "5.2.0",
        "5.2.1",
        "5.2.3",
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
    ]:
        depends_on("rocm-smi-lib@" + ver, when="@" + ver)

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            ver = "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        else:
            ver = None
        return ver

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        args = []
        if "@3.7.0:" in self.spec:
            args.append(self.define("NUMACTL_DIR", self.spec["numactl"].prefix))

        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@4.5.0:"):
            args.append(self.define("ROCM_SMI_DIR", self.spec["rocm-smi-lib"].prefix))
        return args
