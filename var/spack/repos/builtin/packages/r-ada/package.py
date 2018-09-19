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


class RAda(RPackage):
    """Performs discrete, real, and gentle boost under both exponential
    and logistic loss on a given data set."""

    homepage = "https://cran.r-project.org/web/packages/ada/index.html"
    url      = "https://cran.r-project.org/src/contrib/ada_2.0-5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ada"

    version('2.0-5', '25ac0dc2650fba9e19f3d15c7c6721c1')

    depends_on('r-rpart', type=('build', 'run'))
