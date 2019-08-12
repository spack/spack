# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGlimma(RPackage):
    """This package generates interactive visualisations for analysis of
       RNA-sequencing data using output from limma, edgeR or DESeq2 packages
       in an HTML page. The interactions are built on top of the popular
       static representations of analysis results in order to provide
       additional information."""

    homepage = "https://bioconductor.org/packages/release/bioc/html/Glimma.html"
    git      = "https://git.bioconductor.org/packages/Glimma.git"

    version('1.8.2', commit='f4aa1f05c2890d04b01ad4c0ab27f2f729f2c969')

    depends_on('r@3.5.0:3.5.9', when='@1.8.2:', type=('build', 'run'))
    depends_on('r-edger', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
