# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Rocthrust(CMakePackage):
    """Thrust is a parallel algorithm library. This library has been ported to
    HIP/ROCm platform, which uses the rocPRIM library. The HIP ported
    library works on HIP/ROCm platforms"""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocThrust"
    git = "https://github.com/ROCmSoftwarePlatform/rocThrust.git"
    url = "https://github.com/ROCmSoftwarePlatform/rocThrust/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath")

    version("5.4.3", sha256="d133e14ea6d27d358d1bd4d31b79fb1562d1aea7c400e5a2d28d0f159cb6c8a8")
    version("5.4.0", sha256="a4799fb1086da3f70c9b95effb1f5f9033c861685e960a8759278463cc55a971")
    version("5.3.3", sha256="0c2fc8d437efaf5c4c859d97adb049d4025025d0be0e0908f59a8112508234e5")
    version("5.3.0", sha256="0e11b12f208d2751e3e507e3a32403c9bd45da4e191671d765d33abd727d9b96")
    version("5.2.3", sha256="0f5ef39c5faab31eb34b48391d58096463969c133ca7ed09ab4e43caa5461b29")
    version("5.2.1", sha256="5df35ff0970b83d68b69a07ae9ebb62955faac7401c91daa7929664fdd09d69b")
    version("5.2.0", sha256="afa126218485586682c78e97df8025ae4efd32f3751c340e84c436e08868c326")
    version("5.1.3", sha256="8d92de1e69815d92a423b7657f2f37c90f1d427f5bc92915c202d4c266254dad")
    version("5.1.0", sha256="fee779ae3d55b97327d87beca784fc090fa02bc95238d9c3bf3021e266e73979")
    version(
        "5.0.2",
        sha256="60f0cf1848cc7cd8663f15307bd695eee3c5b20d3ad3baa4bc696189ffdcfd53",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="10b7b1be919881904d64f8084c2afe22aa00c560f8493a75dbf5df8386443ab4",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="9171a05dd7438aebd4f6a939b1b33b7e87be1a0bd52d90a171b74539885cf591",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="86cf897b01a6f5df668d978ce42d44a6ae9df9f8adc92d0a1a49a7c3bbead259",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="86fcd3bc275efe9a485aed48afdc6d3351804c076caee43e3fb8bd69752865e9",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="a50eb6500687b4ea9e0b3affb1daff8bbc56199d39fbed3ee61d2d5bfc1a0271",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="da2b6c831c26c26058218b0c5b7b2e43fd7f0dac3b2e3a8e39a839145592c727",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="e3d06c0387a2a6880776c7423b1acf0808fb8833bc822be75793da8c2f521efd",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="120c87316f44ce8e8975e57c9b9bf1246b1ffc00879d31d744289ba9438a976c",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="31bea6cd19a0ffa15e4ab50ecde2402ea5aaa182149cfab98242357e41f1805b",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="65f5e74d72c5aaee90459468d693b212af7d56e31098ee8237b18d1b4d620eb0",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="39350aeb8bfbcd09e387717b2a05c7e3a19e0fa85ff4284b967bb8fae12f9013",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="4cb923dde5eec150a566cb10d23ee5c7ce3aa892c4dea94886a89d95b90f3bdd",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="0d1bac1129d17bb1259fd06f5c9cb4c1620d1790b5c295b866fb3442d18923cb",
        deprecated=True,
    )

    amdgpu_targets = ROCmPackage.amdgpu_targets

    # the rocthrust library itself is header-only, but the build_type and amdgpu_target
    # are relevant to the test client
    variant("amdgpu_target", values=auto_or_any_combination_of(*amdgpu_targets), sticky=True)
    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )
    depends_on("cmake@3.10.2:", type="build", when="@4.2.0:")
    depends_on("cmake@3.5.1:", type="build")

    depends_on("googletest@1.10.0:", type="test")

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
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("rocprim@" + ver, when="@" + ver)
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        args = [
            self.define("CMAKE_MODULE_PATH", "{0}/cmake".format(self.spec["hip"].prefix)),
            self.define("BUILD_TEST", self.run_tests),
        ]

        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        return args
