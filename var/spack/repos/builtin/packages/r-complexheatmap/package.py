# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RComplexheatmap(RPackage):
    """Complex heatmaps are efficient to visualize associations between
       different sources of data sets and reveal potential structures. Here
       the ComplexHeatmap package provides a highly flexible way to arrange
       multiple heatmaps and supports self-defined annotation graphics."""

    homepage = "https://bioconductor.org/packages/ComplexHeatmap/"
    git      = "https://git.bioconductor.org/packages/ComplexHeatmap.git"

    version('1.14.0', commit='0acd8974fb5cedde8cd96efea6dfa39324d25b34')

    depends_on('r-circlize', type=('build', 'run'))
    depends_on('r-getoptlong', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-dendextend', type=('build', 'run'))
    depends_on('r-globaloptions', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.14.0')
