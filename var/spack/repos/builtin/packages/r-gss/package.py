# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RGss(RPackage):
    """General Smoothing Splines.

    A comprehensive package for structural multivariate function estimation
    using smoothing splines."""

    cran = "gss"

    version('2.2-3', sha256='24306401cf4e5869f8a690eca7e17c044ece83edd66969bd2daf5976272d244b')
    version('2.2-2', sha256='1da4da894378ee730cff9628e8b4d2a0d7dfa344b94e5bce6953e66723c21fe4')
    version('2.1-10', sha256='26c47ecae6a9b7854a1b531c09f869cf8b813462bd8093e3618e1091ace61ee2')
    version('2.1-7', sha256='0405bb5e4c4d60b466335e5da07be4f9570045a24aed09e7bc0640e1a00f3adb')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r@3.0.0:', type=('build', 'run'), when='@2.2-2:')
