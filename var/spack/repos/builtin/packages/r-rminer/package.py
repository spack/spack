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


class RRminer(RPackage):
    """Facilitates the use of data mining algorithms in classification and
    regression (including time series forecasting) tasks by presenting a short
    and coherent set of functions."""

    homepage = "http://www3.dsi.uminho.pt/pcortez/rminer.html"
    url      = "https://cran.r-project.org/src/contrib/rminer_1.4.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rminer"

    version('1.4.2', '7d5d90f4ae030cf647d67aa962412c05')

    depends_on('r-plotrix', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-kknn', type=('build', 'run'))
    depends_on('r-pls', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mda', type=('build', 'run'))
    depends_on('r-rpart', type=('build', 'run'))
    depends_on('r-randomforest', type=('build', 'run'))
    depends_on('r-adabag', type=('build', 'run'))
    depends_on('r-party', type=('build', 'run'))
    depends_on('r-cubist', type=('build', 'run'))
    depends_on('r-kernlab', type=('build', 'run'))
    depends_on('r-e1071', type=('build', 'run'))
    depends_on('r-glmnet', type=('build', 'run'))
    depends_on('r-xgboost', type=('build', 'run'))
