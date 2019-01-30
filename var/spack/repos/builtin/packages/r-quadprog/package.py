# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RQuadprog(RPackage):
    """This package contains routines and documentation for solving
       quadratic programming problems."""

    homepage = "https://cran.r-project.org/web/packages/quadprog/index.html"
    url      = "https://cran.r-project.org/src/contrib/quadprog_1.5-5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/quadprog"

    version('1.5-5', '8442f37afd8d0b19b12e77d63e6515ad')
