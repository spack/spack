# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Hipsolver(CMakePackage, CudaPackage, ROCmPackage):
    """hipSOLVER is a LAPACK marshalling library, with multiple supported backends.
    It sits between the application and a 'worker' LAPACK library, marshalling
    inputs into the backend library and marshalling results back to the application.
    hipSOLVER exports an interface that does not require the client to change,
    regardless of the chosen backend. Currently, hipSOLVER supports rocSOLVER
    and cuSOLVER as backends."""

    homepage = "https://github.com/ROCm/hipSOLVER"
    git = "https://github.com/ROCm/hipSOLVER.git"
    url = "https://github.com/ROCm/hipSOLVER/archive/rocm-6.1.1.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath")
    libraries = ["libhipsolver"]

    license("MIT")

    version("develop", branch="develop")
    version("master", branch="master")
    version("6.1.1", sha256="01d4553458f417824807c069cacfc65d23f6cac79536158473b4356986c8fafd")
    version("6.1.0", sha256="3cb89ca486cdbdfcb1a07c35ee65f60219ef7bc62a5b0f94ca1a3206a0106495")
    version("6.0.2", sha256="8215e55c3a5bc9c7eeb141cefdc6a6eeba94d8bc3aeae9e685ab7904965040d4")
    version("6.0.0", sha256="385849db02189d5e62096457e52ae899ae5c1ae7d409dc1da61f904d8861b48c")
    version("5.7.1", sha256="5592e965c0dc5722931302289643d1ece370220af2c7afc58af97b3395295658")
    version("5.7.0", sha256="0e35795bfbcb57ed8e8437471209fb7d230babcc31d9a4a0b3640c3ee639f4a7")
    version("5.6.1", sha256="2e546bc7771f7bf0aa7892b69cded725941573e8b70614759c3d03c21eb78dde")
    version("5.6.0", sha256="11fa51d210853d93d24d55b20367738e49711793412f58e8d7689710b92ae16c")
    version("5.5.1", sha256="826bd64a4887176595bb7319d9a3612e7327602efe1f42aa3f2ad0e783d1a180")
    version("5.5.0", sha256="0f45be0f90907381ae3e82424599e2ca2112d6411b4a64c72558d63f00409b83")
    version("5.4.3", sha256="02a1bffecc494393f49f97174db7d2c101db557d32404923a44520876e682e3a")
    version("5.4.0", sha256="d53d81c55b458ba5e6ea0ec6bd24bcc79ab06789730391da82d8c33b936339d9")
    version("5.3.3", sha256="f5a487a1c7225ab748996ac4d837ac7ab26b43618c4ed97a124f8fac1d67786e")
    version("5.3.0", sha256="6e920a59ddeefd52c9a6d164c33bc097726529e1ede3c417c711697956655b15")
    with default_args(deprecated=True):
        version("5.2.3", sha256="a57d883fdd09c6c7f9856fcfcabee6fa7ff9beed33d2f1a465bf28d38ea6f364")
        version("5.2.1", sha256="e000b08cf7bfb5f8f6d65d163ebeeb3274172b9f474228b810bde5e6f87f2b37")
        version("5.2.0", sha256="96927410e0a2cc0f50172604ef6437e15d2cf4b62d22b2035f13aae21f43dc82")
        version("5.1.3", sha256="96faa799a2db8078b72f9c3b5c199179875a7c20dc1064371b22a6a63397c145")
        version("5.1.0", sha256="697ba2b2814e7ac6f79680e6455b4b5e0def1bee2014b6940f47be7d13c0ae74")

    # default to an 'auto' variant until amdgpu_targets can be given a better default than 'none'
    amdgpu_targets = ROCmPackage.amdgpu_targets
    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
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
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    depends_on("cmake@3.5:", type="build")
    depends_on("suite-sparse", type="build")

    depends_on("rocm-cmake@5.2.0:", type="build", when="@5.2.0:")
    depends_on("rocm-cmake@4.5.0:", type="build")

    depends_on("hip +cuda", when="+cuda")

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
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "master",
        "develop",
    ]:
        depends_on(f"rocblas@{ver}", when=f"+rocm @{ver}")
        depends_on(f"rocsolver@{ver}", when=f"+rocm @{ver}")

    for tgt in ROCmPackage.amdgpu_targets:
        depends_on(f"rocblas amdgpu_target={tgt}", when=f"+rocm amdgpu_target={tgt}")
        depends_on(f"rocsolver amdgpu_target={tgt}", when=f"+rocm amdgpu_target={tgt}")

    depends_on("googletest@1.10.0:", type="test")
    depends_on("netlib-lapack@3.7.1:", type="test")
    patch("001-suite-sparse-include-path.patch", when="@6.1.0")
    patch("0001-suite-sparse-include-path-6.1.1.patch", when="@6.1.1:")

    def patch(self):
        if self.spec.satisfies("@6.1.1 +rocm"):
            with working_dir("library/src/amd_detail"):
                filter_file(
                    "^#include <suitesparse/cholmod.h>",
                    "#include <cholmod.h>",
                    "hipsolver_sparse.cpp",
                )

    def check(self):
        exe = join_path(self.build_directory, "clients", "staging", "hipsolver-test")
        self.run_test(exe, options=["--gtest_filter=-*known_bug*"])

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
        if self.spec.satisfies("+asan"):
            self.asan_on(env)

    def cmake_args(self):
        args = [
            self.define("BUILD_CLIENTS_SAMPLES", "OFF"),
            self.define("BUILD_CLIENTS_TESTS", self.run_tests),
            self.define("SUITE_SPARSE_PATH", self.spec["suite-sparse"].prefix),
            self.define("ROCBLAS_PATH", self.spec["rocblas"].prefix),
        ]

        args.append(self.define_from_variant("USE_CUDA", "cuda"))

        # FindHIP.cmake is still used for +cuda
        if self.spec.satisfies("+cuda"):
            if self.spec["hip"].satisfies("@:5.1"):
                args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.cmake))
            else:
                args.append(
                    self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip)
                )

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))
        if self.spec.satisfies("@5.3.0:"):
            args.append(self.define("CMAKE_INSTALL_LIBDIR", "lib"))

        return args
