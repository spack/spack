# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RGenerics(RPackage):
    """Common S3 Generics not Provided by Base R Methods Related to Model
    Fitting.

    In order to reduce potential package dependencies and conflicts, generics
    provides a number of commonly used S3 generics."""

    cran = "generics"

    version('0.1.1', sha256='a2478ebf1a0faa8855a152f4e747ad969a800597434196ed1f71975a9eb11912')
    version('0.1.0', sha256='ab71d1bdbb66c782364c61cede3c1186d6a94c03635f9af70d926e2c1ac88763')
    version('0.0.2', sha256='71b3d1b719ce89e71dd396ac8bc6aa5f1cd99bbbf03faff61dfbbee32fec6176')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r@3.2:', type=('build', 'run'), when='@0.1.1:')
