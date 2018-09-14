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


class RGenomicranges(RPackage):
    """The ability to efficiently represent and manipulate genomic annotations
       and alignments is playing a central role when it comes to analyzing
       high-throughput sequencing data (a.k.a. NGS data). The GenomicRanges
       package defines general purpose containers for storing and manipulating
       genomic intervals and variables defined along a genome. More specialized
       containers for representing and manipulating short alignments against a
       reference genome, or a matrix-like summarization of an experiment, are
       defined in the GenomicAlignments and SummarizedExperiment packages
       respectively. Both packages build on top of the GenomicRanges
       infrastructure."""

    homepage = "https://bioconductor.org/packages/GenomicRanges/"
    git      = "https://git.bioconductor.org/packages/GenomicRanges.git"

    version('1.32.6', commit='31426be0fd6b76f7858971dc45aaf6e6d1dbac4e')
    version('1.30.3', commit='e99979054bc50ed8c0109bc54563036c1b368997')
    version('1.28.6', commit='197472d618f3ed04c795dc6ed435500c29619563')

    depends_on('r-biocgenerics@0.21.2:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.25.3:', when='@1.32.6', type=('build', 'run'))
    depends_on('r-s4vectors@0.9.47:', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.32:', when='@1.32.6', type=('build', 'run'))
    depends_on('r-iranges@2.9.11:', when='@1.28.6', type=('build', 'run'))
    depends_on('r-iranges@2.11.16:', when='@1.30.3', type=('build', 'run'))
    depends_on('r-iranges@2.14.4:', when='@1.32.6', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.11.5:', when='@1.28.6', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.13.1:', when='@1.30.3', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.15.2:', when='@1.32.6', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r-xvector@0.19.8:', when='@1.32.6', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.28.6', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.32.6', type=('build', 'run'))
