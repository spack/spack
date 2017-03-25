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


class RDplyr(RPackage):
    """A fast, consistent tool for working with data frame like objects, both
    in memory and out of memory."""

    homepage = "https://github.com/hadley/dplyr"
    url      = "https://cran.r-project.org/src/contrib/dplyr_0.5.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/dplyr"

    version('0.5.0', '1fcafcacca70806eea2e6d465cdb94ef')

    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'run'))
