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


class RGgvis(RPackage):
    """An implementation of an interactive grammar of graphics, taking the best
    parts of 'ggplot2', combining them with the reactive framework from 'shiny'
    and web graphics from 'vega'."""

    homepage = "http://ggvis.rstudio.com/"
    url      = "https://cran.rstudio.com/src/contrib/ggvis_0.4.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ggvis"

    version('0.4.3', '30297d464278a7974fb125bcc7d84e77')
    version('0.4.2', '039f45e5c7f1e0652779163d7d99f922')

    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-shiny', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
