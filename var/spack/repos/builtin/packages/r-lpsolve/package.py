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


class RLpsolve(RPackage):
    """Lp_solve is freely available (under LGPL 2) software for solving
       linear, integer and mixed integer programs. In this
       implementation we supply a "wrapper" function in C and some R
       functions that solve general linear/integer problems, assignment
       problems, and transportation problems. This version calls
       lp_solve"""

    homepage = "https://cran.r-project.org/web/packages/lpSolve/index.html"
    url      = "https://cran.r-project.org/src/contrib/lpSolve_5.6.13.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/lpSolve"

    version('5.6.13', '8471654d9ae76e0f85ff3449433d4bc1')
