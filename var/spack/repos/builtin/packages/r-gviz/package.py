# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGviz(RPackage):
    """Genomic data analyses requires integrated visualization
    of known genomic information and new experimental data. Gviz
    uses the biomaRt and the rtracklayer packages to perform live
    annotation queries to Ensembl and UCSC and translates this to
    e.g. gene/transcript structures in viewports of the grid
    graphics package. This results in genomic information plotted
    together with your data."""

    homepage = "http://bioconductor.org/packages/Gviz/"
    git      = "https://git.bioconductor.org/packages/Gviz.git"

    version('1.20.0', commit='299b8255e1b03932cebe287c3690d58c88f5ba5c')

    depends_on('r@3.4.0:3.4.9', when='@1.20.0')
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r-rtracklayer', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-biomart', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-genomicfeatures', type=('build', 'run'))
    depends_on('r-bsgenome', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-biovizbase', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-latticeextra', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r-genomicalignments', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
