# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cgl(AutotoolsPackage):
    """The COIN-OR Cut Generation Library (Cgl) is a collection of cut
    generators that can be used with other COIN-OR packages that make
    use of cuts, such as, among others, the linear solver Clp or the
    mixed integer linear programming solvers Cbc or BCP. Cgl uses the
    abstract class OsiSolverInterface (see Osi) to use or communicate
    with a solver. It does not directly call a solver."""

    homepage = "https://projects.coin-or.org/Cgl"
    url = "https://github.com/coin-or/Cgl/archive/releases/0.60.3.tar.gz"

    depends_on("coinutils")
    depends_on("osi")
    depends_on("clp")

    version("0.60.7", sha256="93b30a80b5d2880c2e72d5877c64bdeaf4d7c1928b3194ea2f88b1aa4517fb1b")
    version("0.60.6", sha256="9e2c51ffad816ab408763d6b931e2a3060482ee4bf1983148969de96d4b2c9ce")
    version("0.60.3", sha256="cfeeedd68feab7c0ce377eb9c7b61715120478f12c4dd0064b05ad640e20f3fb")

    build_directory = "spack-build"
