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


class RSn(RPackage):
    """Build and manipulate probability distributions of the skew-normal
    family and some related ones, notably the skew-t family, and provide
    related statistical methods for data fitting and diagnostics, in the
    univariate and the multivariate case."""

    homepage = "https://cran.r-project.org/web/packages/sn/index.html"
    url      = "https://cran.r-project.org/src/contrib/sn_1.5-0.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/sn"

    version('1.5-0', 'a3349773be950199d7f4c17954be56d1')
    version('1.4-0', 'cfa604317ea54224b06abd1cec179375')
    version('1.3-0', '84d02ba2ab5ca6f3644626013e7ce36d')
    version('1.2-4', 'bf3a47b05016326e910fdb4cc4967e4d')
    version('1.2-3', '290ae511d974a6beb4c3c79c0106858f')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-mnormt', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
