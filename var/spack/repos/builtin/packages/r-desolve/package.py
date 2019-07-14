# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDesolve(RPackage):
    """Functions that solve initial value problems of a system of first-order
       ordinary differential equations ('ODE'), of partial differential
       equations ('PDE'), of differential algebraic equations ('DAE'), and of
       delay differential equations."""

    homepage = "https://cran.r-project.org/package=deSolve"
    url      = "https://cran.r-project.org/src/contrib/deSolve_1.20.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/deSolve"

    version('1.21', sha256='45c372d458fe4c7c11943d4c409517849b1be6782dc05bd9a74b066e67250c63')
    version('1.20', '85c6a2d8568944ae8eef27ac7c35fb25')
