# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMatrixmodels(RPackage):
    """Modelling with sparse and dense 'Matrix' matrices, using modular
    prediction and response module classes."""

    homepage = "http://matrix.r-forge.r-project.org/"
    url      = "https://cran.r-project.org/src/contrib/MatrixModels_0.4-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/MatrixModels"

    version('0.4-1', '65b3ab56650c62bf1046a3eb1f1e19a0')

    depends_on('r-matrix', type=('build', 'run'))
