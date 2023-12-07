# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.hooks.sbang import filter_shebang
from spack.package import *
from spack.util.prefix import Prefix


class Hip(CMakePackage):
    """HIP is a C++ Runtime API and Kernel Language that allows developers to
    create portable applications for AMD and NVIDIA GPUs from
    single source code."""

    homepage = "https://github.com/ROCm-Developer-Tools/HIP"
    git = "https://github.com/ROCm-Developer-Tools/HIP.git"
    url = "https://github.com/ROCm-Developer-Tools/HIP/archive/rocm-5.5.0.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "haampie")
    libraries = ["libamdhip64"]

    version("master", branch="master")
    version("5.6.1", sha256="4b3c4dfcf8595da0e1b8c3e8067b1ccebeaac337762ff098db14375fa8dd4487")
    version("5.6.0", sha256="a8237768c1ae70029d972376f8d279f4de18a1e6106fff6215d1e16847bc375e")
    version("5.5.1", sha256="1f5f6bb72d8d64335ccc8242ef2e2ea8efeb380cce2997f475b1ee77528d9fb4")
    version("5.5.0", sha256="5b0d0253e62f85cc21d043513f7c11c64e4a4ec416159668f0b160d732d09a3c")
    version("5.4.3", sha256="23e51d3af517cd63019f8d199e46b84d5a18251d148e727f3985e8d99ccb0e58")
    version("5.4.0", sha256="e290f835d69ef23e8b5833a7e616b0a989ff89ada4412d9742430819546efc6c")
    version("5.3.3", sha256="51d4049dc37d261afb9e1270e60e112708ff06b470721ff21023e16e040e4403")
    version("5.3.0", sha256="05225832fb5a4d24f49a773ac27e315239943a6f24291a50d184e2913f2cdbe0")
    version("5.2.3", sha256="5b83d1513ea4003bfad5fe8fa741434104e3e49a87e1d7fad49e5a8c1d06e57b")
    version("5.2.1", sha256="7d4686a2f8a9124bb21f7f3958e451c57019f48a0cbb42ffdc56ed02860a46c3")
    version("5.2.0", sha256="a6e0515d4d25865c037b546035df9c51f0882cd2700e759c266ff7e199f37c3a")
    version("5.1.3", sha256="ce755ee6e407904eba3f6b3c9efcdd48eb4f58a26b06e1892166d05f19a75973")
    version("5.1.0", sha256="47e542183699f4005c48631d96f6a1fbdf27e07ad3402ccd7b5f707c2c602266")
    version(
        "5.0.2",
        sha256="e23601e6f4f62083899ea6356fffbe88d1deb20fa61f2c970e3c0474cd8886ca",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="ae12fcda2d955f04a51c9e794bdb0fa96539cda88b6de8e377850e68e7c2a781",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="c2113dc3c421b8084cd507d91b6fbc0170765a464b71fb0d96bb875df368f160",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="4026f31fb4f8050e9aa9d4294f29c3410bfb38422dbbae4236ccd65fed4d55b2",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="955311193819f487f9a2d64bffe07c4b8c3a0dc644dc3ad984f7c66a325bdd6f",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="293b5025b5e153f2f25e465a2e0006a2b4606db7b7ec2ae449f8a4c0b52d491b",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="ecb929e0fc2eaaf7bbd16a1446a876a15baf72419c723734f456ee62e70b4c24",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="e21c10b62868ece7aa3c8413ec0921245612d16d86d81fe61797bf9a64bc37eb",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="d7b78d96cec67c55b74ea3811ce861b16d300410bc687d0629e82392e8d7c857",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="0082c402f890391023acdfd546760f41cb276dffc0ffeddc325999fd2331d4e8",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="25ad58691456de7fd9e985629d0ed775ba36a2a0e0b21c086bd96ba2fb0f7ed1",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="6450baffe9606b358a4473d5f3e57477ca67cff5843a84ee644bcf685e75d839",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="757b392c3beb29beea27640832fbad86681dbd585284c19a4c2053891673babd",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="ae8384362986b392288181bcfbe5e3a0ec91af4320c189bd83c844ed384161b3",
        deprecated=True,
    )

    variant("rocm", default=True, description="Enable ROCm support")
    variant("cuda", default=False, description="Build with CUDA")
    conflicts("+cuda +rocm", msg="CUDA and ROCm support are mutually exclusive")
    conflicts("~cuda ~rocm", msg="CUDA or ROCm support is required")

    depends_on("cuda", when="+cuda")

    depends_on("cmake@3.16.8:", type=("build"), when="@4.5.0:")
    depends_on("cmake@3.4.3:", type="build")
    depends_on("perl@5.10:", type=("build", "run"))

    test_requires_compiler = True

    with when("+rocm"):
        depends_on("gl@4.5:")
        depends_on("py-cppheaderparser", type="build", when="@5.3.3:")
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
        ]:
            depends_on("hip-rocclr@" + ver, when="@" + ver)
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
            depends_on("hsakmt-roct@" + ver, when="@" + ver)
            depends_on("hsa-rocr-dev@" + ver, when="@" + ver)
            depends_on("comgr@" + ver, when="@" + ver)
            depends_on("llvm-amdgpu@{0} +rocm-device-libs".format(ver), when="@" + ver)
            depends_on("rocminfo@" + ver, when="@" + ver)
            depends_on("roctracer-dev-api@" + ver, when="@" + ver)

        for ver in ["5.4.0", "5.4.3", "5.5.0", "5.5.1", "5.6.0", "5.6.1"]:
            depends_on("hipify-clang", when="@" + ver)

        for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1"]:
            depends_on("rocm-core@" + ver, when="@" + ver)
        # hipcc likes to add `-lnuma` by default :(
        # ref https://github.com/ROCm-Developer-Tools/HIP/pull/2202
        depends_on("numactl", when="@3.7.0:")

    # roc-obj-ls requirements
    depends_on("perl-file-which")
    depends_on("perl-uri-encode")

    # Add hip-amd sources thru the below
    for d_version, d_shasum in [
        ("5.5.1", "9c8cb7611b3a496a0e9db92269143ee33b608eb69a8384957ace04e135ac90e9"),
        ("5.5.0", "bf87ed3919987c1a3a3f293418d26b65b3f02b97464e48f0cfcdd8f35763a0b7"),
        ("5.4.3", "475edce0f29c4ccd82e5ee21d4cce4836f2b1e3b13cbc891475e423d38a0ebb9"),
        ("5.4.0", "c4b79738eb6e669160382b6c47d738ac59bd493fc681ca400ff012a2e8212955"),
        ("5.3.3", "36acce92af39b0fa06002e164f5a7f5a9c7daa19bf96645361325775a325499d"),
        ("5.3.0", "81e9bd5209a7b400c986f9bf1d7079bcf7169bbcb06fc4fe843644559a4d612e"),
        ("5.2.3", "5031d07554ce07620e24e44d482cbc269fa972e3e35377e935d2694061ff7c04"),
        ("5.2.1", "4feaa3883cbc54ddcd5d2d5becbe0f3fe3edd5b3b468dc73b5104893029eefac"),
        ("5.2.0", "8774958bebc29a4b7eb9dc2d38808d79d9a24bf9c1f44e801ff99d2d5ba82240"),
        ("5.1.3", "707f2217f0e7aeb62d7b76830a271056d665542bf5f7a54e40adf4d5f299ca93"),
        ("5.1.0", "77984854bfe00f938353fe4c7604d09967eaf5c609d05f1e6423d3c3dea86e61"),
        ("5.0.2", "80e7268dd22eba0f2f9222932480dede1d80e56227c0168c6a0cc8e4f23d3b76"),
        ("5.0.0", "cbd95a577abfd7cbffee14a4848f7789a417c6e5e5a713f42eb75d7948abcdf9"),
        ("4.5.2", "b6f35b1a1d0c466b5af28e26baf646ae63267eccc4852204db1e0c7222a39ce2"),
        ("4.5.0", "7b93ab64d6894ff9b5ba0be35e3ed8501d6b18a2a14223d6311d72ab8a9cdba6"),
    ]:
        resource(
            name="hipamd",
            url="https://github.com/ROCm-Developer-Tools/hipamd/archive/rocm-{0}.tar.gz".format(
                d_version
            ),
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="hipamd",
            when="@{0}".format(d_version),
        )
    # Add opencl sources thru the below
    for d_version, d_shasum in [
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
    ]:
        resource(
            name="opencl",
            url="https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/rocm-{0}.tar.gz".format(
                d_version
            ),
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="opencl",
            when="@{0}".format(d_version),
        )
    for d_version, d_shasum in [
        ("5.5.1", "1375fc7723cfaa0ae22a78682186d4804188b0a54990bfd9c0b8eb421b85e37e"),
        ("5.5.0", "efbae9a1ef2ab3de5ca44091e9bb78522e76759c43524c1349114f9596cc61d1"),
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
    # Add hip-clr sources thru the below
    for d_version, d_shasum in [
        ("5.6.1", "0b88af1e99643899d11b1c8cf8a3c46601051b328a5e0ffbd44ee88b7eb0db33"),
        ("5.6.0", "8dcd99110737a294f67a805639cf372890c8ca16c7603caaa793e71e84478fe4"),
    ]:
        resource(
            name="clr",
            url="https://github.com/ROCm-Developer-Tools/clr/archive/refs/tags/rocm-{0}.tar.gz".format(
                d_version
            ),
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="clr",
            when="@{0}".format(d_version),
        )

    # Add hipcc sources thru the below
    for d_version, d_shasum in [
        ("5.6.1", "5800fac92b841ef6f52acda78d9bf86f83970bec0fb848a6265d239bdb7eb51a"),
        ("5.6.0", "fdb7fdc9e4648376120330f034ee8353038d34c8a015f9eb0c208c56eeddd097"),
    ]:
        resource(
            name="hipcc",
            url="https://github.com/ROCm-Developer-Tools/HIPCC/archive/refs/tags/rocm-{0}.tar.gz".format(
                d_version
            ),
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="hipcc",
            when="@{0}".format(d_version),
        )
    # Add hiptests sources thru the below
    for d_version, d_shasum in [
        ("5.6.1", "5b3002ddfafda162329e4d9e6ac1200eeb48ff08e666b342aa8aeca30750f48b"),
        ("5.6.0", "8cf4509bf9c0747dab8ed8fec1365a9156792034b517207a0b2d63270429fd2e"),
    ]:
        resource(
            name="hip-tests",
            url="https://github.com/ROCm-Developer-Tools/hip-tests/archive/refs/tags/rocm-{0}.tar.gz".format(
                d_version
            ),
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="hip-tests",
            when="@{0}".format(d_version),
        )
    # Note: the ROCm ecosystem expects `lib/` and `bin/` folders with symlinks
    # in the parent directory of the package, which is incompatible with spack.
    # In hipcc the ROCM_PATH variable is used to point to the parent directory
    # of the package. With the following patch we should never hit code that
    # uses the ROCM_PATH variable again; just to be sure we set it to an empty
    # string.
    patch("0001-Make-it-possible-to-specify-the-package-folder-of-ro.patch", when="@3.5.0:4.5.3")
    patch(
        "0010-Improve-compilation-without-git-repo-and-remove-compiler-rt-linkage-for-host"
        ".5.0.0.patch",
        when="@5.0.0",
    )
    patch(
        "0011-Improve-compilation-without-git-repo-and-remove-compiler-rt-linkage-for-host"
        ".5.0.2.patch",
        when="@5.0.2:5.1.3",
    )

    # Improve compilation without git repo and remove compiler rt linkage
    # for host and correction in CMake target path variable and
    # correcting the CMake path variable.
    patch(
        "0012-Improve-compilation-without-git-repo-and-remove-compiler-rt-linkage-for-host"
        ".5.2.0.patch",
        when="@5.2.0",
    )
    patch(
        "0012-Improve-compilation-without-git-repo-and-remove-compiler-rt-linkage-for-host"
        ".5.2.1.patch",
        when="@5.2.1:5.2.3",
    )
    patch("0013-remove-compiler-rt-linkage-for-host.5.3.0.patch", when="@5.3.0:5.4")

    # See https://github.com/ROCm-Developer-Tools/HIP/pull/2141
    patch("0002-Fix-detection-of-HIP_CLANG_ROOT.patch", when="@:3.9.0")

    # See https://github.com/ROCm-Developer-Tools/HIP/pull/2218
    patch("0003-Improve-compilation-without-git-repo.3.7.0.patch", when="@3.7.0:3.9.0")
    patch("0003-Improve-compilation-without-git-repo.3.10.0.patch", when="@3.10.0:4.0.0")
    patch("0003-Improve-compilation-without-git-repo.4.1.0.patch", when="@4.1.0")
    patch(
        "0003-Improve-compilation-without-git-repo-and-remove-compiler-rt-linkage-for-host"
        ".4.2.0.patch",
        when="@4.2.0:4.3.2",
    )
    patch(
        "0009-Improve-compilation-without-git-repo-and-remove-compiler-rt-linkage-for-host"
        "_disabletests.4.5.0.patch",
        when="@4.5.0:4.5.3",
    )
    # See https://github.com/ROCm-Developer-Tools/HIP/pull/2219
    patch("0004-Drop-clang-rt-builtins-linking-on-hip-host.3.7.0.patch", when="@3.7.0:3.9.0")
    patch("0004-Drop-clang-rt-builtins-linking-on-hip-host.3.10.0.patch", when="@3.10.0:4.1.0")

    # Tests are broken when using cmake 3.21
    with when("^cmake@3.21.0:"):
        patch("0005-Disable-tests-3.5.0.patch", when="@3.5.0")
        patch("0005-Disable-tests-3.6.0.patch", when="@3.6.0:3.8.0")
        patch("0005-Disable-tests-3.9.0.patch", when="@3.9.0:4.0.0")
        patch("0005-Disable-tests-4.1.0.patch", when="@4.1.0:4.3.2")

    patch("Add_missing_open_cl_header_file_for_4.3.0.patch", when="@4.3.0:4.3.2")
    patch("0014-hip-test-file-reorg-5.4.0.patch", when="@5.4.0:5.5")
    patch("0016-hip-sample-fix-hipMalloc-call.patch", when="@5.4.3:5.5")
    patch("0014-remove-compiler-rt-linkage-for-host.5.5.0.patch", when="@5.5")
    patch("0014-remove-compiler-rt-linkage-for-host.5.6.0.patch", when="@5.6:")
    patch("0015-reverting-operator-mixup-fix-for-slate.patch", when="@5.6:")
    # See https://github.com/ROCm-Developer-Tools/HIP/pull/3206
    patch(
        "https://github.com/ROCm-Developer-Tools/HIP/commit/50ee82f6bc4aad10908ce09198c9f7ebfb2a3561.patch?full_index=1",
        sha256="c2ee21cdc55262c7c6ba65546b5ca5f65ea89730",
        when="@5.2:",
    )

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("@:4.3.2"):
            return self.stage.source_path
        elif self.spec.satisfies("@4.5:5.5"):
            return "hipamd"
        else:
            return "clr"

    def get_paths(self):
        if self.spec.external:
            # For external packages we only assume the `hip` prefix is known,
            # because spack does not set prefixes of dependencies of externals.
            hip_libs_at_top = os.path.basename(self.spec.prefix) != "hip"
            # We assume self.spec.prefix is  /opt/rocm-x.y.z for rocm-5.2.0 and newer
            # and /opt/rocm-x.y.z/hip for older versions
            # However, depending on how an external is found it can be at either level
            # of the installation path
            if self.spec.satisfies("@5.2.0:"):
                if hip_libs_at_top:
                    rocm_prefix = Prefix(self.spec.prefix)
                else:
                    rocm_prefix = Prefix(os.path.dirname(self.spec.prefix))
            else:
                # We assume self.spec.prefix is /opt/rocm-x.y.z/hip and rocm has a
                # default installation with everything installed under
                # /opt/rocm-x.y.z
                # Note that since the key hip library can also exist at the top of the
                # /opt/rocm-x.y.z/lib tree, it is possible that the package is detected
                # without the correct prefix.  Work around it.
                if hip_libs_at_top:
                    rocm_prefix = Prefix(self.spec.prefix)
                else:
                    rocm_prefix = Prefix(os.path.dirname(self.spec.prefix))

            if not os.path.isdir(rocm_prefix):
                msg = "Could not determine prefix for other rocm components\n"
                msg += "Either report a bug at github.com/spack/spack or "
                msg += "manually edit rocm_prefix in the package file as "
                msg += "a workaround."
                raise RuntimeError(msg)

            if hip_libs_at_top:
                hip_path = "{0}/hip".format(self.spec.prefix)
            else:
                hip_path = self.spec.prefix

            paths = {
                "hip-path": hip_path,
                "rocm-path": rocm_prefix,
                "llvm-amdgpu": rocm_prefix.llvm,
                "hsa-rocr-dev": rocm_prefix.hsa,
                "rocminfo": rocm_prefix,
                "comgr": rocm_prefix,
                "rocm-device-libs": rocm_prefix,
            }

            if self.spec.satisfies("@5.4:"):
                paths["hipify-clang"] = rocm_prefix
        else:
            paths = {
                "hip-path": self.spec.prefix,
                "rocm-path": self.spec.prefix,
                "llvm-amdgpu": self.spec["llvm-amdgpu"].prefix,
                "hsa-rocr-dev": self.spec["hsa-rocr-dev"].prefix,
                "rocminfo": self.spec["rocminfo"].prefix,
                "comgr": self.spec["comgr"].prefix,
                "rocm-device-libs": self.spec["llvm-amdgpu"].prefix,
            }

            if self.spec.satisfies("@5.4:"):
                paths["hipify-clang"] = self.spec["hipify-clang"].prefix

        if "@:3.8.0" in self.spec:
            paths["bitcode"] = paths["rocm-device-libs"].lib
        else:
            paths["bitcode"] = paths["rocm-device-libs"].amdgcn.bitcode

        return paths

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

    def set_variables(self, env):
        if self.spec.satisfies("+rocm"):
            # Note: do not use self.spec[name] here, since not all dependencies
            # have defined prefixes when hip is marked as external.
            paths = self.get_paths()

            # Used in hipcc, but only useful when hip is external, since only then
            # there is a common prefix /opt/rocm-x.y.z.
            env.set("ROCM_PATH", paths["rocm-path"])
            if self.spec.satisfies("@5.4:"):
                env.set("HIPIFY_CLANG_PATH", paths["hipify-clang"])

            # hipcc recognizes HIP_PLATFORM == hcc and HIP_COMPILER == clang, even
            # though below we specified HIP_PLATFORM=rocclr and HIP_COMPILER=clang
            # in the CMake args.
            if self.spec.satisfies("@:4.0.0"):
                env.set("HIP_PLATFORM", "hcc")
            else:
                env.set("HIP_PLATFORM", "amd")

            env.set("HIP_COMPILER", "clang")

            # bin directory where clang++ resides
            env.set("HIP_CLANG_PATH", paths["llvm-amdgpu"].bin)

            # Path to hsa-rocr-dev prefix used by hipcc.
            env.set("HSA_PATH", paths["hsa-rocr-dev"])

            # This is a variable that does not exist in hipcc but was introduced
            # in a patch of ours since 3.5.0 to locate rocm_agent_enumerator:
            # https://github.com/ROCm-Developer-Tools/HIP/pull/2138
            env.set("ROCMINFO_PATH", paths["rocminfo"])

            # This one is used in hipcc to run `clang --hip-device-lib-path=...`
            env.set("DEVICE_LIB_PATH", paths["bitcode"])

            # And this is used in clang whenever the --hip-device-lib-path is not
            # used (e.g. when clang is invoked directly)
            env.set("HIP_DEVICE_LIB_PATH", paths["bitcode"])

            # Just the prefix of hip (used in hipcc)
            env.set("HIP_PATH", paths["hip-path"])

            # Used in comgr and seems necessary when using the JIT compiler, e.g.
            # hiprtcCreateProgram:
            # https://github.com/RadeonOpenCompute/ROCm-CompilerSupport/blob/rocm-4.0.0/lib/comgr/src/comgr-env.cpp
            env.set("LLVM_PATH", paths["llvm-amdgpu"])
            env.set("COMGR_PATH", paths["comgr"])

            # Finally we have to set --rocm-path=<prefix> ourselves, which is not
            # the same as --hip-device-lib-path (set by hipcc). It's used to set
            # default bin, include and lib folders in clang. If it's not set it is
            # infered from the clang install dir (and they try to find
            # /opt/rocm again...). If this path is set, there is no strict checking
            # and parsing of the <prefix>/bin/.hipVersion file. Let's just set this
            # to the hip prefix directory for non-external builds so that the
            # bin/.hipVersion file can still be parsed.
            # See also https://github.com/ROCm-Developer-Tools/HIP/issues/2223
            if "@3.8.0:" in self.spec:
                env.append_path(
                    "HIPCC_COMPILE_FLAGS_APPEND",
                    "--rocm-path={0}".format(paths["rocm-path"]),
                    separator=" ",
                )
        elif self.spec.satisfies("+cuda"):
            env.set("CUDA_PATH", self.spec["cuda"].prefix)
            env.set("HIP_PATH", self.spec.prefix)
            env.set("HIP_PLATFORM", "nvidia")

    def setup_build_environment(self, env):
        self.set_variables(env)

    def setup_run_environment(self, env):
        self.set_variables(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.set_variables(env)

        if "amdgpu_target" in dependent_spec.variants:
            arch = dependent_spec.variants["amdgpu_target"]
            if "none" not in arch and "auto" not in arch:
                env.set("HCC_AMDGPU_TARGET", ",".join(arch.value))

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_dependent_build_environment(env, dependent_spec)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.hipcc = join_path(self.prefix.bin, "hipcc")

    def patch(self):
        if self.spec.satisfies("@:4.3.2"):
            filter_file(
                'INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/../include"',
                'INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"',
                "hip-config.cmake.in",
                string=True,
            )
        if self.spec.satisfies("@5.2:5.4 +rocm"):
            filter_file(
                '"${ROCM_PATH}/llvm"',
                self.spec["llvm-amdgpu"].prefix,
                "hipamd/hip-config.cmake.in",
                string=True,
            )
        if self.spec.satisfies("@5.6: +rocm"):
            filter_file(
                '"${ROCM_PATH}/llvm"',
                self.spec["llvm-amdgpu"].prefix,
                "clr/hipamd/hip-config.cmake.in",
                string=True,
            )

        perl = self.spec["perl"].command
        kwargs = {"ignore_absent": False, "backup": False, "string": False}

        with working_dir("bin"):
            match = "^#!/usr/bin/perl"
            substitute = "#!{perl}".format(perl=perl)

            if self.spec.satisfies("@:4.0.0"):
                files = ["hipify-perl", "hipcc", "extractkernel", "hipconfig", "hipify-cmakefile"]
            elif self.spec.satisfies("@4.0.0:4.3.2"):
                files = [
                    "hipify-perl",
                    "hipcc",
                    "roc-obj-extract",
                    "hipconfig",
                    "hipify-cmakefile",
                    "roc-obj-ls",
                    "hipvars.pm",
                ]
            elif self.spec.satisfies("@4.5.0:5.5"):
                files = []
                filter_file(match, substitute, *files, **kwargs)
                # This guy is used during the cmake phase, so we have to fix the
                # shebang already here in case it is too long.
                filter_shebang("hipconfig")
        if self.spec.satisfies("@4.5.0:5.5"):
            perl = self.spec["perl"].command
            kwargs = {"ignore_absent": False, "backup": False, "string": False}
            with working_dir("hipamd/bin"):
                match = "^#!/usr/bin/perl"
                substitute = "#!{perl}".format(perl=perl)
                files = ["roc-obj-extract", "roc-obj-ls"]
                filter_file(match, substitute, *files, **kwargs)
        if self.spec.satisfies("@5.6.0:"):
            perl = self.spec["perl"].command
            kwargs = {"ignore_absent": False, "backup": False, "string": False}
            match = "^#!/usr/bin/perl"
            substitute = "#!{perl}".format(perl=perl)
            with working_dir("clr/hipamd/bin"):
                files = ["roc-obj-extract", "roc-obj-ls"]
                filter_file(match, substitute, *files, **kwargs)
            with working_dir("hipcc/bin"):
                files = []
                filter_file(match, substitute, *files, **kwargs)
                filter_shebang("hipconfig")
        if "@3.7.0: +rocm" in self.spec:
            numactl = self.spec["numactl"].prefix.lib
            kwargs = {"ignore_absent": False, "backup": False, "string": False}

            with working_dir("bin"):
                match = " -lnuma"
                substitute = " -L{numactl} -lnuma".format(numactl=numactl)
                if self.spec.satisfies("@4.5.0:5.5"):
                    filter_file(match, substitute, "hipcc", **kwargs)
        if "@5.6.0: +rocm" in self.spec:
            numactl = self.spec["numactl"].prefix.lib
            kwargs = {"ignore_absent": False, "backup": False, "string": False}

            with working_dir("hipcc/src"):
                match = " -lnuma"
                substitute = " -L{numactl} -lnuma".format(numactl=numactl)
                filter_file(match, substitute, "hipBin_amd.h", **kwargs)

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.satisfies("@3.7.0:4.3.2"):
            incl = self.spec["hip-rocclr"].prefix.include
            flags.append("-I {0}/compiler/lib/include".format(incl))
            flags.append("-I {0}/elf".format(incl))

        return (flags, None, None)

    def cmake_args(self):
        args = []
        if self.spec.satisfies("+rocm"):
            args.append(self.define("HSA_PATH", self.spec["hsa-rocr-dev"].prefix))
            args.append(self.define("HIP_COMPILER", "clang"))
            args.append(
                self.define(
                    "PROF_API_HEADER_PATH",
                    self.spec["roctracer-dev-api"].prefix.roctracer.include.ext,
                )
            )
            if self.spec.satisfies("@:4.0.0"):
                args.append(self.define("HIP_RUNTIME", "ROCclr"))
                args.append(self.define("HIP_PLATFORM", "rocclr"))
            else:
                args.append(self.define("HIP_RUNTIME", "rocclr"))
                args.append(self.define("HIP_PLATFORM", "amd"))
        if self.spec.satisfies("+cuda"):
            args.append(self.define("HIP_PLATFORM", "nvidia"))

        # LIBROCclr_STATIC_DIR is unused from 3.6.0 and above
        if "@3.5.0:4.3.2" in self.spec:
            args.append(self.define("LIBROCclr_STATIC_DIR", self.spec["hip-rocclr"].prefix.lib))
        if "@4.5.0:" in self.spec:
            args.append(self.define("HIP_COMMON_DIR", self.stage.source_path))
            args.append(self.define("HIP_CATCH_TEST", "OFF"))
        if "@4.5.0:5.5" in self.spec:
            args.append(self.define("ROCCLR_PATH", self.stage.source_path + "rocclr"))
            args.append(self.define("AMD_OPENCL_PATH", self.stage.source_path + "opencl"))
        if "@5.3.0:" in self.spec:
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        if "@5.6.0:" in self.spec:
            args.append(self.define("ROCCLR_PATH", self.stage.source_path + "/clr/rocclr"))
            args.append(self.define("AMD_OPENCL_PATH", self.stage.source_path + "/clr/opencl"))
            args.append(self.define("HIPCC_BIN_DIR", self.stage.source_path + "/hipcc/bin")),
            args.append(self.define("CLR_BUILD_HIP", True)),
            args.append(self.define("CLR_BUILD_OCL", False)),
        return args

    test_src_dir_old = "samples"
    test_src_dir = "hip-tests/samples"

    @run_after("install")
    def install_samples(self):
        if self.spec.satisfies("@5.6.0:"):
            install_tree(self.test_src_dir, self.spec.prefix.share.samples)

    @run_after("install")
    def cache_test_sources(self):
        """Copy the tests source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        if self.spec.satisfies("@:5.1.0"):
            return
        elif self.spec.satisfies("@5.1:5.5"):
            self.cache_extra_test_sources([self.test_src_dir_old])
        elif self.spec.satisfies("@5.6:"):
            self.cache_extra_test_sources([self.test_src_dir])

    def test_samples(self):
        # configure, build and run all hip samples
        if self.spec.satisfies("@:5.1.0"):
            raise SkipTest("Test is only available for specs after version 5.1.0")
        elif self.spec.satisfies("@5.1:5.5"):
            test_dir = join_path(self.test_suite.current_test_cache_dir, self.test_src_dir_old)
        elif self.spec.satisfies("@5.6:"):
            test_dir = join_path(self.test_suite.current_test_cache_dir, self.test_src_dir)
        prefixes = ";".join(
            [
                self.spec["hip"].prefix,
                self.spec["llvm-amdgpu"].prefix,
                self.spec["comgr"].prefix,
                self.spec["hsa-rocr-dev"].prefix,
            ]
        )
        cc_options = ["-DCMAKE_PREFIX_PATH=" + prefixes, ".."]

        amdclang_path = join_path(self.spec["llvm-amdgpu"].prefix, "bin", "amdclang++")
        os.environ["CXX"] = amdclang_path
        os.environ["FC"] = "/usr/bin/gfortran"

        cmake = which(self.spec["cmake"].prefix.bin.cmake)

        for root, dirs, files in os.walk(test_dir):
            dirs.sort()
            if "CMakeLists.txt" in files or "Makefile" in files:
                with working_dir(root, create=True):
                    head, test_name = os.path.split(root)
                    with test_part(
                        self,
                        "test_sample_{0}".format(test_name),
                        purpose="configure, build and run test: {0}".format(test_name),
                    ):
                        if "CMakeLists.txt" in files:
                            print("Configuring  test " + test_name)
                            os.mkdir("build")
                            os.chdir("build")
                            cmake(*cc_options)

                        print("Building test " + test_name)
                        make(parallel=False)
                        # iterate through the files in dir to find the newly built binary
                        for file in os.listdir("."):
                            if (
                                file not in files
                                and os.path.isfile(file)
                                and os.access(file, os.X_OK)
                                and not file.endswith(".o")
                            ):
                                print("Executing test binary: " + file)
                                exe = which(file)
                                if file == "hipDispatchEnqueueRateMT":
                                    options = ["16", "0"]
                                else:
                                    options = []
                                exe(*options)
