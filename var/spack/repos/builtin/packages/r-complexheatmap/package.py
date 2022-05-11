# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RComplexheatmap(RPackage):
    """Make Complex Heatmaps.

       Complex heatmaps are efficient to visualize associations between
       different sources of data sets and reveal potential patterns. Here the
       ComplexHeatmap package provides a highly flexible way to arrange
       multiple heatmaps and supports various annotation graphics."""

    bioc = "ComplexHeatmap"

    version('2.10.0', commit='170df82a1568e879e4019e0ff6feb0047851684f')
    version('2.6.2', commit='0383bada2c76dc3dde71cf6a625016b619aec4d3')
    version('2.0.0', commit='97863d8ddfe36a52df0149b0b040dc386a03d2e4')
    version('1.20.0', commit='1501ecc92fda07efa3652e41626b21741951ce0f')
    version('1.18.1', commit='be0dd9d666a219c61335efe0dac50b2eed2a8825')
    version('1.17.1', commit='f647c97e556d9e918a17be15883a0b72a91d688f')
    version('1.14.0', commit='0acd8974fb5cedde8cd96efea6dfa39324d25b34')

    depends_on('r@3.1.2:', type=('build', 'run'))
    depends_on('r@3.5.0:', type=('build', 'run'), when='@2.10.0:')
    depends_on('r-circlize@0.3.4:', type=('build', 'run'))
    depends_on('r-circlize@0.4.1:', type=('build', 'run'), when='@1.17.1:')
    depends_on('r-circlize@0.4.5:', type=('build', 'run'), when='@2.0.0:')
    depends_on('r-getoptlong', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
    depends_on('r-clue', type=('build', 'run'), when='@2.0.0:')
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-globaloptions@0.0.10:', type=('build', 'run'))
    depends_on('r-globaloptions@0.1.0:', type=('build', 'run'), when='@1.20.0:')
    depends_on('r-png', type=('build', 'run'), when='@2.0.0:')
    depends_on('r-digest', type=('build', 'run'), when='@2.6.2:')
    depends_on('r-iranges', type=('build', 'run'), when='@2.6.2:')
    depends_on('r-matrixstats', type=('build', 'run'), when='@2.6.2:')
    depends_on('r-foreach', type=('build', 'run'), when='@2.10.0:')
    depends_on('r-doparallel', type=('build', 'run'), when='@2.10.0:')

    depends_on('r-dendextend@1.0.1:', type=('build', 'run'), when='@1.14.0:1.17.1')
    depends_on('r-s4vectors@0.26.1:', type=('build', 'run'), when='@2.6.2')
    depends_on('r-cairo', type=('build', 'run'), when='@2.6.2')
