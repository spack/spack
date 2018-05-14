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


class RGenomeinfodb(RPackage):
    """Contains data and functions that define and allow translation between
       different chromosome sequence naming conventions (e.g., "chr1"
       versus "1"), including a function that attempts to place sequence
       names in their natural, rather than lexicographic, order."""

    homepage = "https://bioconductor.org/packages/GenomeInfoDb/"
    url      = "https://git.bioconductor.org/packages/GenomeInfoDb"
    list_url = homepage

    version('1.14.0', git='https://git.bioconductor.org/packages/GenomeInfoDb', commit='4978308a57d887b764cc4ce83724ca1758f580f6')
    version('1.12.3', git='https://git.bioconductor.org/packages/GenomeInfoDb', commit='2deef3f0571b7f622483257bc22d2509ab5a0369')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
    depends_on('r-genomeinfodbdata', type=('build', 'run'))
    depends_on('r@3.4.0:', when='@1.12.3:')
