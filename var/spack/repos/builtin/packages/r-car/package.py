# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCar(RPackage):
    """Companion to Applied Regression.

    Functions and Datasets to Accompany J. Fox and S. Weisberg, An R Companion
    to Applied Regression, Second Edition, Sage, 2011."""

    cran = "car"

    version('3.0-12', sha256='b899a6efae3842a90a2349d381dbcf4b4ed36bd03108ebe7380e81120e457302')
    version('3.0-11', sha256='b32c927206f515631ff276dbb337b0f22e9b2d851f4abb1d2c272e534c19542c')
    version('3.0-10', sha256='1ce316d2fee9b47c951d25d096be732489a3c9f6fc9e612a1eca2e50fb5925f1')
    version('3.0-3', sha256='fa807cb12f6e7fb38ec534cac4eef54747945c2119a7d51155a2492ad778c36f')
    version('3.0-2', sha256='df59a9ba8fed67eef5ddb8f92f2b41745df715d5695c71d562d7031513f37c50')
    version('2.1-4', sha256='fd39cf1750cb560a66623fea3fa9e6a94fc24e3dc36367aff24df7d0743edb28')
    version('2.1-2', sha256='8cc3e57f172c8782a08960b508906d3201596a21f4b6c1dab8d4e59353093652')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r@3.5.0:', type=('build', 'run'), when='@3.0-3:')
    depends_on('r-cardata@3.0-0:', type=('build', 'run'), when='@3.0:')
    depends_on('r-abind', type=('build', 'run'), when='@3.0:')
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mgcv', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-pbkrtest@0.4-4:', type=('build', 'run'))
    depends_on('r-quantreg', type=('build', 'run'))
    depends_on('r-maptools', type=('build', 'run'), when='@3.0:')
    depends_on('r-rio', type=('build', 'run'), when='@3.0:3.0-11')
    depends_on('r-lme4@1.1-27.1:', type=('build', 'run'), when='@3.0-11:')
    depends_on('r-lme4', type=('build', 'run'), when='@3.0:')
    depends_on('r-nlme', type=('build', 'run'), when='@3.0:')
