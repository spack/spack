# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hipcub(CMakePackage, CudaPackage, ROCmPackage):
    """Radeon Open Compute Parallel Primitives Library"""

    homepage = "https://github.com/ROCm/hipCUB"
    git = "https://github.com/ROCm/hipCUB.git"
    url = "https://github.com/ROCm/hipCUB/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    license("BSD-3-Clause")

    maintainers("srekolam", "renjithravindrankannath")
    version("6.0.2", sha256="3f912a23dc34510cf18d9097f6eda37e01d01724975c8149c92a64c92415968c")
    version("6.0.0", sha256="8d9f6e1e3f8433a2ceae1b0efd6727c21383980077e264725d00d5fee165bd30")
    version("5.7.1", sha256="9b23a58408bc4c549d3c754196cb3e2c1a50e177ab0a286101cbea2f7f173945")
    version("5.7.0", sha256="899356867f662d9a6f3870bb4a496f605a3143c6ad4d1fa9e9faead68fa8d13b")
    version("5.6.1", sha256="4b9479daa40424c9ddbc14ce967aa170680f8ca1ed01a514e6e30ccfa22552ce")
    version("5.6.0", sha256="5e74ddbf833f39836bf9ec6c6750348c7386a85ca67aaf9bb54d16c9e1959031")
    version("5.5.1", sha256="ad83f3f1ed85ead9e3012906957c125a896168be913f6fb6af298228fc571480")
    version("5.5.0", sha256="3eec838119326a67eb4cc006c706e328f3a51a01e98bbfb518df8fe4a4707e13")
    version("5.4.3", sha256="cf528d9acb4f9b9c3aad439ae76bfc3d02be6e7a74d96099544e5d54e1a23675")
    version("5.4.0", sha256="78db2c2ea466a4c5d84beedc000ae934f6d0ff1793eae90bb8d02b2dbff8932c")
    version("5.3.3", sha256="b4fc3c05892729873dc098f111c31f83af7d33da572bdb7d87de100d4c238e6d")
    version("5.3.0", sha256="4016cfc240b3cc1a97b549ecc4a5b76369610d46247661834630846391e5fad2")
    with default_args(deprecated=True):
        version("5.2.3", sha256="cab929f10c649f8fd76df989a16d0cd9301bc6aaad91cd2f84498c831378d559")
        version("5.2.1", sha256="07b34d8cdf885838dde264c2a70044505e7b9632cb6efbdb52e2569f95112970")
        version("5.2.0", sha256="ac4dc2310f0eb657e1337c93d8cc4a5d8396f9544a7336eeceb455678a1f9139")
        version("5.1.3", sha256="dc75640689b6a5e15dd3acea643266bdf114ea63efc60be8272f484cf8f04494")
        version("5.1.0", sha256="b30d51fc5fca2584f0c9a6fa8dafc9fbdda96a3acff30288e49b397f8842f705")
    version(
        "5.0.2",
        sha256="22effb18f2c38d76fa379f14c9f9ee7a11987a5d1ae4a7e837af87232c8c9183",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="09c4f1b88aa5f50f04043d379e4960dab556e0fbdf8e25ab03d02a07c1ff7b2f",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="bec9ba1a6aa0475475ee292e54807accc839ed001338275f48da13e3bfb77514",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="5902fae0485789f1d1cc6b8e81d9f1b39338170d3139844d5edf0d324f9694c9",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="20fcd34323c541c182655b7ff6dc6ff268c0127596f0d9993884621c2b14b67a",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="733499a8d55e2d73bf874d43a98ee7425e4325f77e03fb0c80debf36c740cb70",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="56b50e185b7cdf4615d2f56d3a4e86fe76f885e9ad04845f3d0671afcb315c69",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="6d33cc371b9a5ac9c0ab9853bac736f6cea0d2192f4dc9e6d8175d207ee4b4f2",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="656bd6ec547810fd74bcebba41453e6e729f3fdb7346f5564ab71fc0346c3fb5",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="759da5c6ef0cc1e4ecf2083659e78b8bbaa015f0bb360177674e0feb3032c5be",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="c46995f9f18733ec18e370c21d7c0d6ac719e8e9d3254c6303a20ba90831e12e",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="11d7d97268aeb953c34a80125c4577e27cb57cb6095606533105cecf2bd2ec9c",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="a2438632ea1606e83a8c0e1a8777aa5fdca66d77d90862642eb0ec2314b4978d",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="1eb2cb5f6e90ed1b7a9ac6dd86f09ec2ea27bceb5a92eeffa9c2123950c53b9d",
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

    depends_on("cmake@3.10.2:", type="build", when="@4.2.0:")
    depends_on("cmake@3.5.1:", type="build")

    depends_on("hip +cuda", when="+cuda")

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
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
    ]:
        depends_on("rocprim@" + ver, when="+rocm @" + ver)
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)

    # fix hardcoded search in /opt/rocm and broken config mode search
    patch("find-hip-cuda-rocm-5.1.patch", when="@5.1:5.2 +cuda")
    patch("find-hip-cuda-rocm-5.3.patch", when="@5.3: +cuda")

    def setup_build_environment(self, env):
        if self.spec.satisfies("+rocm"):
            env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        args = [self.define("BUILD_TEST", self.run_tests)]

        if self.spec.satisfies("+rocm ^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        # FindHIP.cmake was used for +rocm until 3.7.0 and is still used for +cuda
        if self.spec.satisfies("@:3.7.0") or self.spec.satisfies("+cuda"):
            if self.spec["hip"].satisfies("@:5.1"):
                args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.cmake))
            else:
                args.append(
                    self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip)
                )

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        return args
