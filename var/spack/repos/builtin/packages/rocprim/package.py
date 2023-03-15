# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rocprim(CMakePackage):
    """Radeon Open Compute Parallel Primitives Library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocPRIM"
    git = "https://github.com/ROCmSoftwarePlatform/rocPRIM.git"
    url = "https://github.com/ROCmSoftwarePlatform/rocPRIM/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath")

    version("5.4.3", sha256="7be6314a46195912d3203e7e59cb8880a46ed7c1fd221e92fadedd20532e0e48")
    version("5.4.0", sha256="1740dca11c70ed350995331c292f7e3cb86273614e4a5ce9f0ea64dea5364318")
    version("5.3.3", sha256="21a6b352ad3f5b2b7d05a5ed55e612feb3c5c19d34fdb8f80260b6d25af18b2d")
    version("5.3.0", sha256="4885bd662b038c6e9f058a756fd838203dbd00227bfef6adaf31496010b100e4")
    version("5.2.3", sha256="502f49cf3190f4ac20d0a6b19eb2d0786bb3c5661329940378081f1678aa8e82")
    version("5.2.1", sha256="47f09536b0afbb7be4d6fb71cca9f0a4fa58dde29c83aee247d4b167f6f3acae")
    version("5.2.0", sha256="f99eb7d2f6b1445742fba631a0dc8bb0d464a767a9c4fb79ac865d9570fe747b")
    version("5.1.3", sha256="b5a08d2e76388bd1ffa6c946009928fe95de846ab6b65a6475998070c0cf6dc1")
    version("5.1.0", sha256="dfe106c01155e00ed816f0231d1576ff8c08750cc8278fa453926f388dc6fe48")
    version(
        "5.0.2",
        sha256="a4280f15d470699a1c6a5f86bdd951c1387e0af227c6bee6f81cee658406f4b0",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="0e7e7bda6a09b70a07ddd926986882df0c8d8ff3e0a34e12cb6d44f7d0a5840e",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="0dc673847e67db672f2e239f299206fe16c324005ddd2e92c7cb7725bb6f4fa6",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="6f0ca1da9a93064af662d6c61fbdb56bb313f8edca85615ead0dd284eb481089",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="d29ffcb5dd1c6155c586b9952fa4c11b717d90073feb083db6b03ea74746194b",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="f6cf53b5fa07a0d6f508e39c7da5b11f562c0cac4b041ec5c41a8fc733f707c7",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="3932cd3a532eea0d227186febc56747dd95841732734d9c751c656de9dd770c8",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="c46d789f85d15f8ec97f90d67b9d49fb87239912fe8d5f60a7b4c59f9d0e3da8",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="61abf4d51853ae71e54258f43936bbbb096bf06f5891d224d359bfe3104015d0",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="b406956b27d1c06b749e991a250d4ad3eb26e20c6bebf121e2ca6051597b4fa4",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="ace6b4ee4b641280807028375cb0e6fa7b296edba9e9fc09177a5d8d075a716e",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="4d37320d174eaada99dd796d81fa97d5dcc65a6dff8e8ff1c21e8e68acb4ea74",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="225209a0cbd003c241821c8a9192cec5c07c7f1a6ab7da296305fc69f5f6d365",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="29302dbeb27ae88632aa1be43a721f03e7e597c329602f9ca9c9c530c1def40d",
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

    depends_on("cmake@3.10.2:", type="build", when="@4.2.0:")
    depends_on("cmake@3.5.1:", type="build")
    depends_on("numactl", type="link", when="@3.7.0:")

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
        depends_on("comgr@" + ver, when="@" + ver)
        depends_on("hsa-rocr-dev@" + ver, when="@" + ver)
        depends_on("llvm-amdgpu@" + ver, when="@" + ver)
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)

    # the patch is meant for 5.3.0 only.this is already in the 5.3.3+ releases
    patch("fix-device-merge-mismatched-param-5.3.0.patch", when="@5.3.0")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        args = [
            self.define("ONLY_INSTALL", "ON"),
            self.define("BUILD_TEST", "OFF"),
            self.define("BUILD_BENCHMARK", "OFF"),
            self.define("BUILD_EXAMPLE", "OFF"),
        ]

        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@:5.1.3"):
            args.append("-DCMAKE_MODULE_PATH={0}".format(self.spec["hip"].prefix.cmake))
        elif self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        return args
