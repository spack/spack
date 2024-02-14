# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import re

from spack.package import *


class Rdc(CMakePackage):
    """ROCm Data Center Tool"""

    homepage = "https://github.com/ROCm/rdc"
    url = "https://github.com/ROCm/rdc/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["librdc"]

    def url_for_version(self, version):
        if version == Version("3.9.0"):
            return "https://github.com/ROCm/rdc/archive/rdc_so_ver-0.3.tar.gz"

        url = "https://github.com/ROCm/rdc/archive/rocm-{0}.tar.gz"
        return url.format(version)

    license("MIT")

    version("6.0.2", sha256="00defa3b68c340d7f46b8cb06b37ab0602a7949bfddc884b01c163a1526502f8")
    version("6.0.0", sha256="5e3847a919d5f7efe99d8d76c96e78401659eccd1fb234b1b8cb4304096d6e89")
    version("5.7.1", sha256="5251eb3085f2019246b332e9552dfae1572cf64ddf58306b81cbe7108019ffee")
    version("5.7.0", sha256="924e94f14f6390d7a6ff7863fb4e2085c1ff5f9c12b8bd46471eb31f001c4f14")
    version("5.6.1", sha256="9e9f57cebbc5ae386a405957ed2c17344cdb42db5e1a71285f2c9bc09eea6519")
    version("5.6.0", sha256="5213cd89215463862f6a1e9480ebe017944a6bb6b0db1722628afaa34af57991")
    version("5.5.1", sha256="a58a319ee702cf61cf71a4eba647c231392f68449b35419d941079c6de944844")
    version("5.5.0", sha256="56e85e77581963fbcfcc43e091a91773de470152347808ae730bcaf92c9f5ee8")
    version("5.4.3", sha256="c44f0b070b5650bc78e2eb968aae57a8ac1e1fd160e897055b79f3026c4fbad3")
    version("5.4.0", sha256="268aab43e31045443b08a21aee8750da4cf04750c6f419ec171ec704d377a4e4")
    version("5.3.3", sha256="1bf1a02f305e3a629801e62584116a34eafbd1b26627837a2a8c10550fcf611b")
    version("5.3.0", sha256="ce9c85dad8e0c0b21e8e5938bf16f86a62dc5f6ded5f453c61acd43666634d6b")
    with default_args(deprecated=True):
        version("5.2.3", sha256="5ba060449bbf5e84979cb4c62eb1dac9b0e3eca45e930d2e20e7beaa87361b39")
        version("5.2.1", sha256="84b3c3754b8c9732ee6d00d37881591d3d6876feb8f29746d9eb18faea7ad035")
        version("5.2.0", sha256="2f35f74485e783f56ea724a7c69ce825f181fcdbe89de453d97ce6a3d3176ae0")
        version("5.1.3", sha256="ac3e594d7b245c787d6d9b63f551ca898d4d9403fbec0e4502f9970575e031b8")
        version("5.1.0", sha256="3cf58cb07ef241b3b73b23af83b6477194884feba642584a491e67deeceff038")
    version(
        "5.0.2",
        sha256="9e21fe7e9dd02b69425dab6be22a85469fee072bcebd2d2957633dfad8b45574",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="68d45a319dc4222d94e1fb1ce10df5f3464de0b745d0d2e9aebbf273493adcc5",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="1b467e2a473374488292ca1680562ec4e798f43847ea6464453f8f8297f12d8d",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="e9bc53d068e9a4fdccff587e34c7fe0880f003a18652cd48c29faf031dd2c98f",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="aae028aae61eb0f4dd30708c4bbb8c5c57a426f10dae9b967b81500fb106d981",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="d3dda2022ec1f8c7de4de64696009125a903fcb2f82c38b3ac07e4ab35bf9190",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="ea2c7c07d55f607968f58d7e30326cae5db5b48c1ba354caa5727394d5bad258",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="dc81ee9727c8913c05dcf20a00669ce611339ef6d6db8af34e57f42bcfa804ac",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="e9ebfc46dfa983400909ed8a9da4fa37869ab118a8426c2e4f793e21174ca07f",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="fdc51f9f1f756406d1e2ffaeee0e247d1b04fc4078f08e581bbaa7da79697ac1",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="bc6339e7f41850a4a049d085a880cfafd3fd8e1610fb94c572d79753d01aa298",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="d0d0a0e68a848b7a8fa2d88c1d0352ce68e1e142debf32c31d941904f03c4b2f",
        deprecated=True,
    )

    depends_on("cmake@3.15:3.19.7", type="build", when="@:4.3.1")
    depends_on("cmake@3.15:", type="build", when="@4.5.0:")
    depends_on("grpc@1.28.1+shared", type="build", when="@:5.3")
    depends_on("grpc@1.44.0+shared", when="@5.4.0:5.4")
    depends_on("grpc@1.55.0+shared", when="@5.5.0:")
    depends_on("protobuf")
    depends_on("libcap")

    for ver in [
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
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
    ]:
        depends_on("rocm-smi-lib@" + ver, type=("build", "link"), when="@" + ver)

    for ver in [
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
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
    ]:
        depends_on("hsa-rocr-dev@" + ver, when="@" + ver)

    for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1", "5.7.0", "5.7.1", "6.0.0", "6.0.2"]:
        depends_on("rocm-core@" + ver, when="@" + ver)

    def patch(self):
        filter_file(r"\${ROCM_DIR}/rocm_smi", "${ROCM_SMI_DIR}", "CMakeLists.txt")
        filter_file(
            r"${GRPC_ROOT}/bin/protoc",
            "{0}/bin/protoc".format(self.spec["protobuf"].prefix),
            "CMakeLists.txt",
            string=True,
        )
        if self.spec.satisfies("@5.4.0:5.4"):
            filter_file(
                "${ROCM_DIR}/${CMAKE_INSTALL_INCLUDEDIR}",
                "{0}/include".format(self.spec["rocm-smi-lib"].prefix),
                "CMakeLists.txt",
                string=True,
            )
            filter_file(
                "${ROCM_DIR}/${CMAKE_INSTALL_LIBDIR}",
                "{0}/lib".format(self.spec["rocm-smi-lib"].prefix),
                "CMakeLists.txt",
                string=True,
            )

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
        rpath = self.rpath
        rpath.append(self.prefix.opt.rocm.rdc.lib)
        rpath = ";".join(rpath)
        args = [
            "-DCMAKE_INSTALL_RPATH=" + rpath,
            "-DGRPC_ROOT=" + self.spec["grpc"].prefix,
            "-DCMAKE_MODULE_PATH={0}/cmake_modules".format(self.stage.source_path),
            "-DROCM_SMI_DIR=" + self.spec["rocm-smi-lib"].prefix,
            "-DCMAKE_BUILD_WITH_INSTALL_RPATH=1",
        ]
        return args
