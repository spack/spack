# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RDeoptimr(RPackage):
    """Differential Evolution Optimization in Pure R.

    Differential Evolution (DE) stochastic algorithms for global optimization
    of problems with and without constraints. The aim is to curate a collection
    of its state-of-the-art variants that (1) do not sacrifice simplicity of
    design, (2) are essentially tuning-free, and (3) can be efficiently
    implemented directly in the R language. Currently, it only provides an
    implementation of the 'jDE' algorithm by Brest et al. (2006)
    <doi:10.1109/TEVC.2006.872133>."""

    cran = "DEoptimR"

    version('1.0-10', sha256='774f7ba0ac9c73aaab4567024b98afdb58098905726e72bceeeb9e380e782ad5')
    version('1.0-8', sha256='846911c1b2561a9fae73a8c60a21a5680963ebb0050af3c1f1147ae9a121e5ef')
