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


class RCrosstalk(RPackage):
    """Provides building blocks for allowing HTML widgets to communicate with
    each other, with Shiny or without (i.e. static .html files). Currently
    supports linked brushing and filtering."""

    homepage = "http://rstudio.github.io/crosstalk/"
    url      = "https://cran.r-project.org/src/contrib/crosstalk_1.0.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/crosstalk"

    version('1.0.0', 'c13c21b81af2154be3f08870fd3a7077')

    depends_on('r-htmltools@0.3.5:', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-shiny@0.11:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
