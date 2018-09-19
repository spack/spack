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


class RBsgenome(RPackage):
    """Infrastructure shared by all the Biostrings-based genome data
       packages."""

    homepage = "https://www.bioconductor.org/packages/BSgenome/"
    git      = "https://git.bioconductor.org/packages/BSgenome.git"

    version('1.46.0', commit='bdfbd6d09820993585b8231ddea5e11c99008dc5')
    version('1.44.2', commit='105b00588a758d5ec7c347a7dff2756aea4516a0')

    depends_on('r-biocgenerics@0.13.8:', type=('build', 'run'))
    depends_on('r-s4vectors@0.9.36:', type=('build', 'run'))
    depends_on('r-iranges@2.1.33:', type=('build', 'run'), when='@1.44.2')
    depends_on('r-iranges@2.11.16:', type=('build', 'run'), when='@1.46.0')
    depends_on('r-genomeinfodb@1.11.4:', type=('build', 'run'), when='@1.44.2')
    depends_on('r-genomeinfodb@1.13.1:', type=('build', 'run'), when='@1.46.0')
    depends_on('r-genomicranges@1.27.6:', type=('build', 'run'), when='@1.44.2')
    depends_on('r-genomicranges@1.29.14:', type=('build', 'run'), when='@1.46.0')
    depends_on('r-biostrings@2.35.3:', type=('build', 'run'))
    depends_on('r-rtracklayer@1.25.8:', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.44.2:')
