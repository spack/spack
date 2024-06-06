# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class RocmDbgapi(CMakePackage):
    """The AMD Debugger API is a library that provides all the support
    necessary for a debugger and other tools to perform low level
    control of the execution and inspection of execution state of
    AMD's commercially available GPU architectures."""

    homepage = "https://github.com/ROCm/ROCdbgapi"
    git = "https://github.com/ROCm/ROCdbgapi.git"
    url = "https://github.com/ROCm/ROCdbgapi/archive/rocm-6.1.1.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["librocm-dbgapi"]

    license("MIT")

    version("master", branch="amd-master")
    version("6.1.1", sha256="425a6cf6a3942c2854c1f5e7717bed906cf6c3753b46c44476f54bfef6188dac")
    version("6.1.0", sha256="0985405b6fd44667a7ce8914aa39a7e651613e037e649fbdbfa2adcf744a2d50")
    version("6.0.2", sha256="39036f083de421f46afd8d3a8799576242ef64002643d7185767ccbba41ae854")
    version("6.0.0", sha256="4e823eba255e46b93aff05fd5938ef2a51693ffd74debebffc1aabfce613805c")
    version("5.7.1", sha256="0ee9c2f083868849f2ea0cec7010e0270c27e7679ccbbadd12072cc0ef6c8a6f")
    version("5.7.0", sha256="285ddded8e7f1981d8861ffc1cd7770b78129e4955da08ad55a4779945699716")
    version("5.6.1", sha256="c7241bf94bdb97a4cf1befbf25b8c35720797710da6f6b5b9d6a4094c1bc9c8b")
    version("5.6.0", sha256="9b66e47f4eccb3c8bbc324aade92aac6139539dda449427b7823d0c45341afc8")
    version("5.5.1", sha256="c41dfc62591bcf42003fe744d8bd03a51311d54e4b012f946ca0ede0c14dd977")
    version("5.5.0", sha256="ce572340a3fe99e4f1538eb614933153456003f8dfe9306a5735cdd25b451e25")
    version("5.4.3", sha256="d647c9121a50f2c54367c567d8f39a145cb135e1ceed931581659f57f49f61e5")
    version("5.4.0", sha256="895eb7056864daada40c3f9cd37645b0bdf4b6dc408b5f8cc974fc4cd9ab7ccb")
    version("5.3.3", sha256="3c81cb23fe671d391557a63c13b6a13d4dc367db5cb5de55592a6758284d8a3f")
    version("5.3.0", sha256="afffec78e34fe70952cd41efc3d7ba8f64e43acb2ad20aa35c9b8b591bed48ca")
    with default_args(deprecated=True):
        version("5.2.3", sha256="17925d23f614ecb2b40dffe5e14535cba380d4f489ea1a027762c356be9fbc2b")
        version("5.2.1", sha256="169e3914ebd99d6a5c034c568964b7bad56611262e292f77c0c65a7708e02376")
        version("5.2.0", sha256="44f0528a7583bc59b6585166d2289970b20115c4c70e3bcc218aff19fc242b3f")
        version("5.1.3", sha256="880f80ebf741e3451676837f720551e02cffd0b9346ca4dfa6cf7f7043282f2b")
        version("5.1.0", sha256="406db4b20bda12f6f32cbef88b03110aa001bf7bef6676f36e909b53c8354e43")

    depends_on("cmake@3:", type="build")
    depends_on("hwdata", when="@5.5.0:")

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
        "master",
    ]:
        depends_on(f"hsa-rocr-dev@{ver}", type="build", when=f"@{ver}")
        depends_on(f"comgr@{ver}", type=("build", "link"), when=f"@{ver}")

    for ver in [
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
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            return "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        return None

    def patch(self):
        filter_file(
            r"(<INSTALL_INTERFACE:include>)",
            r"\1 {0}/include".format(self.spec["hsa-rocr-dev"].prefix),
            "CMakeLists.txt",
        )

    def cmake_args(self):
        args = []
        if self.spec.satisfies("@5.3.0:"):
            args.append(self.define("CMAKE_INSTALL_LIBDIR", "lib"))
        return args
