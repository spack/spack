##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class RGgbio(RPackage):
    """The ggbio package extends and specializes the grammar of graphics for
       biological data. The graphics are designed to answer common scientific
       questions, in particular those often asked of high throughput genomics
       data. All core Bioconductor data structures are supported, where
       appropriate. The package supports detailed views of particular genomic
       regions, as well as genome-wide overviews. Supported overviews include
       ideograms and grand linear views. High-level plots include sequence
       fragment length, edge-linked interval to data view, mismatch pileup,
       and several splicing summaries."""

    homepage = "http://bioconductor.org/packages/ggbio/"
    git      = "https://git.bioconductor.org/packages/ggbio.git"

    version('1.24.1', commit='ef04c1bca1330f37152bcc21080cbde94849a094')

    depends_on('r-gridextra', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-gtable', type=('build', 'run'))
    depends_on('r-hmisc', type=('build', 'run'))
    depends_on('r-biovizbase', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-genomicalignments', type=('build', 'run'))
    depends_on('r-bsgenome', type=('build', 'run'))
    depends_on('r-variantannotation', type=('build', 'run'))
    depends_on('r-rtracklayer', type=('build', 'run'))
    depends_on('r-genomicfeatures', type=('build', 'run'))
    depends_on('r-organismdbi', type=('build', 'run'))
    depends_on('r-ggally', type=('build', 'run'))
    depends_on('r-ensembldb', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-annotationfilter', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.24.1')
