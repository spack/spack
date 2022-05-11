# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RLabelled(RPackage):
    """Manipulating Labelled Data.

    Work with labelled data imported from 'SPSS' or 'Stata' with 'haven' or
    'foreign'. This package provides useful functions to deal with
    "haven_labelled" and "haven_labelled_spss" classes introduced by 'haven'
    package."""

    cran = "labelled"

    version('2.9.0', sha256='36ac0e169ee065a8bced9417efeb85d62e1504a590d4321667d8a6213285d639')
    version('2.7.0', sha256='b1b66b34d3ad682e492fc5bb6431780760576d29dbac40d87bef3c0960054bdb')

    depends_on('r@3.0:', type=('build', 'run'), when='@2.9.0:')
    depends_on('r-haven@2.3.1:', type=('build', 'run'))
    depends_on('r-haven@2.4.1:', type=('build', 'run'), when='@2.9.0:')
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-dplyr@1.0.0:', type=('build', 'run'), when='@2.9.0:')
    depends_on('r-lifecycle', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-vctrs', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'), when='@2.9.0:')
    depends_on('r-tidyr', type=('build', 'run'))

    depends_on('r-pillar', type=('build', 'run'), when='@:2.7.0')
