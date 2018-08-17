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


class RSomaticsignatures(RPackage):
    """The SomaticSignatures package identifies mutational signatures of
       single nucleotide variants (SNVs). It provides a infrastructure related
       to the methodology described in Nik-Zainal (2012, Cell), with
       flexibility in the matrix decomposition algorithms."""

    homepage = "https://bioconductor.org/packages/SomaticSignatures/"
    git      = "https://git.bioconductor.org/packages/SomaticSignatures.git"

    version('2.12.1', commit='932298c6877d076004de5541cec85a14e819517a')

    depends_on('r-variantannotation', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-nmf', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-ggbio', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-pcamethods', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-proxy', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.12.1')
