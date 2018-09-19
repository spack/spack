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


class RShortread(RPackage):
    """This package implements sampling, iteration, and input of FASTQ
    files. The package includes functions for filtering and trimming
    reads, and for generating a quality assessment report. Data are
    represented as DNAStringSet-derived objects, and easily manipulated
    for a diversity of purposes. The package also contains legacy support
    for early single-end, ungapped alignment formats."""

    homepage = "https://www.bioconductor.org/packages/ShortRead/"
    git      = "https://git.bioconductor.org/packages/ShortRead.git"

    version('1.34.2', commit='25daac63b301df66a8ef6e98cc2977522c6786cd')

    depends_on('r@3.4.0:3.4.9', when='@1.34.2')
    depends_on('r-latticeextra', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('r-hwriter', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-genomicalignments', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
