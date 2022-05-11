# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RSeuratobject(RPackage):
    """Data Structures for Single Cell Data.

    Defines S4 classes for single-cell genomic data and associated information,
    such as dimensionality reduction embeddings, nearest-neighbor graphs, and
    spatially-resolved coordinates. Provides data access methods and R-native
    hooks to ensure the Seurat object is familiar to other R users. See Satija
    R, Farrell J, Gennert D, et al (2015) <doi:10.1038/nbt.3192>, Macosko E,
    Basu A, Satija R, et al (2015) <doi:10.1016/j.cell.2015.05.002>, and Stuart
    T, Butler A, et al (2019) <doi:10.1016/j.cell.2019.05.031> for more
    details."""

    cran = "SeuratObject"

    version('4.0.4', sha256='585261b7d2045193accf817a29e2e3356e731f57c554bed37d232fa49784088c')

    depends_on('r@4.0.0:', type=('build', 'run'))
    depends_on('r-matrix@1.3-3:', type=('build', 'run'))
    depends_on('r-rcpp@1.0.5:', type=('build', 'run'))
    depends_on('r-rlang@0.4.7:', type=('build', 'run'))
    depends_on('r-rcppeigen', type=('build', 'run'))
