# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSeurat(RPackage):
    """Seurat is an R package designed for QC, analysis, and exploration of
    single cell RNA-seq data."""

    homepage = "http://satijalab.org/seurat/"
    url      = "https://cloud.r-project.org/src/contrib/Seurat_2.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Seurat"

    version('3.0.2', sha256='16df5dec6b41d49320c5bf5ce30eb3b7dedeea69b054b55b77528f2f2b7bce04')
    version('3.0.1', sha256='8c467bdbfdb9aff51bde6a897ff98a7389941f688639d8f1d36c71dde076a257')
    version('2.1.0', '46427837bb739883f9b7addd08fccee5')
    version('2.0.1', 'a77794891e93b9fa1ef41735fe8424ea')

    depends_on('r@3.4.0:')
    depends_on('r-ggplot2@3.0.0:', type=('build', 'run'))
    depends_on('r-gplots', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-reshape2', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-tidyr', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-caret', when='@:2.3.2', type=('build', 'run'))
    depends_on('r-gdata', when='@:2.3.2', type=('build', 'run'))
    depends_on('r-gridextra', when='@:2.3.0', type=('build', 'run'))
    depends_on('r-cowplot', type=('build', 'run'))
    depends_on('r-rocr', type=('build', 'run'))
    depends_on('r-hmisc', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-nmf', when='@:2.2.0', type=('build', 'run'))
    depends_on('r-irlba', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-fpc', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-rcppprogress', type=('build', 'run'))
    depends_on('r-lars', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-dtw', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-mixtools', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-ica', type=('build', 'run'))
    depends_on('r-diffusionmap', when='@:2.3.3', type=('build', 'run'))
    depends_on('r-tsne', type=('build', 'run'))
    depends_on('r-rtsne', type=('build', 'run'))
    depends_on('r-ranger', when='@:2.3.2', type=('build', 'run'))
    depends_on('r-pbapply', type=('build', 'run'))
    depends_on('r-ggjoy', when='@:2.1.0', type=('build', 'run'))
    depends_on('r-plotly', type=('build', 'run'))
    depends_on('r-sdmtools', type=('build', 'run'))
    depends_on('r-tclust', when='@:2.3.2', type=('build', 'run'))
    depends_on('r-fnn', when='@:2.3.2', type=('build', 'run'))
    depends_on('r-vgam', when='@:2.3.2', type=('build', 'run'))
    depends_on('r-matrix@1.2.14:', type=('build', 'run'))
    depends_on('r-colorbrewer', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('r-rcppeigen', type=('build', 'run'))
    depends_on('r-ggridges', when='@2.2.0:', type=('build', 'run'))
    depends_on('r-e1071', when='@:2.0.1', type=('build', 'run'))
    depends_on('r-compositions', when='@:2.0.1', type=('build', 'run'))
    depends_on('r-nmof', when='@:2.0.1', type=('build', 'run'))
    depends_on('r-metap', when='@2.2.1:', type=('build', 'run'))
    depends_on('r-cluster', when='@2.3.0:', type=('build', 'run'))
    depends_on('r-fitdistrplus', when='@2.3.0:', type=('build', 'run'))
    depends_on('r-png', when='@2.3.0:', type=('build', 'run'))
    depends_on('r-lmtest', when='@2.3.0:', type=('build', 'run'))
    depends_on('r-rann', when='@2.3.0:', type=('build', 'run'))
    depends_on('r-reticulate', when='@2.3.1:', type=('build', 'run'))
    depends_on('r-stringr', when='@:2.3.2', type=('build', 'run'))
    depends_on('r-dplyr', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-httr', when='@2.3.4:', type=('build', 'run'))
    depends_on('r-dosnow', when='@2.3.0:2.3.4', type=('build', 'run'))
    depends_on('r-foreach', when='@2.3.0:2.3.4', type=('build', 'run'))
    depends_on('r-hdf5r', when='@2.3.2:2.3.4', type=('build', 'run'))
    depends_on('r-future', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-future-apply', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-ggrepel', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-kernsmooth', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-rlang', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-rsvd', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-scales', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-sctransform@0.2.0:', when='@3.0.0:', type=('build', 'run'))
    depends_on('java', when='@:2.3.3')
