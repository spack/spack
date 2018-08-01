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


class RGtrellis(RPackage):
    """Genome level Trellis graph visualizes genomic data conditioned by
       genomic categories (e.g. chromosomes). For each genomic category,
       multiple dimensional data which are represented as tracks describe
       different features from different aspects. This package provides high
       flexibility to arrange genomic categories and to add self-defined
       graphics in the plot."""

    homepage = "https://bioconductor.org/packages/gtrellis/"
    git      = "https://git.bioconductor.org/packages/gtrellis.git"

    version('1.8.0', commit='f813b420a008c459f63a2a13e5e64c5507c4c472')

    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-circlize', type=('build', 'run'))
    depends_on('r-getoptlong', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.8.0')
