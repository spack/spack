# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mindthegap(CMakePackage):
    """MindTheGap is a software that performs integrated detection and
    assembly of genomic insertion variants in NGS read datasets with
    respect to a reference genome."""

    homepage = "https://gatb.inria.fr/software/mind-the-gap/"
    git = "https://github.com/GATB/MindTheGap.git"

    maintainers("snehring")

    version("2.3.0", tag="v2.3.0", submodules=True)
    version("2.0.2", tag="v2.0.2", submodules=True)

    depends_on("cmake@3.1:", type="build", when="@2.3.0")
    depends_on("cmake@2.6:", type="build", when="@2.0.2")

    depends_on("zlib")
