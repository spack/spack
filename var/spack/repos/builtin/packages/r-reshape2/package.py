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


class RReshape2(RPackage):
    """Flexibly restructure and aggregate data using just two functions: melt
    and dcast (or acast)."""

    homepage = "https://github.com/hadley/reshape"
    url      = "https://cran.r-project.org/src/contrib/reshape2_1.4.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/reshape2"

    version('1.4.2', 'c851a0312191b8c5bab956445df7cf5f')
    version('1.4.1', '41e9dffdf5c6fa830321ac9c8ebffe00')

    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
