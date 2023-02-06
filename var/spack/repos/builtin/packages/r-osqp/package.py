# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ROsqp(RPackage):
    """Quadratic Programming Solver using the 'OSQP' Library.

    Provides bindings to the 'OSQP' solver. The 'OSQP' solver is a numerical
    optimization package or solving convex quadratic programs written in 'C'
    and based on the alternating direction method of multipliers. See
    <arXiv:1711.08013> for details."""

    cran = "osqp"

    version("0.6.0.7", sha256="ee6584d02341e3f1d8fab3b2cb93defd6c48d561297d82a6bedb3e7541868203")

    depends_on("r-rcpp@0.12.14:", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))
    depends_on("cmake", type="build")
