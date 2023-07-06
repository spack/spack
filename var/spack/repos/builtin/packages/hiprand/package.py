# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Hiprand(CMakePackage, CudaPackage, ROCmPackage):
    """The hipRAND project provides an interface for generating pseudo-random
    and quasi-random numbers with either cuRAND or rocRAND backends."""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipRAND"
    git = "https://github.com/ROCmSoftwarePlatform/hipRAND.git"
    url = "https://github.com/ROCmSoftwarePlatform/hipRAND/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath")
    libraries = ["libhiprand"]

    version("develop", branch="develop")
    version("master", branch="master")
    version("5.4.3", sha256="7d3d04476880ec90c088dff81f69aac8699eaef972476000e5c4726584ffa98f")
    version("5.4.0", sha256="9456d4b4d5fd5c0b728f4aa4f8c224f829fe6fbf08e397848475293f71029a22")
    version("5.3.3", sha256="f72626b00d61ed2925b3124b7f094ccfaf7750f02bee6bac6b79317e1c5576ef")
    version("5.3.0", sha256="6fd9b3a719bf4c228657cb2a0ff283eb7d777ba31bfffe5a26589d588f89a279")
    version("5.2.3", sha256="56d62a94c8ce6e2fc55fff57f3d0931b6332654333d1ad5dee854aefb1548f66")
    version("5.2.1", sha256="27b00e15ca1f6608a5625a246b55f3128ce32fdca605eb727f66c6322b77bf42")
    version("5.2.0", sha256="3d179aa928446471651ef2f308779b5946b3ba9bbc1643689b0abc56e6ec2f5e")
    version("5.1.3", sha256="6965e30a6ec0bef4ee251d144785a4dda55dff32aed27e12dc1b4dc0c4bbc094")
    version("5.1.0", sha256="a3dd384439047bdad60864f0aff7fcf855a6a601458b05770d054b53c1a7cae2")

    # default to an 'auto' variant until amdgpu_targets can be given a better default than 'none'
    amdgpu_targets = ROCmPackage.amdgpu_targets
    variant(
        "amdgpu_target",
        values=spack.variant.DisjointSetsOfValues(("auto",), ("none",), amdgpu_targets)
        .with_default("auto")
        .with_error(
            "the values 'auto' and 'none' are mutually exclusive with any of the other values"
        )
        .with_non_feature_values("auto", "none"),
        sticky=True,
    )
    variant("rocm", default=True, description="Enable ROCm support")
    conflicts("+cuda +rocm", msg="CUDA and ROCm support are mutually exclusive")
    conflicts("~cuda ~rocm", msg="CUDA or ROCm support is required")
    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    depends_on("cmake@3.10.2:", type="build")

    depends_on("rocm-cmake@5.2.0:", type="build", when="@5.2.0:")
    depends_on("rocm-cmake@5.1.0:", type="build")

    depends_on("hip +cuda", when="+cuda")

    depends_on("googletest@1.10.0:", type="test")

    for ver in [
        "5.1.0",
        "5.1.3",
        "5.2.0",
        "5.2.1",
        "5.2.3",
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
        "master",
        "develop",
    ]:
        depends_on("rocrand@" + ver, when="+rocm @" + ver)

    depends_on("rocrand ~hiprand", when="+rocm")
    for tgt in ROCmPackage.amdgpu_targets:
        depends_on(
            "rocrand amdgpu_target={0}".format(tgt), when="+rocm amdgpu_target={0}".format(tgt)
        )

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

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

    def cmake_args(self):
        args = [self.define("BUILD_BENCHMARK", "OFF"), self.define("BUILD_TEST", self.run_tests)]

        if self.spec.satisfies("+cuda"):
            args.append(self.define("BUILD_WITH_LIB", "CUDA"))
            # FindHIP.cmake is used for +cuda
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip))
        else:
            args.append(self.define("BUILD_WITH_LIB", "ROCM"))

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        if self.spec.satisfies("@5.3.0:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")

        return args
