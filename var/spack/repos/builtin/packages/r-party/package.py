##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class RParty(RPackage):
    """A computational toolbox for recursive partitioning."""

    homepage = "https://cran.r-project.org/web/packages/party/index.html"
    url      = "https://cran.r-project.org/src/contrib/party_1.2-3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/party"

    version('1.2-3', '77b042c6014d0c52b5e6bd9feab26e9e')
    version('1.1-2', '40a00336cf8418042d2ab616675c8ddf')

    depends_on('r@2.14.0:', when=('@:1.1-9'))
    depends_on('r@3.0.0:', when=('@1.2-0:'))

    depends_on('r-mvtnorm@1.0-2:', type=('build', 'run'))
    depends_on('r-modeltools@0.2-21:', type=('build', 'run'))
    depends_on('r-strucchange', type=('build', 'run'))
    depends_on('r-survival@2.37-7:', type=('build', 'run'))
    depends_on('r-coin@1.1-0:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-sandwich@1.1-1:', type=('build', 'run'))
