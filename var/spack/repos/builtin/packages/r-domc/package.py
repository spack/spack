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


class RDomc(RPackage):
    """Provides a parallel backend for the %dopar% function using
    the multicore functionality of the parallel package."""

    homepage = "https://cran.r-project.org/package=doMC"
    url      = "https://cran.r-project.org/src/contrib/doMC_1.3.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/doMC"

    version('1.3.4', 'f965b09add9056e84f99a831dc3af7d1')

    depends_on('r@2.14.0:')

    depends_on('r-foreach@1.2.0:', type=('build', 'run'))
    depends_on('r-iterators@1.0.0:', type=('build', 'run'))
