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


class RIpred(RPackage):
    """Improved predictive models by indirect classification and bagging for
    classification, regression and survival problems as well as resampling
    based estimators of prediction error."""

    homepage = "https://cran.r-project.org/package=ipred"
    url      = "https://cran.r-project.org/src/contrib/ipred_0.9-5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ipred"

    version('0.9-5', 'ce8768547a7aa9554ad3650b18ea3cbd')

    depends_on('r@2.10:')

    depends_on('r-rpart@3.1-8:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-class', type=('build', 'run'))
    depends_on('r-prodlim', type=('build', 'run'))
