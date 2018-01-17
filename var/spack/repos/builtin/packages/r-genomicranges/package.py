##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
    url      = "https://git.bioconductor.org/packages/GenomicRanges"
    list_url = homepage

    version('1.28.6', git='https://git.bioconductor.org/packages/GenomicRanges', commit='197472d618f3ed04c795dc6ed435500c29619563')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.28.6')
