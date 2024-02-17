# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Hipsparse(CMakePackage, CudaPackage, ROCmPackage):
    """hipSPARSE is a SPARSE marshalling library, with
    multiple supported backends"""

    homepage = "https://github.com/ROCm/hipSPARSE"
    git = "https://github.com/ROCm/hipSPARSE.git"
    url = "https://github.com/ROCm/hipSPARSE/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath", "haampie")
    libraries = ["libhipsparse"]

    license("MIT")
    version("6.0.2", sha256="40c1d2493f87c686d9afd84a00321ad10ca0d0d80d6dcfeee8e51858dd1bd8c1")
    version("6.0.0", sha256="718a5f03b6a579c0542a60d00f5688bec53a181b429b7ee8ce3c8b6c4a78d754")
    version("5.7.1", sha256="16c3818260611226c3576d8d55ad8f51e0890d2473503edf2c9313250ae65ca7")
    version("5.7.0", sha256="729b749b5340034639873a99e6091963374f6f0456c8f36d076c96f03fe43888")
    version("5.6.1", sha256="d636d0c5d1e38cc0c09b1e95380199ec82bd465b94bd6661f0c8d9374d9b565d")
    version("5.6.0", sha256="3a6931b744ebaa4469a4c50d059a008403e4dc2a4f04dd69c3c6d20916b4a491")
    version("5.5.1", sha256="3d291e4fe2c611d555e54de66149b204fe7ac59f5dd00a9ad93bc6dca0528880")
    version("5.5.0", sha256="8122c8f17d899385de83efb7ac0d8a4fabfcd2aa21bbed63e63ea7adf0d22df6")
    version("5.4.3", sha256="b373eccd03679a13fab4e740fc780da25cbd598abca3a1e5e3613ae14954f9db")
    version("5.4.0", sha256="47420d38483c8124813b744971e428a0352c83d9b62a5a50f74ffa8f9b785b20")
    version("5.3.3", sha256="d96d0e47594ab12e8c380da2300704c105736a0771940d7d2fae666f2869e457")
    version("5.3.0", sha256="691b32b916952ed9af008aa29f60cc190322b73cfc098bb2eda3ff68c89c7b35")
    with default_args(deprecated=True):
        version("5.2.3", sha256="f70d3deff13188adc4105ef3ead53510e4b54075b9ffcfe3d3355d90d4b6eadd")
        version("5.2.1", sha256="7b8e4ff264285ae5aabb3c5c2b38bf28f90b2af44efb0398fcf13ffc24bc000a")
        version("5.2.0", sha256="4fdab6ec953c6d2d000687c5979077deafd37208cd722554b5a6ede1e5ba170c")
        version("5.1.3", sha256="6e6a0752654f0d391533df8cedf4b630a78ad34c99087741520c582963ce1602")
        version("5.1.0", sha256="f41329534f2ff477a0db6b7f77a72bb062f117800970c122d676db8b207ce80b")
    version(
        "5.0.2",
        sha256="a266e8b3bbdea04617260f51b3d85cc672af6ca417cae0812d04fd9702429c47",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="0a1754508e06d3a6b17593a71a3c57a3e25d3b46d88573098fda11442853196c",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="81ca24491fbf2bc8e5aa477a6c38776877579ac9f4241ddadeca76a579a7ebb5",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="1049c490fc2008d701a16d14e11004e3bc5b4da993aa48b117e3c44be5677e3c",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="e5757b5213b880237ae0f24616088f79c449c2955cf2133642dbbc9c655f4691",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="194fbd589ce34471f3255f71ea5fca2d27bee47a464558a86d0713b4d26237ea",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="cdedf3766c10200d3ebabe86cbb9c0fe6504e4b3317dccca289327d7c189bb3f",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="66710c390489922f0bd1ac38fd8c32fcfb5b7760b92c2d282f7d1abf214742ee",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="fc3736b2ea203209021616b2ffbcdd664781d692b07b8e8bb7f78b42dabbd5e5",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="7fd863ebf6eed09325c23ba06d9008b2f2c1345283d1a331e329e1a512b602f7",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="ab0ea3dd9b68a126291ed5a35e50fc85d0aeb35fe862f5d9e544435e4262c435",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="8874c100e9ba54587a6057c2a0e555a0903254a16e9e01c2385bae1b027f83b5",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="a2f02d8fc6ad9a561f06dacde54ecafd30563c5c95f93819a5694e5b650dad7f",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="fa16b2a307a5d9716066c2876febcbc1cef855bf0c96d235d2d8f2206a0fb69d",
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

    depends_on("hip +cuda", when="+cuda")

    depends_on("cmake@3.5:", type="build")
    depends_on("git", type="build")

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
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
    ]:
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)
        depends_on("rocsparse@" + ver, when="+rocm @" + ver)

    for tgt in ROCmPackage.amdgpu_targets:
        depends_on(
            "rocsparse amdgpu_target={0}".format(tgt), when="+rocm amdgpu_target={0}".format(tgt)
        )

    patch("e79985dccde22d826aceb3badfc643a3227979d2.patch", when="@3.5.0")
    patch("530047af4a0f437dafc02f76b3a17e3b1536c7ec.patch", when="@3.5.0")
    patch("0a90ddc4c33ed409a938513b9dbdca8bfad65e06.patch", when="@:5.4")

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
            self.define("CMAKE_CXX_STANDARD", "14"),
            self.define("BUILD_CLIENTS_SAMPLES", "OFF"),
            self.define("BUILD_CLIENTS_TESTS", "OFF"),
        ]

        args.append(self.define_from_variant("BUILD_CUDA", "cuda"))

        # FindHIP.cmake was used for +rocm until 5.0.0 and is still used for +cuda
        if self.spec.satisfies("@:4") or self.spec.satisfies("+cuda"):
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
