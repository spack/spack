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


class RGgally(RPackage):
    """The R package 'ggplot2' is a plotting system based on the grammar of
       graphics. 'GGally' extends 'ggplot2' by adding several functions to
       reduce the complexity of combining geometric objects with transformed
       data. Some of these functions include a pairwise plot matrix, a two
       group pairwise plot matrix, a parallel coordinates plot, a survival
       plot, and several functions to plot networks."""

    homepage = "https://cran.r-project.org/package=GGally"
    url      = "https://cran.r-project.org/src/contrib/GGally_1.3.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/GGally"

    version('1.3.2', 'efe58133ba8431198af7afb6bcb76264')

    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-gtable', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-progress', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-reshape', type=('build', 'run'))
