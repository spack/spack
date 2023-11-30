# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Hipblas(CMakePackage, CudaPackage, ROCmPackage):
    """hipBLAS is a BLAS marshalling library, with multiple
    supported backends"""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipBLAS"
    git = "https://github.com/ROCmSoftwarePlatform/hipBLAS.git"
    url = "https://github.com/ROCmSoftwarePlatform/hipBLAS/archive/rocm-5.5.0.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath", "haampie")
    libraries = ["libhipblas"]

    version("develop", branch="develop")
    version("master", branch="master")
    version("5.6.1", sha256="f9da82fbefc68b84081ea0ed0139b91d2a540357fcf505c7f1d57eab01eb327c")
    version("5.6.0", sha256="9453a31324e10ba528f8f4755d2c270d0ed9baa33e980d8f8383204d8e28a563")
    version("5.5.1", sha256="5920c9a9c83cf7e2b42d1f99f5d5091cac7f6c0a040a737e869e57b92d7045a9")
    version("5.5.0", sha256="b080c25cb61531228d26badcdca856c46c640035c058bfc1c9f63de65f418cd5")
    version("5.4.3", sha256="5acac147aafc15c249c2f24c19459135ed68b506403aa92e602b67cfc10c38b7")
    version("5.4.0", sha256="341d61adff8d08cbf70aa07bd11a088bcd0687fc6156870a1aee9eff74f3eb4f")
    version("5.3.3", sha256="1ce093fc6bc021ad4fe0b0b93f9501038a7a5a16b0fd4fc485d65cbd220a195e")
    version("5.3.0", sha256="873d55749479873994679840906c4257316dfb09a6200411204ad4a8c2480565")
    version("5.2.3", sha256="4d66db9b000b6207b5270d90556b724bfdb08ebbfcc675f014287e0be7ee6344")
    version("5.2.1", sha256="ccae36b118b7a1eb4b2f7d65fb163f54ab9c5cf774dbe2ec60971d4f78ae8308")
    version("5.2.0", sha256="5e9091dc4ef83896f5c3bc5ade1cb5db8e1a6afc451dbba4da19d8a7ec2b6f29")
    version("5.1.3", sha256="f0fdaa851971b41b48ec2e7d640746fbd6f9f433da2020c5fd95c91a7473d9e1")
    version("5.1.0", sha256="22faba3828e50a4c4e22f569a7d6441c797a11db1d472619c01d3515a3275e92")
    version(
        "5.0.2",
        sha256="201772bfc422ecb2c50e898dccd7d3d376cf34a2b795360e34bf71326aa37646",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="63cffe748ed4a86fc80f408cb9e8a9c6c55c22a2b65c0eb9a76360b97bbb9d41",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="82dd82a41bbadbb2a91a2a44a5d8e0d2e4f36d3078286ed4db3549b1fb6d6978",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="187777ed49cc7c496c897e8ba80532d458c9afbc51a960e45f96923ad896c18e",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="7b1f774774de5fa3d2b777e3a262328559d56165c32aa91b002505694362e7b2",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="0631e21c588794ea1c8413ef8ff293606bcf7a52c0c3ff88da824f103395a76a",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="c7ce7f69c7596b5a54e666fb1373ef41d1f896dd29260a691e2eadfa863e2b1a",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="876efe80a4109ad53d290d2921b3fb425b4cb857b32920819f10dcd4deee4ef8",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="6cc03af891b36cce8266d32ba8dfcf7fdfcc18afa7a6cc058fbe28bcf8528d94",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="45cb5e3b37f0845bd9e0d09912df4fa0ce88dd508ec9448241ae6600d3c4b1e8",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="82ddd57fd905a5d4060665349ec017ff757a7c121cb9310574be3c3630b3545f",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="33cb82e8b2658ae2096f39e41492ba8b6852ac37c26a730612b8642d9d29abe3",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="9840a493ab4838c86696ceb33ce07c34b5f59f62db4f88cb3af62b69d84f8729",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="d451da80beb048767da71a090afceed2e111d01b3e95a7044deada5054d6e7b1",
        deprecated=True,
    )

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

    depends_on("cmake@3.5:", type="build")

    depends_on("googletest@1.10.0:", type="test")
    depends_on("netlib-lapack@3.7.1:", type="test")
    depends_on("boost@1.64.0:1.76.0 +program_options cxxstd=14", type="test")

    patch("link-clients-blas.patch", when="@4.3.0:4.3.2")
    patch("link-clients-blas-4.5.0.patch", when="@4.5.0:4.5.2")
    patch("hipblas-link-clients-blas-5.0.0.patch", when="@5.0.0:5.0.2")
    patch("remove-hipblas-clients-file-installation.patch", when="@5.5:")

    depends_on("rocm-cmake@5.2.0:", type="build", when="@5.2.0:")
    depends_on("rocm-cmake@4.5.0:", type="build", when="@4.5.0:")
    depends_on("rocm-cmake@3.5.0:", type="build")

    depends_on("hip +cuda", when="+cuda")

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
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "master",
        "develop",
    ]:
        depends_on("rocsolver@" + ver, when="+rocm @" + ver)
        depends_on("rocblas@" + ver, when="+rocm @" + ver)

    for tgt in ROCmPackage.amdgpu_targets:
        depends_on(
            "rocblas amdgpu_target={0}".format(tgt), when="+rocm amdgpu_target={0}".format(tgt)
        )
        depends_on(
            "rocsolver amdgpu_target={0}".format(tgt), when="+rocm amdgpu_target={0}".format(tgt)
        )

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
        args = [
            self.define("BUILD_CLIENTS_SAMPLES", "OFF"),
            self.define("BUILD_CLIENTS_TESTS", self.run_tests),
        ]

        if self.spec.satisfies("@:3.9.0"):
            args.append(self.define_from_variant("TRY_CUDA", "cuda"))
        else:
            args.append(self.define_from_variant("USE_CUDA", "cuda"))

        # FindHIP.cmake was used for +rocm until 4.1.0 and is still used for +cuda
        if self.spec.satisfies("@:4.0") or self.spec.satisfies("+cuda"):
            if self.spec["hip"].satisfies("@:5.1"):
                args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.cmake))
            else:
                args.append(
                    self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip)
                )

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))
        if self.spec.satisfies("@5.3.0:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")

        return args

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        exe = Executable(join_path(self.build_directory, "clients", "staging", "hipblas-test"))
        exe("--gtest_filter=-*known_bug*")
