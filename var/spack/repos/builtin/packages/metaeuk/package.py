# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Metaeuk(CMakePackage):
    """MetaEuk is a modular toolkit designed for large-scale gene discovery
    and annotation in eukaryotic metagenomic contigs.
    """

    homepage = "https://metaeuk.soedinglab.org/"
    url = "https://github.com/soedinglab/metaeuk/archive/refs/tags/6-a5d39d9.tar.gz"
    maintainers("snehring")

    version("6-a5d39d9", sha256="be19c26f5bdb7dcdd7bc48172105afecf19e5a2e5555edb3ba0c4aa0e4aac126")

    depends_on("cmake@2.8.12:", type="build")
