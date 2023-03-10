# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.boost import Boost


class RocmTensile(CMakePackage):
    """Radeon Open Compute Tensile library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/Tensile/"
    git = "https://github.com/ROCmSoftwarePlatform/Tensile.git"
    url = "https://github.com/ROCmSoftwarePlatform/Tensile/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "haampie")

    version("5.4.3", sha256="a4c5e62edd33ea6b8528eb3f017a14c28eaa67c540f5c9023f6a245340198b0f")
    version("5.4.0", sha256="2da9c1df3c6d9b44afdad621ef59a03389fb1a38a61a8b8bad9c9991b97157eb")
    version("5.3.3", sha256="ecb99243edf1cd2bb5e953915a7dae7867c3cdb0cd8ed15b8618aaaeb2bd7b29")
    version("5.3.0", sha256="05c546986549154e6c7b4f57a0b3bfd5cb223d2393c206ff1702f89454c832f4")
    version("5.2.3", sha256="840698bf2ac62e08ae76c3843f1dad5367ed098d42e6a5fa7953de70642fd2cf")
    version("5.2.1", sha256="49582e28f7e14fed6a66c59482a41d3899c1eb8e7aa0ce40a7a2e806dadc536b")
    version("5.2.0", sha256="aa6107944482ad278111d11d2e926393423fc70e7e1838574fe7ad9f553bdacf")
    version("5.1.3", sha256="87020ca268e3a1ed8853f629839d6497764d862bd70b8775e98de439f6c89f1d")
    version("5.1.0", sha256="0ac86a623597152c5b1d8bb5634aad3e55afa51959476aaa5e9869d259ddf375")
    version(
        "5.0.2",
        sha256="c6130de3b02f4f10635d18f913b3b88ea754fce2842c680e9caf5a6781da8f37",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="2a814ee8576ff1f06cc5ac4556300c8e7cbf77ef8c87b56992f3e66d8862f213",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="da20256224749c0a8b44aaede25fbcd66cfeac483081af5d22f1d1fcf49dffc1",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="26a27659c864b5372ca4407671c6e8d4be3bbc05c64fc18762ad570cd3b3af1f",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="6fce0ac22051a454fe984283766eb473dc50752cd30bad05acb3dbde6ef4f8b1",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="911c0cdb0146d43a2a59170e6a803f414a2b68df7d9ff369ab784d11a08d7264",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="198e357a14a79366b27b1097856d4821996bc36163be0cd2668910b253721060",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="92b8ee13dfc11a67d5136227ee985622685790fd3f0f0e1ec6db411d4e9a3419",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="cf105ce8c3e352d19713b3bf8bda77f25c1a692c4f2ca82d631ba15523ecc1cd",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="8d5b50aadfa56a9195e4c387b8eb351c9b9b7671b136b624e07fe28db24bd330",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="17a011f8c3433d4f8c2dddabd5854cf96c406d24592b3942deb51672c570882e",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="c78a11db85fdf54bfd26533ee6fa98f6a6e789fa423537993061497ac5f22ed6",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="488a7f76ea42a7601d0557f53068ec4832a2c7c06bb1b511470a4e35599a5a4d",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="71eb3eed6625b08a4cedb539dd9b596e3d4cc82a1a8063d37d94c0765b6f8257",
        deprecated=True,
    )

    tensile_architecture = (
        "all",
        "gfx906",
        "gfx908",
        "gfx000",
        "gfx900",
        "gfx906:xnack-",
        "gfx908:xnack-",
        "gfx90a:xnack-",
        "gfx1010",
        "gfx1011",
        "gfx1012",
        "gfx1030",
    )

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )
    variant("tensile_architecture", default="all", values=tensile_architecture, multi=True)
    variant("openmp", default=True, description="Enable OpenMP")
    conflicts("tensile_architecture=gfx906", when="@4.0.1:")
    conflicts("tensile_architecture=gfx908", when="@4.0.1:")
    depends_on("cmake@3:", type="build")
    # This is the default library format since 3.7.0
    depends_on("msgpack-c@3:", when="@3.7:")
    depends_on("boost", type=("build", "link"))
    depends_on(Boost.with_default_variants)

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
        depends_on("rocm-cmake@" + ver, type="build", when="@" + ver)
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("comgr@" + ver, when="@" + ver)
        depends_on("rocminfo@" + ver, type="build", when="@" + ver)

    for ver in ["5.1.0", "5.1.3", "5.2.0", "5.2.1", "5.2.3", "5.3.0", "5.3.3", "5.4.0", "5.4.3"]:
        depends_on("rocm-openmp-extras@" + ver, when="@" + ver)

    for ver in ["3.5.0", "3.7.0", "3.8.0", "3.9.0"]:
        depends_on("rocm-smi@" + ver, type="build", when="@" + ver)

    for ver in [
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
        depends_on("rocm-smi-lib@" + ver, type="build", when="@" + ver)

    root_cmakelists_dir = "Tensile/Source"
    # Status: https://github.com/ROCmSoftwarePlatform/Tensile/commit/a488f7dadba34f84b9658ba92ce9ec5a0615a087
    # Not yet landed in 3.7.0, nor 3.8.0.
    patch("0001-fix-compile-error.patch", when="@3.7.0:3.8.0")
    patch("0002-require-openmp-when-tensile-use-openmp-is-on.patch", when="@3.9.0:4.0.0")
    patch("0003-require-openmp-extras-when-tensile-use-openmp.patch", when="@5.1.0:")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def get_gpulist_for_tensile_support(self):
        arch = self.spec.variants["tensile_architecture"].value
        if arch[0] == "all":
            if self.spec.satisfies("@:4.0.0"):
                arch_value = self.tensile_architecture[1:4]
            elif self.spec.satisfies("@4.1.0:4.2.0"):
                arch_value = self.tensile_architecture[3:6]
            elif self.spec.satisfies("@4.3.0:"):
                arch_value = self.tensile_architecture[3:]
            return arch_value
        else:
            return arch

    def cmake_args(self):
        args = [
            self.define("amd_comgr_DIR", self.spec["comgr"].prefix),
            self.define("Tensile_COMPILER", "hipcc"),
            self.define("Tensile_LOGIC", "asm_full"),
            self.define("Tensile_CODE_OBJECT_VERSION", "V3"),
            self.define("Boost_USE_STATIC_LIBS", "OFF"),
            self.define("BUILD_WITH_TENSILE_HOST", "ON" if "@3.7.0:" in self.spec else "OFF"),
        ]

        if "@3.7.0:" in self.spec:
            args.append(self.define("Tensile_LIBRARY_FORMAT", "msgpack"))
        if "@5.1.0:" in self.spec:
            args.append(self.define("TENSILE_USE_OPENMP", "ON")),
            args.append(
                self.define("ROCM_OPENMP_EXTRAS_DIR", self.spec["rocm-openmp-extras"].prefix)
            ),
        else:
            args.append(self.define("TENSILE_USE_OPENMP", "OFF")),

        args.append(self.define("Tensile_ARCHITECTURE", self.get_gpulist_for_tensile_support()))

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        return args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            install_tree("./client", prefix.client)
            install_tree("./lib", prefix.lib)
