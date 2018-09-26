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


class ROrganismdbi(RPackage):
    """The package enables a simple unified interface to several annotation
       packages each of which has its own schema by taking advantage of the
       fact that each of these packages implements a select methods."""

    homepage = "https://bioconductor.org/packages/OrganismDbi/"
    git      = "https://git.bioconductor.org/packages/OrganismDbi.git"

    version('1.18.1', commit='ba2d1237256805e935d9534a0c6f1ded07b42e95')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-genomicfeatures', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocinstaller', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-rbgl', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.18.1')
