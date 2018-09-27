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


class RRsamtools(RPackage):
    """This package provides an interface to the 'samtools', 'bcftools', and
       'tabix' utilities (see 'LICENCE') for manipulating SAM (Sequence
       Alignment / Map), FASTA, binary variant call (BCF) and compressed
       indexed tab-delimited (tabix) files."""

    homepage = "https://bioconductor.org/packages/Rsamtools/"
    git      = "https://git.bioconductor.org/packages/Rsamtools.git"

    version('1.32.2', commit='2b3254ccdeb24dc6ad95a93c2eb527021631797e')
    version('1.28.0', commit='dfa5b6abef68175586f21add7927174786412472')

    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.1.3:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-genomicranges@1.31.8:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-biostrings@2.47.6:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biocgenerics@0.25.1:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.25:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-iranges@2.13.12:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r-xvector@0.19.7:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('r-bitops', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.28.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.32.2', type=('build', 'run'))
