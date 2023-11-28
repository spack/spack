# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Rocsparse(CMakePackage):
    """rocSPARSE exposes a common interface that provides
    Basic Linear Algebra Subroutines for sparse computation
    implemented on top of AMD's Radeon Open eCosystem Platform ROCm runtime
    and toolchains. rocSPARSE is created using the HIP programming
    language and optimized for AMD's latest discrete GPUs."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocSPARSE"
    git = "https://github.com/ROCmSoftwarePlatform/rocSPARSE.git"
    url = "https://github.com/ROCmSoftwarePlatform/rocSPARSE/archive/rocm-5.5.0.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath")
    libraries = ["librocsparse"]

    amdgpu_targets = ROCmPackage.amdgpu_targets

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )
    variant("test", default=False, description="Build rocsparse-test client")

    version("5.6.1", sha256="6a50a64354507f1374e1a86aa7f5c07d1aaa96ac193ac292c279153087bb5d54")
    version("5.6.0", sha256="5797db3deb4a532e691447e3e8c923b93bd9fe4c468f3a88f00cecd80bebcae4")
    version("5.5.1", sha256="1dd2d18898dfebdf898e8fe7d1c1198e8f8451fd70ff12a1990ec1419cf359e1")
    version("5.5.0", sha256="cbee79b637691bc710c1c83fbaa91db7498d38d4df873be23e28ed5617acde72")
    version("5.4.3", sha256="9fb633f235eb0567cc54fae6bdc779f16bf0bb4e6f5bdddb40312c6d11ca8478")
    version("5.4.0", sha256="c8f0e920a8ec15b9ae40564c68191363356cc4d793c16247bb6e11ef5293ed11")
    version("5.3.3", sha256="4204035e952e20ada4526a94989e8e5c76c04574176fe63a021522862461c800")
    version("5.3.0", sha256="521ca0e7b52f26edbff8507eb1479dc26019f456756d884d7b8b192c3ea518e8")
    version("5.2.3", sha256="6da3f3303a8ada94c4dbff4b42ee33a2e2883a908ee21c41cb2aa7180382026a")
    version("5.2.1", sha256="01f3535442740221edad2cde0a20b2499c807f6733d5016b33c47f34a5a55c49")
    version("5.2.0", sha256="7ed929af16d2502135024a6463997d9a95f03899b8a33aa95db7029575c89572")
    version("5.1.3", sha256="ef9641045b36c9aacc87e4fe7717b41b1e29d97e21432678dce7aca633a8edc2")
    version("5.1.0", sha256="a2f0f8cb02b95993480bd7264fc65e8b11464a90b86f2dcd0dd82a2e6d4bd704")
    version(
        "5.0.2",
        sha256="c9d9e1b7859e1c5aa5050f5dfdf86245cbd7c1296c0ce60d9ca5f3e22a9b748b",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="6d352bf27dbed08e5115a58815aa76c59eb2008ec9dcc921aadf2efe20115d2a",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="e37af2cd097e239a55a278df534183b5591ef4d985fe1a268a229bd11ada6599",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="b120e9e17e7e141caee4c8c4288c9d1902bad0cec2ea76458d3ba11343376938",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="fa5ea64f71e1cfbebe41618cc183f501b387824a6dc58486ab1214d7af5cbef2",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="1a8109bdc8863b3acfe991449360c9361cae7cabdbe753c553bc57872cd0ad5e",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="8a86ed49d278e234c82e406a1430dc28f50d416f8f1065cf5bdf25cc5721129c",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="7514968ed2342dc274acce8b269c128a6aa96cce769a37fd3880b5269c2ed17f",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="2b41bc6623d204ad7f351a902810f34cd32b762d1bf59081dbb00f83e689a794",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="8325828c5d7818dfb45e03b5f1572a573cc21964d596aaaa33b7469817b03abd",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="7b8f952d0c7f8ac2f3bb60879ab420fabbfafb0885a3d8464d5b4c191e97dec6",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="a5d085fffe05a7ac7f5658075d9782b9b02d0c5c3e2c1807dad266c3a61141fd",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="db561ae5e8ee117f7c539a9ef6ee49c13b82ba9f702b22c76e741cca245386a9",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="9ca6bae7da78abbb47143c3d77ff4a8cd7d63979875fc7ebc46b400769fd9cb5",
        deprecated=True,
    )

    depends_on("cmake@3.5:", type="build")

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
    ]:
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("rocprim@" + ver, when="@" + ver)
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)

    # Add option so Spack can manage downloaded test matricies as resources.
    patch("0001-set-mtx-directory.patch", when="@4.5.0:5.3 +test")
    # Enable use of Spack-provided Python.
    patch("0002-fix-gentest-shebang.patch", when="@4.5.0:5.3 +test")
    # Fix build for most Radeon 5000 and Radeon 6000 series GPUs.
    patch("0003-fix-navi-1x-rocm-4.5.patch", when="@4.5.0:5.1")
    patch("0003-fix-navi-1x-rocm-5.2.patch", when="@5.2")

    depends_on("googletest@1.11.0:", when="@5.1.0: +test")
    depends_on("googletest@1.10.0:", when="+test")
    depends_on("python@3:", type="build", when="+test")
    depends_on("py-pyyaml", type="build", when="+test")

    with when("+test"):
        resource(
            name="amazon0312",
            url="https://sparse.tamu.edu/MM/SNAP/amazon0312.tar.gz",
            sha256="75ffd36b33675856f370f508d53e6197caa972ac52929991db7dc4198bd64910",
            destination="mtx",
        )
        resource(
            name="Chebyshev4",
            url="https://sparse.tamu.edu/MM/Muite/Chebyshev4.tar.gz",
            sha256="82553d73281587ea70e5faa427910e979524412c89e59ada7fa47a97142ae8a6",
            destination="mtx",
        )
        resource(
            name="sme3Dc",
            url="https://sparse.tamu.edu/MM/FEMLAB/sme3Dc.tar.gz",
            sha256="82f03904849cceea0af1b9975942717527ecc5e87a98cfddea78ffbe7e7c076d",
            destination="mtx",
        )
        resource(
            name="webbase-1M",
            url="https://sparse.tamu.edu/MM/Williams/webbase-1M.tar.gz",
            sha256="17a0391cdd966350b2b41f32aaf8e6684f3c55f25eb68c4be088f44f728a3ed4",
            destination="mtx",
        )
        resource(
            name="rma10",
            url="https://sparse.tamu.edu/MM/Bova/rma10.tar.gz",
            sha256="50db8d278d371531b3dd0638444d47a77f3a3e189663993a857861dbc34c5e3f",
            destination="mtx",
        )
        resource(
            name="bibd_22_8",
            url="https://sparse.tamu.edu/MM/JGD_BIBD/bibd_22_8.tar.gz",
            sha256="534b5210662d1b5b14a3938671501189685d12abf9f2a206778508345181014c",
            destination="mtx",
        )
        resource(
            name="mac_econ_fwd500",
            url="https://sparse.tamu.edu/MM/Williams/mac_econ_fwd500.tar.gz",
            sha256="0dec2952b2908e3d59e4179289245db7f2c84f9e5e6543e818491deed5978f82",
            destination="mtx",
        )
        resource(
            name="mc2depi",
            url="https://sparse.tamu.edu/MM/Williams/mc2depi.tar.gz",
            sha256="c02fef86efdd4f4322487e7472697a3d30b084ede1021e6d6889b347d3f6b268",
            destination="mtx",
        )
        resource(
            name="scircuit",
            url="https://sparse.tamu.edu/MM/Hamm/scircuit.tar.gz",
            sha256="227d4c98e51c8af49c07f89929c62f2523e115e81b672e7f306185ea92c2996f",
            destination="mtx",
        )
        resource(
            name="ASIC_320k",
            url="https://sparse.tamu.edu/MM/Sandia/ASIC_320k.tar.gz",
            sha256="d0d4ac477f641c8372d7347bc262ffcbde017f50fb17bb1a1539c98dd3440145",
            destination="mtx",
        )
        resource(
            name="bmwcra_1",
            url="https://sparse.tamu.edu/MM/GHS_psdef/bmwcra_1.tar.gz",
            sha256="31467b319f3d4e8a8fc3a320344650bee14b285755b13ee29264b7a488b3d222",
            destination="mtx",
        )
        resource(
            name="nos1",
            url="https://sparse.tamu.edu/MM/HB/nos1.tar.gz",
            sha256="7e64dc2408890e85a60dbd2ad048963c74625cc3037dbdff9647d30844a52674",
            destination="mtx",
        )
        resource(
            name="nos2",
            url="https://sparse.tamu.edu/MM/HB/nos2.tar.gz",
            sha256="7439318b969e8cad0e96f154937a35256374bb8f0e16ed7ecc3a5219f8dc903b",
            destination="mtx",
        )
        resource(
            name="nos3",
            url="https://sparse.tamu.edu/MM/HB/nos3.tar.gz",
            sha256="7dd62179bbcaeb693c774712a8d70b97316364983f1cbf06cecb3900da8954a5",
            destination="mtx",
        )
        resource(
            name="nos4",
            url="https://sparse.tamu.edu/MM/HB/nos4.tar.gz",
            sha256="ec2323a5195db153fd6ae32ff537b22eb47f08e73949754b71f8d4104358f10f",
            destination="mtx",
        )
        resource(
            name="nos5",
            url="https://sparse.tamu.edu/MM/HB/nos5.tar.gz",
            sha256="dd67e906b0392cfbbe5a01a1f1a569c50875cbf88249a31721fb87519666a342",
            destination="mtx",
        )
        resource(
            name="nos6",
            url="https://sparse.tamu.edu/MM/HB/nos6.tar.gz",
            sha256="a0301c38ed91b849571303db581205cfae113565a7938eaa1a7466320f0d03c4",
            destination="mtx",
        )
        resource(
            name="nos7",
            url="https://sparse.tamu.edu/MM/HB/nos7.tar.gz",
            sha256="c5d8d99bf4b54ee45e2f45d78530e3787f2e9670c000a68ad986a3b923e9e5ae",
            destination="mtx",
        )
        resource(
            name="shipsec1",
            url="https://sparse.tamu.edu/MM/DNVS/shipsec1.tar.gz",
            sha256="d021889affed5429f85b606900f76870d0b1b1aefd92529cc6f43bf9d7ef0eb1",
            destination="mtx",
        )
        resource(
            name="mplate",
            url="https://sparse.tamu.edu/MM/Cote/mplate.tar.gz",
            sha256="647b848343e423a24e05d3a3d462fa6b77958e362aadf70e9bb51bd420730df2",
            destination="mtx",
        )
        resource(
            name="qc2534",
            url="https://sparse.tamu.edu/MM/Bai/qc2534.tar.gz",
            sha256="591c54ceee70222909353d2a400dd9819e3432143b2c25b6c4ffa262b8e397c8",
            destination="mtx",
        )
        resource(
            name="Chevron2",
            url="https://sparse.tamu.edu/MM/Chevron/Chevron2.tar.gz",
            sha256="9334b61c25958f5221fd114e9698c11ac0ec57a0432150731d3fe80033da3026",
            destination="mtx",
        )
        resource(
            name="Chevron3",
            url="https://sparse.tamu.edu/MM/Chevron/Chevron3.tar.gz",
            sha256="5679292ba86defedb0a6afc25274948521ace7ca90fc765265be11ca6eaaaee4",
            destination="mtx",
        )
        resource(
            name="Chevron4",
            url="https://sparse.tamu.edu/MM/Chevron/Chevron4.tar.gz",
            sha256="2ac9dc0d8d38cbf4a62089c74e53aea87edbb3f0b553b77b27c70df70e1d17d5",
            destination="mtx",
        )

    def check(self):
        if self.spec.satisfies("+test"):
            exe = join_path(self.build_directory, "clients", "staging", "rocsparse-test")
            self.run_test(exe, options=["--gtest_filter=*quick*:*pre_checkin*-*known_bug*"])

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

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
            self.define_from_variant("BUILD_CLIENTS_TESTS", "test"),
            self.define("BUILD_CLIENTS_BENCHMARKS", "OFF"),
            self.define("ROCSPARSE_MTX_DIR", join_path(self.stage.source_path, "mtx")),
        ]

        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        if self.spec.satisfies("@5.3.0:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        return args
