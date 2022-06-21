# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBrio(RPackage):
    """Basic R Input Output.

    Functions to handle basic input output, these functions always read and
    write UTF-8 (8-bit Unicode Transformation Format) files and provide more
    explicit control over line endings."""

    cran = "brio"

    version('1.1.3', sha256='eaa89041856189bee545bf1c42c7920a0bb0f1f70bb477487c467ee3e8fedcc6')
    version('1.1.0', sha256='6bb3a3b47bea13f1a1e3dcdc8b9f688502643e4b40a481a34aa04a261aabea38')
