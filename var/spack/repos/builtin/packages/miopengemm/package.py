# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Miopengemm(CMakePackage):
    """An OpenCL general matrix multiplication (GEMM) API
    and kernel generator"""

    homepage = "https://github.com/ROCm/MIOpenGEMM"
    git = "https://github.com/ROCm/MIOpenGEMM.git"
    url = "https://github.com/ROCm/MIOpenGEMM/archive/rocm-6.0.0.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["libmiopengemm"]

    def url_for_version(self, version):
        if version == Version("1.1.6"):
            return "https://github.com/ROCm/MIOpenGEMM/archive/1.1.6.tar.gz"
        url = "https://github.com/ROCm/MIOpenGEMM/archive/rocm-{0}.tar.gz"
        return url.format(version)

    license("MIT")

    with default_args(deprecated=True):
        version("5.5.1", sha256="a997b560521641e7173613cf547ecde5d15ac6fac1786d392b0f133c91f99a40")
        version("5.5.0", sha256="ffd9775129564662b338952588057a088f7e9723b4a9a766b2dd96fdc0992c26")
        version("5.4.3", sha256="5051051cab60ca0f6347a981da6c9dbeddf8b0de698d4e5409a0db0c622acafc")

    depends_on("cmake@3:", type="build")

    for ver in ["5.5.0", "5.5.1"]:
        depends_on(f"rocm-cmake@{ver}", type="build", when=f"@{ver}")
        depends_on(f"rocm-opencl@{ver}", when=f"@{ver}")

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
