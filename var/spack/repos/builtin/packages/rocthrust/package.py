# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Rocthrust(CMakePackage):
    """Thrust is a parallel algorithm library. This library has been ported to
    HIP/ROCm platform, which uses the rocPRIM library. The HIP ported
    library works on HIP/ROCm platforms"""

    homepage = "https://github.com/ROCm/rocThrust"
    git = "https://github.com/ROCm/rocThrust.git"
    url = "https://github.com/ROCm/rocThrust/archive/rocm-6.1.1.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath")
    version("6.1.1", sha256="03420d8af687107775a1fbd3db5e8c9872c7c738747de77a5e8c0b3466a3321a")
    version("6.1.0", sha256="8c36fb7b34758579601365a450700899133da5802e5c8370654051b190bd6e1c")
    version("6.0.2", sha256="8de9414f6b921ff549ba102239fcf65f5cc70ece5eec9753de5ec91870e6934d")
    version("6.0.0", sha256="a3fdafe4b6124118e07f23a3b0270d91740da324f61aaa3e8c034da08d9312b1")
    version("5.7.1", sha256="b7cb9ea6c42b2c6b610c34d2c438443e0f99245bd391aff18591949bf1cd53ee")
    version("5.7.0", sha256="64e10f071acfc5b8e3c168b9178289cf1afc7b168bf1962793fc256b25074d3a")
    version("5.6.1", sha256="63df61d5ab46d4cfda6066d748274bacecc77151692e372e6f7df5e91852bdc2")
    version("5.6.0", sha256="e52a27bcb4add38a5f0f3a5c7e409c230bf4ba9afae19bd2e06c2be00d39db59")
    version("5.5.1", sha256="66f126e5ea46ca761533411f81e83402773f95d3184cb7645ca73df227413023")
    version("5.5.0", sha256="c031f71cd4b6eaf98664fd2ad50fc18f7ccbfa67be415dca425169d2d1c81e9e")
    version("5.4.3", sha256="d133e14ea6d27d358d1bd4d31b79fb1562d1aea7c400e5a2d28d0f159cb6c8a8")
    version("5.4.0", sha256="a4799fb1086da3f70c9b95effb1f5f9033c861685e960a8759278463cc55a971")
    version("5.3.3", sha256="0c2fc8d437efaf5c4c859d97adb049d4025025d0be0e0908f59a8112508234e5")
    version("5.3.0", sha256="0e11b12f208d2751e3e507e3a32403c9bd45da4e191671d765d33abd727d9b96")
    with default_args(deprecated=True):
        version("5.2.3", sha256="0f5ef39c5faab31eb34b48391d58096463969c133ca7ed09ab4e43caa5461b29")
        version("5.2.1", sha256="5df35ff0970b83d68b69a07ae9ebb62955faac7401c91daa7929664fdd09d69b")
        version("5.2.0", sha256="afa126218485586682c78e97df8025ae4efd32f3751c340e84c436e08868c326")
        version("5.1.3", sha256="8d92de1e69815d92a423b7657f2f37c90f1d427f5bc92915c202d4c266254dad")
        version("5.1.0", sha256="fee779ae3d55b97327d87beca784fc090fa02bc95238d9c3bf3021e266e73979")

    amdgpu_targets = ROCmPackage.amdgpu_targets

    # the rocthrust library itself is header-only, but the build_type and amdgpu_target
    # are relevant to the test client
    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )
    depends_on("cmake@3.10.2:", type="build")

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
    ]:
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"rocprim@{ver}", when=f"@{ver}")
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")

    def check(self):
        with working_dir(self.builder.build_directory):
            make("test")

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
