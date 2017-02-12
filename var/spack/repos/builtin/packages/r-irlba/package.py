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


class RIrlba(RPackage):
    """Fast and memory efficient methods for truncated singular and eigenvalue
    decompositions and principal component analysis of large sparse or dense
    matrices."""

    homepage = "https://cran.r-project.org/web/packages/irlba/index.html"
    url      = "https://cran.r-project.org/src/contrib/irlba_2.1.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/irlba"

    version('2.1.2', '290940abf6662ed10c0c5a8db1bc6e88')
    version('2.0.0', '557674cf8b68fea5b9f231058c324d26')

    depends_on('r-matrix', type=('build', 'run'))
