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


class RProdlim(RPackage):
    """Product-Limit Estimation for Censored Event History Analysis. Fast and
    user friendly implementation of nonparametric estimators for censored event
    history (survival) analysis. Kaplan-Meier and Aalen-Johansen method."""

    homepage = "https://cran.r-project.org/package=prodlim"
    url      = "https://cran.r-project.org/src/contrib/prodlim_1.5.9.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/prodlim"

    version('1.5.9', 'e0843053c9270e41b657a733d6675dc9')

    depends_on('r@2.9.0:')

    depends_on('r-rcpp@0.11.5:', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-kernsmooth', type=('build', 'run'))
    depends_on('r-lava', type=('build', 'run'))
