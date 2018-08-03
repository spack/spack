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


class RGenomicalignments(RPackage):
    """Provides efficient containers for storing and manipulating short genomic
    alignments (typically obtained by aligning short reads to a reference
    genome). This includes read counting, computing the coverage, junction
    detection, and working with the nucleotide content of the alignments."""

    homepage = "https://bioconductor.org/packages/GenomicAlignments/"
    git      = "https://git.bioconductor.org/packages/GenomicAlignments.git"

    version('1.14.2', commit='57b0b35d8b36069d4d94af86af051f0129b28eef')
    version('1.12.2', commit='b5d6f19e4a89b6c1c3e9e58e5ea4eb13870874ef')

    depends_on('r-biocgenerics@0.15.3:', type=('build', 'run'))
    depends_on('r-s4vectors@0.13.13:', type=('build', 'run'))
    depends_on('r-iranges@2.5.36:', type=('build', 'run'), when='@1.12.2')
    depends_on('r-iranges@2.11.16:', type=('build', 'run'), when='@1.14.2')
    depends_on('r-genomeinfodb@1.11.5:', type=('build', 'run'), when='@1.12.2')
    depends_on('r-genomeinfodb@1.13.1:', type=('build', 'run'), when='@1.14.2')
    depends_on('r-genomicranges@1.27.19:', type=('build', 'run'), when='@1.12.2')
    depends_on('r-genomicranges@1.29.14:', type=('build', 'run'), when='@1.14.2')
    depends_on('r-summarizedexperiment@1.5.3:', type=('build', 'run'))
    depends_on('r-biostrings@2.37.1:', type=('build', 'run'))
    depends_on('r-rsamtools@1.21.4:', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.12.2:')
