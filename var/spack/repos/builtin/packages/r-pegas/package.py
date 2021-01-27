# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPegas(RPackage):
    """Functions for reading, writing, plotting, analysing, and
    manipulating allelic and haplotypic data, including from VCF files,
    and for the analysis of population nucleotide sequences and
    micro-satellites including coalescent analyses, linkage
    disequilibrium, population structure (Fst, Amova) and equilibrium
    (HWE), haplotype networks, minimum spanning tree and network, and
    median-joining networks."""

    homepage = "https://cran.r-project.org/web/packages/pegas/index.html"
    url      = "https://cran.r-project.org/src/contrib/pegas_0.14.tar.gz"

    maintainers = ['dorton21']

    version('0.14', sha256='7df90e6c4a69e8dbed2b3f68b18f1975182475bf6f86d4159256b52fd5332053')

    depends_on('r@3.2.0:+X', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-adegenet', type=('build', 'run'))
    depends_on('r-rgl', type=('build', 'run'))
    depends_on('r-rlang@0.4.7:', type=('build', 'run'))
    depends_on('texlive@2019:', type=('build', 'run'))
