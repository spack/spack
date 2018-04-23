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


class RInfluencer(RPackage):
    """Provides functionality to compute various node centrality measures on
    networks. Included are functions to compute betweenness centrality (by
    utilizing Madduri and Bader's SNAP library), implementations of Burt's
    constraint and effective network size (ENS) metrics, Borgatti's algorithm
    to identify key players, and Valente's bridging metric. On Unix systems,
    the betweenness, Key Players, and bridging implementations are parallelized
    with OpenMP, which may run faster on systems which have OpenMP
    configured."""

    homepage = "https://github.com/rcc-uchicago/influenceR"
    url      = "https://cran.r-project.org/src/contrib/influenceR_0.1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/influenceR"

    version('0.1.0', '6c8b6decd78c341364b5811fb3050ba5')

    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
