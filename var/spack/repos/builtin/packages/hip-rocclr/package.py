# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class HipRocclr(CMakePackage):
    """Hip-ROCclr is a virtual device interface that compute runtimes interact
    with to different backends such as ROCr or PAL This abstraction allows
    runtimes to work on Windows as well as on Linux without much effort."""

    homepage = "https://github.com/ROCm/ROCclr"
    git = "https://github.com/ROCm/ROCclr.git"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")

    def url_for_version(self, version):
        # Fix up a typo in the 3.5.0 release.
        if version == Version("3.5.0"):
            return "https://github.com/ROCm/ROCclr/archive/roc-3.5.0.tar.gz"

        url = "https://github.com/ROCm/ROCclr/archive/rocm-{0}.tar.gz"
        return url.format(version)

    license("MIT")

    version("master", branch="main")
    version("5.6.1", sha256="cc9a99c7e4de3d9360c0a471b27d626e84a39c9e60e0aff1e8e1500d82391819")
    version("5.6.0", sha256="864f87323e793e60b16905284fba381a7182b960dd4a37fb67420c174442c03c")
    version("5.5.1", sha256="1375fc7723cfaa0ae22a78682186d4804188b0a54990bfd9c0b8eb421b85e37e")
    version("5.5.0", sha256="efbae9a1ef2ab3de5ca44091e9bb78522e76759c43524c1349114f9596cc61d1")
    version("5.4.3", sha256="71d9668619ab57ec8a4564d11860438c5aad5bd161a3e58fbc49555fbd59182d")
    version("5.4.0", sha256="46a1579310b3ab9dc8948d0fb5bed4c6b312f158ca76967af7ab69e328d43138")
    version("5.3.3", sha256="f8133a5934f9c53b253d324876d74f08a19e2f5b073bc94a62fe64b0d2183a18")
    version("5.3.0", sha256="2bf14116b5e2270928265f5d417b3d0f0f2e13cbc8ec5eb8c80d4d4a58ff7e94")
    version("5.2.3", sha256="0493c414d4db1af8e1eb30a651d9512044644244488ebb13478c2138a7612998")
    version("5.2.1", sha256="465ca9fa16869cd89dab8c2d66d9b9e3c14f744bbedaa1d215b0746d77a500ba")
    version("5.2.0", sha256="37f5fce04348183bce2ece8bac1117f6ef7e710ca68371ff82ab08e93368bafb")
    version("5.1.3", sha256="ddee63cdc6515c90bab89572b13e1627b145916cb8ede075ef8446cbb83f0a48")
    version("5.1.0", sha256="f4f265604b534795a275af902b2c814f416434d9c9e16db81b3ed5d062187dfa")
    version(
        "5.0.2",
        sha256="34decd84652268dde865f38e66f8fb4750a08c2457fea52ad962bced82a03e5e",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="6b72faf8819628a5c109b2ade515ab9009606d10f11316f0d7e4c4c998d7f724",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="6581916a3303a31f76454f12f86e020fb5e5c019f3dbb0780436a8f73792c4d1",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="ca8d6305ff0e620d9cb69ff7ac3898917db9e9b6996a7320244b48ab6511dd8e",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="bda52c65f03a69a9d8ab1a118d45646d76843249fb975d67e5141e63fa3acc79",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="8a86b4f2a1b1c7ac628262e5b11b07ff42a224e62e594a4e0683aeb616062538",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="c57525af32c59becf56fd83cdd61f5320a95024d9baa7fb729a01e7a9fcdfd78",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="9eb1d88cfc9474979aaf29b99bcf9d3769a0f7f1f8f10660941aabf83d9eeb0c",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="8db502d0f607834e3b882f939d33e8abe2f9b55ddafaf1b0c2cd29a0425ed76a",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="d1ac02840c2dcb3d5fa3008fe9e313767ebe6d1dcf978a924341834ec96ebfe2",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="d248958672ae35ab7f9fbd83827ccf352e2756dfa7819f6b614ace2e1a9a064e",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="10d8aa6f5af7b51813015da603c4e75edc863c3530793f6ed9769ca345c08ed6",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="a49f464bb2eab6317e87e3cc249aba3b2517a34fbdfe50175f0437f69a219adc",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="87c1ee9f02b8aa487b628c543f058198767c474cec3d21700596a73c028959e1",
        deprecated=True,
    )

    depends_on("cmake@3:", type="build")
    depends_on("gl@4.5:", type="link")
    depends_on("glx@1.4:", type=("build", "link"))
    depends_on("libelf", type="link", when="@3.7.0:3.8.0")
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
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "master",
    ]:
        depends_on("hsakmt-roct@" + ver, when="@" + ver)
        depends_on("hsa-rocr-dev@" + ver, when="@" + ver)
        depends_on("comgr@" + ver, when="@" + ver)

    # See: https://github.com/ROCm/ROCclr/pull/16
    # In 3.7.0 the find opengl things have changed slightly.
    patch("opengl.patch", when="@3.5.0")

    resource(
        name="opencl-on-vdi",
        url="https://github.com/ROCm/ROCm-OpenCL-Runtime/archive/roc-3.5.0.tar.gz",
        sha256="511b617d5192f2d4893603c1a02402b2ac9556e9806ff09dd2a91d398abf39a0",
        expand=True,
        destination="",
        placement="opencl-on-vdi",
        when="@3.5.0",
    )

    # Add opencl sources thru the below
    for d_version, d_shasum in [
        ("5.6.1", "ec26049f7d93c95050c27ba65472736665ec7a40f25920a868616b2970f6b845"),
        ("5.6.0", "52ab260d00d279c2a86c353901ffd88ee61b934ad89e9eb480f210656705f04e"),
        ("5.5.1", "a8a62a7c6fc5398406d2203b8cb75621a24944688e545d917033d87de2724498"),
        ("5.5.0", "0df9fa0b8aa0c8e6711d34eec0fdf1ed356adcd9625bc8f1ce9b3e72090f3e4f"),
        ("5.4.3", "b0f8339c844a2e62773bd85cd1e7c5ecddfe71d7c8e8d604e1a1d60900c30873"),
        ("5.4.0", "a294639478e76c75dac0e094b418f9bd309309b07faf6af126cdfad9aab3c5c7"),
        ("5.3.3", "cab394e6ef16c35bab8de29a66b96a7dc0e7d1297aaacba3718fa1d369233c9f"),
        ("5.3.0", "d251e2efe95dc12f536ce119b2587bed64bbda013969fa72be58062788044a9e"),
        ("5.2.3", "932ea3cd268410010c0830d977a30ef9c14b8c37617d3572a062b5d4595e2b94"),
        ("5.2.1", "eb4ff433f8894ca659802f81792646034f8088b47aca6ad999292bcb8d6381d5"),
        ("5.2.0", "80f73387effdcd987a150978775a87049a976aa74f5770d4420847b004dd59f0"),
        ("5.1.3", "44a7fac721abcd93470e1a7e466bdea0c668c253dee93e4f1ea9a72dbce4ba31"),
        ("5.1.0", "362d81303048cf7ed5d2f69fb65ed65425bc3da4734fff83e3b8fbdda51b0927"),
        ("5.0.2", "3edb1992ba28b4a7f82dd66fbd121f62bd859c1afb7ceb47fa856bd68feedc95"),
        ("5.0.0", "2aa3a628b336461f83866c4e76225ef5338359e31f802987699d6308515ae1be"),
        ("4.5.2", "96b43f314899707810db92149caf518bdb7cf39f7c0ad86e98ad687ffb0d396d"),
        ("4.5.0", "3a163aed24619b3faf5e8ba17325bdcedd1667a904ea20914ac6bdd33fcdbca8"),
        ("4.3.1", "7f98f7d4707b4392f8aa7017aaca9e27cb20263428a1a81fb7ec7c552e60c4ca"),
        ("4.3.0", "d37bddcc6835b6c0fecdf4d02c204ac1d312076f3eef2b1faded1c4c1bc651e9"),
        ("4.2.0", "18133451948a83055ca5ebfb5ba1bd536ed0bcb611df98829f1251a98a38f730"),
        ("4.1.0", "0729e6c2adf1e3cf649dc6e679f9cb936f4f423f4954ad9852857c0a53ef799c"),
        ("4.0.0", "d43ea5898c6b9e730b5efabe8367cc136a9260afeac5d0fe85b481d625dd7df1"),
        ("3.10.0", "3aa9dc5a5f570320b04b35ee129ce9ff21062d2770df934c6c307913f975e93d"),
        ("3.9.0", "286ff64304905384ce524cd8794c28aee216befd6c9267d4187a12e5a21e2daf"),
        ("3.8.0", "7f75dd1abf3d771d554b0e7b0a7d915ab5f11a74962c92b013ee044a23c1270a"),
        ("3.7.0", "283e1dfe4c3d2e8af4d677ed3c20e975393cdb0856e3ccd77b9c7ed2a151650b"),
    ]:
        resource(
            name="opencl-on-vdi",
            url="https://github.com/ROCm/ROCm-OpenCL-Runtime/archive/rocm-{0}.tar.gz".format(
                d_version
            ),
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="opencl-on-vdi",
            when="@{0}".format(d_version),
        )

    resource(
        name="opencl-on-vdi",
        git="https://github.com/ROCm/ROCm-OpenCL-Runtime.git",
        destination="",
        placement="opencl-on-vdi",
        branch="main",
        when="@master",
    )

    @run_after("install")
    def deploy_missing_files(self):
        if "@3.5.0" in self.spec:
            # the amdrocclr_staticTargets.cmake file is generated but not
            # installed and when we install it by hand, we have to fix the
            # path to the static library libamdrocclr_static.a from build
            # dir to prefix lib dir.
            cmakefile = join_path(self.build_directory, "amdrocclr_staticTargets.cmake")
            filter_file(self.build_directory, self.prefix.lib, cmakefile)
            install(cmakefile, self.prefix.lib)
        elif self.spec.satisfies("@3.7.0:4.3.2"):
            path = join_path(self.prefix.lib, "cmake/rocclr/ROCclrConfig.cmake")
            filter_file(self.build_directory, self.prefix, path)

    def cmake_args(self):
        args = [
            self.define("USE_COMGR_LIBRARY", "yes"),
            self.define("OPENCL_DIR", join_path(self.stage.source_path, "opencl-on-vdi")),
        ]
        return args

    def __init__(self, spec):
        super().__init__(spec)
        if self.spec.satisfies("@4.5.0:"):
            self.phases = ["cmake", "build"]
