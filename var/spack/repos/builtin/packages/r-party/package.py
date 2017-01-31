##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
    url      = "https://cran.r-project.org/src/contrib/party_1.1-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/party"

    version('1.1-2', '40a00336cf8418042d2ab616675c8ddf')

    depends_on('r@2.14.0:')

    depends_on('r-mvtnorm@1.0-2:', type=('build', 'run'))
    depends_on('r-modeltools@0.1-21:', type=('build', 'run'))
    depends_on('r-strucchange', type=('build', 'run'))
    depends_on('r-survival@2.37-7:', type=('build', 'run'))
    depends_on('r-coin@1.1-0:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-sandwich@1.1-1:', type=('build', 'run'))
