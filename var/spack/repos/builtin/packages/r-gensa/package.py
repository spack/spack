# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGensa(RPackage):
    """Generalized Simulated Annealing.

    Performs search for global minimum of a very complex non-linear objective
    function with a very large number of optima."""

    cran = "GenSA"

    version('1.1.7', sha256='9d99d3d0a4b7770c3c3a6de44206811272d78ab94481713a8c369f7d6ae7b80f')

    depends_on('r@2.12.0:', type=('build', 'run'))
