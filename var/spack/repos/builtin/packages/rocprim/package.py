# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rocprim(CMakePackage):
    """Radeon Open Compute Parallel Primitives Library"""

    homepage = "https://github.com/ROCm/rocPRIM"
    git = "https://github.com/ROCm/rocPRIM.git"
    url = "https://github.com/ROCm/rocPRIM/archive/rocm-6.1.0.tar.gz"
    tags = ["rocm"]

    license("MIT")

    maintainers("cgmb", "srekolam", "renjithravindrankannath")
    version("6.1.1", sha256="94b265b6b4ed366b0ba008ef77ab6623b7b880b45874f202c887f01b67905922")
    version("6.1.0", sha256="9f02e5f8be90baa679a28f83927495ddf0e17d684536e1f820021e8c3e8e6c84")
    version("6.0.2", sha256="d3998720d3206965335902f8f67ca497b320a33b810cd19b2a2264505cb38779")
    version("6.0.0", sha256="51f26c9f891a64c8db8df51d75d86d404d682092fd9d243e966ac6b2a6de381a")
    version("5.7.1", sha256="15d820a0f61aed60efbba88b6efe6942878b02d912f523f9cf8f33a4583d6cd7")
    version("5.7.0", sha256="a1bf94bbad13a0410b49476771270606d8a9d257188ee3ec3a37eee80540fe9b")
    version("5.6.1", sha256="e9ec1b0039c07cf3096653a04224fe5fe755afc6ba000f6838b3a8bc84df27de")
    version("5.6.0", sha256="360d6ece3c4a3c289dd88043432026fb989e982ae4d05230d8cdc858bcd50466")
    version("5.5.1", sha256="63cdc682afb39efd18f097faf695ce64c851c4a550a8ad96fa89d694451b6a42")
    version("5.5.0", sha256="968d9059f93d3f0f8a602f7b989e54e36cff2f9136486b6869e4534a5bf8c7d9")
    version("5.4.3", sha256="7be6314a46195912d3203e7e59cb8880a46ed7c1fd221e92fadedd20532e0e48")
    version("5.4.0", sha256="1740dca11c70ed350995331c292f7e3cb86273614e4a5ce9f0ea64dea5364318")
    version("5.3.3", sha256="21a6b352ad3f5b2b7d05a5ed55e612feb3c5c19d34fdb8f80260b6d25af18b2d")
    version("5.3.0", sha256="4885bd662b038c6e9f058a756fd838203dbd00227bfef6adaf31496010b100e4")
    with default_args(deprecated=True):
        version("5.2.3", sha256="502f49cf3190f4ac20d0a6b19eb2d0786bb3c5661329940378081f1678aa8e82")
        version("5.2.1", sha256="47f09536b0afbb7be4d6fb71cca9f0a4fa58dde29c83aee247d4b167f6f3acae")
        version("5.2.0", sha256="f99eb7d2f6b1445742fba631a0dc8bb0d464a767a9c4fb79ac865d9570fe747b")
        version("5.1.3", sha256="b5a08d2e76388bd1ffa6c946009928fe95de846ab6b65a6475998070c0cf6dc1")
        version("5.1.0", sha256="dfe106c01155e00ed816f0231d1576ff8c08750cc8278fa453926f388dc6fe48")

    amdgpu_targets = ROCmPackage.amdgpu_targets

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )

    depends_on("cmake@3.10.2:", type="build")
    depends_on("numactl", type="link")
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
        depends_on(f"comgr@{ver}", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")

    # the patch is meant for 5.3.0 only.this is already in the 5.3.3+ releases
    patch("fix-device-merge-mismatched-param-5.3.0.patch", when="@5.3.0")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        args = [
            self.define("ONLY_INSTALL", (not self.run_tests)),
            self.define("BUILD_TEST", self.run_tests),
            self.define("BUILD_BENCHMARK", "OFF"),
            self.define("BUILD_EXAMPLE", "OFF"),
        ]

        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@:5.1"):
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.cmake))
        elif self.spec.satisfies("@5.2:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        return args
