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


class RIgraph(RPackage):
    """Routines for simple graphs and network analysis. It can handle large
    graphs very well and provides functions for generating random and regular
    graphs, graph visualization, centrality methods and much more."""

    homepage = "http://igraph.org/"
    url      = "https://cran.r-project.org/src/contrib/igraph_1.0.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/igraph"

    version('1.1.2', 'ca1617aea272852d2856c4661ad1c7d8')
    version('1.0.1', 'ea33495e49adf4a331e4ba60ba559065')

    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-pkgconfig', type=('build', 'run'))
    depends_on('r-irlba', type=('build', 'run'))
    depends_on('gmp')
    depends_on('libxml2')
