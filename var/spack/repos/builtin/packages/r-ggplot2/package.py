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


class RGgplot2(RPackage):
    """An implementation of the grammar of graphics in R. It combines the
    advantages of both base and lattice graphics: conditioning and shared axes
    are handled automatically, and you can still build up a plot step by step
    from multiple data sources. It also implements a sophisticated
    multidimensional conditioning system and a consistent interface to map data
    to aesthetic attributes. See http://ggplot2.org for more information,
    documentation and examples."""

    homepage = "http://ggplot2.org/"
    url      = "https://cran.r-project.org/src/contrib/ggplot2_2.2.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ggplot2"

    version('2.2.1', '14c5a3507bc123c6e7e9ad3bef7cee5c')
    version('2.1.0', '771928cfb97c649c720423deb3ec7fd3')

    depends_on('r@3.1:')

    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-gtable@0.1.1:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-plyr@1.7.1:', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-scales@0.4.1', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
