# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RLimma(RPackage):
    """Linear Models for Microarray Data.

       Data analysis, linear models and differential expression for microarray
       data."""

    bioc = "limma"

    version('3.50.0', commit='657b19bbc33c5c941af79aeb68967bf42ea40e23')
    version('3.46.0', commit='ff03542231827f39ebde6464cdbba0110e24364e')
    version('3.40.6', commit='3ae0767ecf7a764030e7b7d0b1d0f292c0b24055')
    version('3.38.3', commit='77b292eb150cdedaa1db704bcfb01f0bb29e9849')
    version('3.36.5', commit='3148d1cb7eea9c6bdd60351d51abcfd665332d44')
    version('3.34.9', commit='6755278a929f942a49e2441fb002a3ed393e1139')
    version('3.32.10', commit='593edf28e21fe054d64137ae271b8a52ab05bc60')

    depends_on('r@2.3.0:', type=('build', 'run'))
    depends_on('r@3.6.0:', type=('build', 'run'), when='@3.40.6:')
