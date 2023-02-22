# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class HsaRocrDev(CMakePackage):
    """This repository includes the user mode API nterfaces and libraries
    necessary for host applications to launch computer kernels to available
    HSA ROCm kernel agents.AMD Heterogeneous System Architecture HSA -
    Linux HSA Runtime for Boltzmann (ROCm) platforms."""

    homepage = "https://github.com/RadeonOpenCompute/ROCR-Runtime"
    git = "https://github.com/RadeonOpenCompute/ROCR-Runtime.git"
    url = "https://github.com/RadeonOpenCompute/ROCR-Runtime/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "haampie")
    libraries = ["libhsa-runtime64"]

    version("master", branch="master")

    version("5.4.3", sha256="a600eed848d47a7578c60da7e64eb92f29bbce2ec67932b251eafd4c2974cb67")
    version("5.4.0", sha256="476cd18500cc227d01f6b44c00c7adc8574eb8234b6b4daefc219650183fa090")
    version("5.3.3", sha256="aca88d90f169f35bd65ce3366b8670c7cdbe3abc0a2056eab805d0192cfd7130")
    version("5.3.0", sha256="b51dbedbe73390e0be748b92158839c82d7fa0e514fede60aa7696dc498facf0")
    version("5.2.3", sha256="978de85d3455207bb82bef2254a4624e9116b1258a8c164d7a7e21a644eff12f")
    version("5.2.1", sha256="448a7409bdc6618332a42b9503122996f26b91768140b710ba99bff8a8c03dd9")
    version("5.2.0", sha256="529e49693dd9f6459586dd0a26f14dd77dbdf8c0b45fb54830b294eba7babd27")
    version("5.1.3", sha256="479340ec34cdffbbdb1002c85a47d1fccd23e8394631a1f001ef6130be08287d")
    version("5.1.0", sha256="a5f7245059c3d28dbc037e1e6fa3f09084e29147096dd61f7ce5560291ab330f")
    version(
        "5.0.2",
        sha256="94ce313f3b37e6571778dc6865d73dafa798cbaf4de63b5307382c4a2418e99f",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="61644365ea2b09fa7ec22f3dbdb74f2b6b1daa34b180138da9e0c856006a373e",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="d99eddedce0a97d9970932b64b0bb4743e47d2740e8db0288dbda7bec3cefa80",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="fbf550f243dddfef46a716e360b77c43886fed3eef67215ab9dab1c82f3851ca",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="85fbd1645120b71635844090ce8bd9f7af0a3d1065d5fae476879f99ba0c0475",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="2a08657a517971447fc233cb2c8ee2e117c6ab5efc31af147b28b3ef59b3847d",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="fa0e7bcd64e97cbff7c39c9e87c84a49d2184dc977b341794770805ec3f896cc",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="c223a5f7ccac280520abb6ea49fdd36fa9468718098a9d984be6ef839ccbc6db",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="e84c48e80ea38698a5bd5da3940048ad3cab3696d10a53132acad07ca357f17c",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="58866d8acdb6cc45227f2412098e37c65908b20ed3dd54901dfb515c15ad5f71",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="d722fb61f62037894957856f2c2d17231c4622bdf75db372321ee30206dceeb6",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="1dfad4d89d6c099e15073ed38e083bcf6cc463470dcc8a1e1b9e22060c060c72",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="0071d14431f73ce74574e61d0786f2b7cf34b14ea898a1f54b6e1b06b2d468c0",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="52c12eec3e3404c0749c70f156229786ee0c3e6d3c979aed9bbaea500fa1f3b8",
        deprecated=True,
    )

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )
    variant("shared", default=True, description="Build shared or static library")
    variant("image", default=True, description="build with or without image support")

    depends_on("cmake@3:", type="build")
    depends_on("pkgconfig", type="build", when="@5.3.0:")

    # Note, technically only necessary when='@3.7: +image', but added to all
    # to work around https://github.com/spack/spack/issues/23951
    depends_on("xxd", when="+image", type="build")
    depends_on("elf", type="link")
    depends_on("numactl")
    depends_on("pkgconfig", type="build", when="@5.3.0:")

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
        depends_on("hsakmt-roct@" + ver, when="@" + ver)
        depends_on("llvm-amdgpu@" + ver, when="@" + ver)
        # allow standalone rocm-device-libs (useful for aomp)
        depends_on(
            "rocm-device-libs@" + ver, when="@{0} ^llvm-amdgpu ~rocm-device-libs".format(ver)
        )

    # Both 3.5.0 and 3.7.0 force INSTALL_RPATH in different ways
    patch("0001-Do-not-set-an-explicit-rpath-by-default-since-packag.patch", when="@3.5.0")
    patch("0002-Remove-explicit-RPATH-again.patch", when="@3.7.0:")

    root_cmakelists_dir = "src"

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
        spec = self.spec

        # hsa-rocr-dev wants the directory containing the header files, but
        # libelf adds an extra path (include/libelf) compared to elfutils
        libelf_include = os.path.dirname(
            find_headers("libelf", spec["elf"].prefix.include, recursive=True)[0]
        )

        args = [
            self.define("LIBELF_INCLUDE_DIRS", libelf_include),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

        if self.spec.satisfies("@3.7.0:"):
            args.append(self.define_from_variant("IMAGE_SUPPORT", "image"))

            # device libs is bundled with llvm-amdgpu (default) or standalone
            if self.spec.satisfies("^rocm-device-libs"):
                bitcode_dir = spec["rocm-device-libs"].prefix.amdgcn.bitcode
            else:
                bitcode_dir = spec["llvm-amdgpu"].prefix.amdgcn.bitcode

            args.append(self.define("BITCODE_DIR", bitcode_dir))

        return args
