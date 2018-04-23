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


class RGlmnet(RPackage):
    """Extremely efficient procedures for fitting the entire lasso or
    elastic-net regularization path for linear regression, logistic and
    multinomial regression models, Poisson regression and the Cox model. Two
    recent additions are the multiple-response Gaussian, and the grouped
    multinomial. The algorithm uses cyclical coordinate descent in a path-wise
    fashion, as described in the paper linked to via the URL below."""

    homepage = "https://cran.rstudio.com/web/packages/glmnet/index.html"
    url      = "https://cran.rstudio.com/src/contrib/glmnet_2.0-13.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/glmnet"
    version('2.0-13', '1dd5636388df5c3a29207d0bf1253343')
    version('2.0-5', '049b18caa29529614cd684db3beaec2a')

    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
