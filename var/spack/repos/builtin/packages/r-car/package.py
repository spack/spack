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


class RCar(RPackage):
    """Functions and Datasets to Accompany J. Fox and S. Weisberg, An R
    Companion to Applied Regression, Second Edition, Sage, 2011."""

    homepage = "https://r-forge.r-project.org/projects/car/"
    url      = "https://cran.r-project.org/src/contrib/car_2.1-4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/car"

    version('2.1-4', 'a66c307e8ccf0c336ed197c0f1799565')
    version('2.1-2', '0f78ad74ef7130126d319acec23951a0')

    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mgcv', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-pbkrtest', type=('build', 'run'))
    depends_on('r-quantreg', type=('build', 'run'))
