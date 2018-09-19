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


class RForecast(RPackage):
    """Methods and tools for displaying and analysing univariate time
    series forecasts including exponential smoothing via state space
    models and automatic ARIMA modelling."""

    homepage = "https://cran.r-project.org/package=forecast"
    url      = "https://cran.r-project.org/src/contrib/forecast_8.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/forecast"

    version('8.2', '3ef095258984364c100b771b3c90d15e')

    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-fracdiff', type=('build', 'run'))
    depends_on('r-tseries', type=('build', 'run'))
    depends_on('r-lmtest', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-timedate', type=('build', 'run'))
    depends_on('r-rcpparmadillo', type=('build', 'run'))
