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


class RDygraphs(RPackage):
    """An R interface to the 'dygraphs' JavaScript charting library (a copy of
    which is included in the package). Provides rich facilities for charting
    time-series data in R, including highly configurable series- and
    axis-display and interactive features like zoom/pan and series/point
    highlighting."""

    homepage = "https://cran.r-project.org/web/packages/dygraphs/index.html"
    url      = "https://cran.r-project.org/src/contrib/dygraphs_1.1.1.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/dygraphs"

    version('1.1.1.4', '85dab4d471c2842887f46afc2521f4bb')
    version('0.9', '7f0ce4312bcd3f0a58b8c03b2772f833')

    depends_on('r@3.0:')

    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-htmlwidgets@0.6:', type=('build', 'run'))
    depends_on('r-htmltools@0.3.5:', when=('@1.1.1.4:'), type=('build', 'run'))
    depends_on('r-zoo@1.7-10:', type=('build', 'run'))
    depends_on('r-xts@0.9-7:', type=('build', 'run'))
