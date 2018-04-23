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


class RFnn(RPackage):
    """Cover-tree and kd-tree fast k-nearest neighbor search algorithms and
    related applications including KNN classification, regression and
    information measures are implemented."""

    homepage = "https://cran.r-project.org/web/packages/FNN/index.html"
    url      = "https://cran.r-project.org/src/contrib/FNN_1.1.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/FNN"

    version('1.1',   '8ba8f5b8be271785593e13eae7b8c393')
    version('1.0',   'e9a47dc69d1ba55165be0877b8443fe0')
    version('0.6-4', '1c105df9763ceb7b13989cdbcb542fcc')
    version('0.6-3', 'f0f0184e50f9f30a36ed5cff24d6cff2')
    version('0.6-2', '20648ba934ea32b1b00dafb75e1a830c')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-chemometrics', type=('build', 'run'))
