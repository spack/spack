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


class RGenomicfeatures(RPackage):
    """A set of tools and methods for making and manipulating transcript
       centric annotations. With these tools the user can easily download the
       genomic locations of the transcripts, exons and cds of a given organism,
       from either the UCSC Genome Browser or a BioMart database (more sources
       will be supported in the future). This information is then stored in a
       local database that keeps track of the relationship between transcripts,
       exons, cds and genes. Flexible methods are provided for extracting the
       desired features in a convenient format."""

    homepage = "http://bioconductor.org/packages/GenomicFeatures/"
    git      = "https://git.bioconductor.org/packages/GenomicFeatures.git"

    version('1.32.2', commit='8487aedc8be85a99f0c3fc90cd62430b3fec3a03')
    version('1.28.5', commit='ba92381ae93cb1392dad5e6acfab8f6c1d744834')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.29:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-iranges@2.13.23:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.15.4:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-genomicranges@1.31.17:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-annotationdbi@1.41.4:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-rsqlite@2.0:', when='@1.28.5:', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r-xvector@0.19.7:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-biostrings@2.47.6:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-rtracklayer', type=('build', 'run'))
    depends_on('r-rtracklayer@1.39.7:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-biomart', type=('build', 'run'))
    depends_on('r-biomart@2.17.1:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biobase@2.15.1:', when='@1.32.2', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.28.5', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.32.2', type=('build', 'run'))
