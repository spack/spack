# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RZip(RPackage):
    """Cross-Platform 'zip' Compression.

    Cross-Platform 'zip' Compression Library. A replacement for the 'zip'
    function, that does not require any additional external tools on any
    platform."""

    cran = "zip"

    version('2.2.0', sha256='9f95987c964039834f770ecda2d5f7e3d3a9de553c89db2a5926c4219bf4b9d8')
    version('2.1.1', sha256='11dd417932296d3a25c53aa8d3b908973c4945a496cc473dd321825dfaaa7c2c')
    version('2.0.3', sha256='4a8cb8e41eb630bbf448a0fd56bcaeb752b8484fef98c6419334edf46401317e')
