# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
