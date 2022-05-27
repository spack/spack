# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RBitops(RPackage):
    """Bitwise Operations.

    Functions for bitwise operations on integer vectors."""

    cran = "bitops"

    version('1.0-7', sha256='e9b5fc92c39f94a10cd0e13f3d6e2a9c17b75ea01467077a51d47a5f708517c4')
    version('1.0-6', sha256='9b731397b7166dd54941fb0d2eac6df60c7a483b2e790f7eb15b4d7b79c9d69c')
