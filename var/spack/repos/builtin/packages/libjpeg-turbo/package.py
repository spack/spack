# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibjpegTurbo(CMakePackage, AutotoolsPackage):
    """libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to
    accelerate baseline JPEG compression and decompression.

    libjpeg is a library that implements JPEG image encoding, decoding and
    transcoding.
    """

    # https://github.com/libjpeg-turbo/libjpeg-turbo/blob/master/BUILDING.md
    homepage = "https://libjpeg-turbo.org/"
    url = "https://github.com/libjpeg-turbo/libjpeg-turbo/archive/2.0.3.tar.gz"

    version("2.1.5", sha256="254f3642b04e309fee775123133c6464181addc150499561020312ec61c1bf7c")
    version("2.1.4", sha256="a78b05c0d8427a90eb5b4eb08af25309770c8379592bb0b8a863373128e6143f")
    version("2.1.3", sha256="dbda0c685942aa3ea908496592491e5ec8160d2cf1ec9d5fd5470e50768e7859")
    version("2.1.2", sha256="e7fdc8a255c45bc8fbd9aa11c1a49c23092fcd7379296aeaeb14d3343a3d1bed")
    version("2.1.1", sha256="20e9cd3e5f517950dfb7a300ad344543d88719c254407ffb5ad88d891bf701c4")
    version("2.1.0", sha256="d6b7790927d658108dfd3bee2f0c66a2924c51ee7f9dc930f62c452f4a638c52")
    version("2.0.6", sha256="005aee2fcdca252cee42271f7f90574dda64ca6505d9f8b86ae61abc2b426371")
    version("2.0.5", sha256="b3090cd37b5a8b3e4dbd30a1311b3989a894e5d3c668f14cbc6739d77c9402b7")
    version("2.0.4", sha256="7777c3c19762940cff42b3ba4d7cd5c52d1671b39a79532050c85efb99079064")
    version("2.0.3", sha256="a69598bf079463b34d45ca7268462a18b6507fdaa62bb1dfd212f02041499b5d")
    version("2.0.2", sha256="b45255bd476c19c7c6b198c07c0487e8b8536373b82f2b38346b32b4fa7bb942")
    version("1.5.90", sha256="cb948ade92561d8626fd7866a4a7ba3b952f9759ea3dd642927bc687470f60b7")
    version(
        "1.5.3",
        sha256="1a17020f859cb12711175a67eab5c71fc1904e04b587046218e36106e07eabde",
        deprecated=True,
    )
    version(
        "1.5.0",
        sha256="232280e1c9c3e6a1de95fe99be2f7f9c0362ee08f3e3e48d50ee83b9a2ed955b",
        deprecated=True,
    )
    version(
        "1.3.1",
        sha256="5008aeeac303ea9159a0ec3ccff295434f4e63b05aed4a684c9964d497304524",
        deprecated=True,
    )

    provides("jpeg")

    build_system(
        conditional("autotools", when="@:1.5.3"),
        conditional("cmake", when="@1.5.90:"),
        default="cmake",
    )

    variant("shared", default=True, description="Build shared libs")
    variant("static", default=True, description="Build static libs")
    variant("jpeg8", default=False, description="Emulate libjpeg v8 API/ABI")

    # Can use either of these. But in the current version of the package
    # only nasm is used. In order to use yasm an environmental variable
    # NASM must be set.
    # TODO: Implement the selection between two supported assemblers.
    # depends_on('yasm', type='build')
    depends_on("nasm", type="build")
    with when("build_system=autotools"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")

    with when("build_system=cmake"):
        depends_on("cmake", type="build", when="@1.5.90:")

    @property
    def libs(self):
        return find_libraries("libjpeg*", root=self.prefix, recursive=True)


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_SHARED", "shared"),
            self.define_from_variant("ENABLE_STATIC", "static"),
            self.define_from_variant("WITH_JPEG8", "jpeg8"),
        ]

        return args
