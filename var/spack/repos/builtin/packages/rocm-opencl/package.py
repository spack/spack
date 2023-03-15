# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class RocmOpencl(CMakePackage):
    """OpenCL: Open Computing Language on ROCclr"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime"
    git = "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime.git"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["libOpenCL"]

    def url_for_version(self, version):
        if version == Version("3.5.0"):
            return (
                "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/roc-3.5.0.tar.gz"
            )

        url = "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/rocm-{0}.tar.gz"
        return url.format(version)

    version("master", branch="main")

    version("5.4.3", sha256="b0f8339c844a2e62773bd85cd1e7c5ecddfe71d7c8e8d604e1a1d60900c30873")
    version("5.4.0", sha256="a294639478e76c75dac0e094b418f9bd309309b07faf6af126cdfad9aab3c5c7")
    version("5.3.3", sha256="cab394e6ef16c35bab8de29a66b96a7dc0e7d1297aaacba3718fa1d369233c9f")
    version("5.3.0", sha256="d251e2efe95dc12f536ce119b2587bed64bbda013969fa72be58062788044a9e")
    version("5.2.3", sha256="932ea3cd268410010c0830d977a30ef9c14b8c37617d3572a062b5d4595e2b94")
    version("5.2.1", sha256="eb4ff433f8894ca659802f81792646034f8088b47aca6ad999292bcb8d6381d5")
    version("5.2.0", sha256="80f73387effdcd987a150978775a87049a976aa74f5770d4420847b004dd59f0")
    version("5.1.3", sha256="44a7fac721abcd93470e1a7e466bdea0c668c253dee93e4f1ea9a72dbce4ba31")
    version("5.1.0", sha256="362d81303048cf7ed5d2f69fb65ed65425bc3da4734fff83e3b8fbdda51b0927")
    version(
        "5.0.2",
        sha256="3edb1992ba28b4a7f82dd66fbd121f62bd859c1afb7ceb47fa856bd68feedc95",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="2aa3a628b336461f83866c4e76225ef5338359e31f802987699d6308515ae1be",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="96b43f314899707810db92149caf518bdb7cf39f7c0ad86e98ad687ffb0d396d",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="3a163aed24619b3faf5e8ba17325bdcedd1667a904ea20914ac6bdd33fcdbca8",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="7f98f7d4707b4392f8aa7017aaca9e27cb20263428a1a81fb7ec7c552e60c4ca",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="d37bddcc6835b6c0fecdf4d02c204ac1d312076f3eef2b1faded1c4c1bc651e9",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="18133451948a83055ca5ebfb5ba1bd536ed0bcb611df98829f1251a98a38f730",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="0729e6c2adf1e3cf649dc6e679f9cb936f4f423f4954ad9852857c0a53ef799c",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="d43ea5898c6b9e730b5efabe8367cc136a9260afeac5d0fe85b481d625dd7df1",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="3aa9dc5a5f570320b04b35ee129ce9ff21062d2770df934c6c307913f975e93d",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="286ff64304905384ce524cd8794c28aee216befd6c9267d4187a12e5a21e2daf",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="7f75dd1abf3d771d554b0e7b0a7d915ab5f11a74962c92b013ee044a23c1270a",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="283e1dfe4c3d2e8af4d677ed3c20e975393cdb0856e3ccd77b9c7ed2a151650b",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="511b617d5192f2d4893603c1a02402b2ac9556e9806ff09dd2a91d398abf39a0",
        deprecated=True,
    )

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    depends_on("cmake@3:", type="build")
    depends_on("gl@4.5:", type="link")
    depends_on("numactl", type="link", when="@3.7.0:")

    for d_version, d_shasum in [
        ("5.4.3", "71d9668619ab57ec8a4564d11860438c5aad5bd161a3e58fbc49555fbd59182d"),
        ("5.4.0", "46a1579310b3ab9dc8948d0fb5bed4c6b312f158ca76967af7ab69e328d43138"),
        ("5.3.3", "f8133a5934f9c53b253d324876d74f08a19e2f5b073bc94a62fe64b0d2183a18"),
        ("5.3.0", "2bf14116b5e2270928265f5d417b3d0f0f2e13cbc8ec5eb8c80d4d4a58ff7e94"),
        ("5.2.3", "0493c414d4db1af8e1eb30a651d9512044644244488ebb13478c2138a7612998"),
        ("5.2.1", "465ca9fa16869cd89dab8c2d66d9b9e3c14f744bbedaa1d215b0746d77a500ba"),
        ("5.2.0", "37f5fce04348183bce2ece8bac1117f6ef7e710ca68371ff82ab08e93368bafb"),
        ("5.1.3", "ddee63cdc6515c90bab89572b13e1627b145916cb8ede075ef8446cbb83f0a48"),
        ("5.1.0", "f4f265604b534795a275af902b2c814f416434d9c9e16db81b3ed5d062187dfa"),
        ("5.0.2", "34decd84652268dde865f38e66f8fb4750a08c2457fea52ad962bced82a03e5e"),
        ("5.0.0", "6b72faf8819628a5c109b2ade515ab9009606d10f11316f0d7e4c4c998d7f724"),
        ("4.5.2", "6581916a3303a31f76454f12f86e020fb5e5c019f3dbb0780436a8f73792c4d1"),
        ("4.5.0", "ca8d6305ff0e620d9cb69ff7ac3898917db9e9b6996a7320244b48ab6511dd8e"),
    ]:
        resource(
            name="rocclr",
            url="https://github.com/ROCm-Developer-Tools/ROCclr/archive/rocm-{0}.tar.gz".format(
                d_version
            ),
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="rocclr",
            when="@{0}".format(d_version),
        )
    # Patch to set package installation path for OpenCL.
    patch("0001-fix-build-error-rocm-opencl-5.1.0.patch", when="@5.1.0:5.1")

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
        "master",
    ]:
        depends_on("hip-rocclr@" + ver, type="build", when="@" + ver)
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
        "master",
    ]:
        depends_on("comgr@" + ver, type="build", when="@" + ver)
        depends_on("hsa-rocr-dev@" + ver, type="link", when="@" + ver)

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

    def flag_handler(self, name, flags):
        # The includes are messed up in ROCm 3.5.0:
        # ROCM-OpenCL-Runtime uses flat includes
        # and the find_package(ROCclr) bit it
        # commented out. So instead we provide
        # all the includes...

        if self.spec.satisfies("@:4.3.2") and name in ("cflags", "cxxflags"):
            rocclr = self.spec["hip-rocclr"].prefix
            extra_includes = [
                "include",
                "include/compiler/lib/include",
                "include/elf",
                "compiler/lib",
                "compiler/lib/include",
                "elf/utils/libelf",
                "elf/utils/common",
            ]

            for p in extra_includes:
                flag = "-I {0}".format(join_path(rocclr, p))
                flags.append(flag)

        return (flags, None, None)

    def cmake_args(self):
        args = ["-DUSE_COMGR_LIBRARY=yes"]
        if self.spec.satisfies("@:4.3.0"):
            "-DROCclr_DIR={0}".format(self.spec["hip-rocclr"].prefix),
            "-DLIBROCclr_STATIC_DIR={0}/lib".format
            (self.spec["hip-rocclr"].prefix)
        if "@4.5.0:" in self.spec:
            args.append(self.define("ROCCLR_PATH", self.stage.source_path + "/rocclr"))
            args.append(self.define("AMD_OPENCL_PATH", self.stage.source_path))
        return args

    def setup_run_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib),
        env.set("OCL_ICD_VENDORS", self.prefix.vendors + "/")

    @run_after("install")
    def post_install(self):
        vendor_config_path = join_path(self.prefix + "/vendors")
        mkdirp(vendor_config_path)

        config_file_name = "amdocl64_30800.icd"
        with open(join_path(vendor_config_path, config_file_name), "w") as f:
            f.write("libamdocl64.so")
