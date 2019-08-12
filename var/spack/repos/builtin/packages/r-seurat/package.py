# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSeurat(RPackage):
    """Seurat is an R package designed for QC, analysis, and exploration of
    single cell RNA-seq data."""

    homepage = "http://satijalab.org/seurat/"
    url      = "https://cran.r-project.org/src/contrib/Seurat_2.1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/Seurat"

    version('2.1.0', '46427837bb739883f9b7addd08fccee5')
    version('2.0.1', 'a77794891e93b9fa1ef41735fe8424ea')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-gplots', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-caret', type=('build', 'run'))
    depends_on('r-gdata', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-pkgconfig', type=('build', 'run'))
    depends_on('r-plogr', type=('build', 'run'))
    depends_on('r-gridextra', type=('build', 'run'))
    depends_on('r-cowplot', type=('build', 'run'))
    depends_on('r-rocr', type=('build', 'run'))
    depends_on('r-hmisc', type=('build', 'run'))
    depends_on('r-nmf', type=('build', 'run'))
    depends_on('r-irlba', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-fpc', type=('build', 'run'))
    depends_on('r-rcppprogress', type=('build', 'run'))
    depends_on('r-lars', type=('build', 'run'))
    depends_on('r-dtw', type=('build', 'run'))
    depends_on('r-mixtools', type=('build', 'run'))
    depends_on('r-ica', type=('build', 'run'))
    depends_on('r-diffusionmap', type=('build', 'run'))
    depends_on('r-tsne', type=('build', 'run'))
    depends_on('r-rtsne', type=('build', 'run'))
    depends_on('r-ranger', type=('build', 'run'))
    depends_on('r-pbapply', type=('build', 'run'))
    depends_on('r-ggjoy', type=('build', 'run'))
    depends_on('r-plotly', type=('build', 'run'))
    depends_on('r-sdmtools', type=('build', 'run'))
    depends_on('r-tclust', type=('build', 'run'))
    depends_on('r-fnn', type=('build', 'run'))
    depends_on('r-vgam', type=('build', 'run'))
