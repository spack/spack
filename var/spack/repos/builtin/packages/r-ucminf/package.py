# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RUcminf(RPackage):
    """General-Purpose Unconstrained Non-Linear Optimization.

    An algorithm for general-purpose unconstrained non-linear optimization.
    The algorithm is of quasi-Newton type with BFGS updating of the inverse
    Hessian and soft line search with a trust region type monitoring of the
    input to the line search algorithm. The interface of 'ucminf' is designed
    for easy interchange with 'optim'."""

    cran = "ucminf"

    version('1.1-4', sha256='a2eb382f9b24e949d982e311578518710f8242070b3aa3314a331c1e1e7f6f07')
