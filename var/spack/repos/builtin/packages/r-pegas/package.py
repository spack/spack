# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPegas(RPackage):
    """Population and Evolutionary Genetics Analysis System.

    Functions for reading, writing, plotting, analysing, and manipulating
    allelic and haplotypic data, including from VCF files, and for the analysis
    of population nucleotide sequences and micro-satellites including
    coalescent analyses, linkage disequilibrium, population structure (Fst,
    Amova) and equilibrium (HWE), haplotype networks, minimum spanning tree and
    network, and median-joining networks."""

    cran = "pegas"

    maintainers("dorton21")

    version("1.2", sha256="9d39f3937c09ea6e2189949a23879bb366f5ca1df3a6aac411c7d2b73837ad55")
    version("1.1", sha256="87ba91a819496dfc3abdcc792ff853a6d49caae6335598a24c23e8851505ed59")
    version("0.14", sha256="7df90e6c4a69e8dbed2b3f68b18f1975182475bf6f86d4159256b52fd5332053")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-ape@5.3-11:", type=("build", "run"))

    depends_on("r-adegenet", type=("build", "run"), when="@:0.14")
