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


class RXgboost(RPackage):
    """Extreme Gradient Boosting, which is an efficient implementation of
    gradient boosting framework. This package is its R interface. The package
    includes efficient linear model solver and tree learning algorithms. The
    package can automatically do parallel computation on a single machine which
    could be more than 10 times faster than existing gradient boosting
    packages. It supports various objective functions, including regression,
    classification and ranking. The package is made to be extensible, so that
    users are also allowed to define their own objectives easily."""

    homepage = "https://github.com/dmlc/xgboost"
    url      = "https://cran.r-project.org/src/contrib/xgboost_0.6-4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/xgboost"

    version('0.6-4', '86e517e3ce39f8a01de796920f6b425e')
    version('0.4-4', 'c24d3076058101a71de4b8af8806697c')

    depends_on('r@3.3.0:')

    depends_on('r-matrix@1.1-0:', type=('build', 'run'))
    depends_on('r-data-table@1.9.6:', type=('build', 'run'))
    depends_on('r-magrittr@1.5:', type=('build', 'run'))
    depends_on('r-stringi@0.5.2:', type=('build', 'run'))

    # This is not listed as required, but installation fails without it
    # ERROR: dependency 'stringr' is not available for package 'xgboost'
    depends_on('r-stringr', type=('build', 'run'))
