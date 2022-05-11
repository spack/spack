# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RRandomglm(RPackage):
    """Random General Linear Model Prediction.

    The package implements a bagging predictor based on general linear
    models."""

    cran = "randomGLM"

    version('1.02-1', sha256='3bf7c1dbdacc68125f8ae3014b9bc546dd3328d04ad015d154781bdf3f1a230c')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
