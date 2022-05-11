# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RWaldo(RPackage):
    """Find Differences Between R Objects.

    Compare complex R objects and reveal the key differences. Designed
    particularly for use in testing packages where being able to quickly
    isolate key differences makes understanding test failures much easier."""

    cran = "waldo"

    version('0.3.1', sha256='ec2c8c1afbc413f8db8b6b0c6970194a875f616ad18e1e72a004bc4497ec019b')
    version('0.2.3', sha256='1fbab22fe9be6ca8caa3df7306c763d7025d81ab6f17b85daaf8bdc8c9455c53')

    depends_on('r-cli', type=('build', 'run'))
    depends_on('r-diffobj', type=('build', 'run'))
    depends_on('r-diffobj@0.3.4:', type=('build', 'run'), when='@0.3.1:')
    depends_on('r-fansi', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-rematch2', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-rlang@0.4.10:', type=('build', 'run'), when='@0.3.1:')
    depends_on('r-tibble', type=('build', 'run'))
