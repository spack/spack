# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack.package import *


class OpenclCHeaders(Package):
    """OpenCL (Open Computing Language) C header files"""

    homepage = "https://www.khronos.org/registry/OpenCL/"
    url = "https://github.com/KhronosGroup/OpenCL-Headers/archive/v2020.06.16.tar.gz"
    maintainers("lorddavidiii")

    version(
        "2022.01.04", sha256="6e716e2b13fc8d363b40a165ca75021b102f9328e2b38f8054d7db5884de29c9"
    )
    version(
        "2021.06.30", sha256="6640d590c30d90f89351f5e3043ae6363feeb19ac5e64bc35f8cfa1a6cd5498e"
    )
    version(
        "2021.04.29", sha256="477e2b26125d99a9b2f20c68262f27ca3f3ca7899593a8af2b7fe077bdce18d1"
    )
    version(
        "2020.12.18", sha256="5dad6d436c0d7646ef62a39ef6cd1f3eba0a98fc9157808dfc1d808f3705ebc2"
    )
    version(
        "2020.06.16", sha256="2f5a60e5ac4b127650618c58a7e3b35a84dbf23c1a0ac72eb5e7baf221600e06"
    )
    version(
        "2020.03.13", sha256="664bbe587e5a0a00aac267f645b7c413586e7bc56dca9ff3b00037050d06f476"
    )

    def install(self, spec, prefix):
        install_tree("CL", prefix.include.CL)
        if sys.platform == "darwin":
            ln = which("ln")
            ln("-s", prefix.include.CL, prefix.include.OpenCL)
