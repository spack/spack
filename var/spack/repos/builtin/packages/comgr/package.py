# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Comgr(CMakePackage):
    """This provides various Lightning Compiler related services. It currently
    contains one library, the Code Object Manager (Comgr)"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport"
    git = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport.git"
    url = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "haampie")
    libraries = ["libamd_comgr"]

    version("master", branch="amd-stg-open")

    version("5.4.3", sha256="8af18035550977fe0aa9cca8dfacbe65fe292e971de5a0e160710bafda05a81f")
    version("5.4.0", sha256="f4b83b27ff6195679d695c3f41fa25456e9c50bae6d978f46d3541b472aef757")
    version("5.3.3", sha256="6a4ef69e672a077b5909977248445f0eedf5e124af9812993a4d444be030c78b")
    version("5.3.0", sha256="072f849d79476d87d31d62b962e368762368d540a9da02ee2675963dc4942b2c")
    version("5.2.3", sha256="36d67dbe791d08ad0a02f0f3aedd46059848a0a232c5f999670103b0410c89dc")
    version("5.2.1", sha256="ebeaea8e653fc2b9d67d3271be44690ac7876ee679baa01d47863e75362b8c85")
    version("5.2.0", sha256="5f63fa93739ee9230756ef93c53019474b6cdddea3b588492d785dae1b08c087")
    version("5.1.3", sha256="3078c10e9a852fe8357712a263ad775b15944e083f93a879935c877511066ac9")
    version("5.1.0", sha256="1cdcfe5acb768ef50fb0026d4ee7ba01e615251ad3c27bb2593cdcf8c070a894")
    version(
        "5.0.2",
        sha256="20d733f70d8edb573d8c92707f663d7d46dcaff08026cd6addbb83266679f92a",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="da1bbc694bd930a504406eb0a0018c2e317d8b2c136fb2cab8de426870efe9a8",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="e45f387fb6635fc1713714d09364204cd28fea97655b313c857beb1f8524e593",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="03c5880e0922fcff31306f7da2eb9d3a3709d9b5b75b3524dcfae85f4b181678",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="f1d99550383ed7b3a01d304eedc3d86a8e45b271aa5a80b1dd099c22fda3f745",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="f77b505abb474078374701dfc49e651ad3eeec5349ce6edda54549943a3775ee",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="40a1ea50d2aea0cf75c4d17cdd6a7fe44ae999bf0147d24a756ca4675ce24e36",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="ffb625978555c63582aa46857672431793261166aa31761eff4fe5c2cab661ae",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="f389601fb70b2d9a60d0e2798919af9ddf7b8376a2e460141507fe50073dfb31",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="b44ee5805a6236213d758fa4b612bb859d8f774b9b4bdc3a2699bb009dd631bc",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="6600e144d72dadb6d893a3388b42af103b9443755ce556f4e9e205ccd8ec0c83",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="62a35480dfabaa98883d91ed0f7c490daa9bbd424af37e07e5d85a6e8030b146",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="73e56ec3c63dade24ad351e9340e2f8e127694028c1fb7cec5035376bf098432",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="25c963b46a82d76d55b2302e0e18aac8175362656a465549999ad13d07b689b9",
        deprecated=True,
    )

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    # Disable the hip compile tests.  Spack should not be using
    # /opt/rocm, and this breaks the build when /opt/rocm exists.
    patch("hip-tests.patch", when="@:4.2.0")

    depends_on("cmake@3.2.0:", type="build", when="@:3.8")
    depends_on("cmake@3.13.4:", type="build", when="@3.9.0:")

    depends_on("zlib", type="link")
    depends_on("z3", type="link")
    depends_on("ncurses", type="link")

    depends_on("rocm-cmake@3.5.0:", type="build")

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
        # llvm libs are linked statically, so this *could* be a build dep
        depends_on("llvm-amdgpu@" + ver, when="@" + ver)

        # aomp may not build rocm-device-libs as part of llvm-amdgpu, so make
        # that a conditional dependency
        depends_on(
            "rocm-device-libs@" + ver, when="@{0} ^llvm-amdgpu ~rocm-device-libs".format(ver)
        )

    root_cmakelists_dir = join_path("lib", "comgr")

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
