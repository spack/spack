# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScs(RPackage):
    """Splitting Conic Solver.

    Solves convex cone programs via operator splitting. Can solve: linear
    programs ('LPs'), second-order cone programs ('SOCPs'), semidefinite
    programs ('SDPs'), exponential cone programs ('ECPs'), and power cone
    programs ('PCPs'), or problems with any combination of those cones. 'SCS'
    uses 'AMD' (a set of routines for permuting sparse matrices prior to
    factorization) and 'LDL' (a sparse 'LDL' factorization and solve package)
    from 'SuiteSparse'
    (<https://people.engr.tamu.edu/davis/suitesparse.html>)."""

    cran = "scs"

    version("3.0-1", sha256="d6881eeec7282f8bfbf60847327786e7f90299e4b8c0b084d8bd11fec7705913")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("gmake", type="build")
