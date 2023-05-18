# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Maeparser(CMakePackage):
    """Parser for Schrodinger Maestro files"""

    homepage = "https://github.com/schrodinger/maeparser"
    url = "https://github.com/schrodinger/maeparser/archive/refs/tags/v1.3.0.tar.gz"

    maintainers("RMeli")

    version("1.3.0", sha256="fa8f9336de1e5d1cabec29a6da04547b1fb040bb32ba511ff30b4a14097c751c")

    variant(
        "shared",
        default=True,
        description="Build maeparser as a shared library (turn off for a static one)",
    )

    depends_on("boost +iostreams +filesystem +test")
    depends_on("zlib")

    def cmake_args(self):
        args = [self.define_from_variant("MAEPARSER_BUILD_SHARED_LIBS", "shared")]
        return args
