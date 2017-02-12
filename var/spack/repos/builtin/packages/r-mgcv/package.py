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


class RMgcv(RPackage):
    """GAMs, GAMMs and other generalized ridge regression with multiple
    smoothing parameter estimation by GCV, REML or UBRE/AIC. Includes a gam()
    function, a wide variety of smoothers, JAGS support and distributions
    beyond the exponential family."""

    homepage = "https://cran.r-project.org/package=mgcv"
    url      = "https://cran.r-project.org/src/contrib/mgcv_1.8-16.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mgcv"

    version('1.8-16', '4c1d85e0f80b017bccb4b63395842911')
    version('1.8-13', '30607be3aaf44b13bd8c81fc32e8c984')

    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
