# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRminer(RPackage):
    """Facilitates the use of data mining algorithms in classification and
    regression (including time series forecasting) tasks by presenting a short
    and coherent set of functions."""

    homepage = "http://www3.dsi.uminho.pt/pcortez/rminer.html"
    url      = "https://cloud.r-project.org/src/contrib/rminer_1.4.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rminer"

    version('1.4.2', '7d5d90f4ae030cf647d67aa962412c05')

    depends_on('r-plotrix', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-kknn', type=('build', 'run'))
    depends_on('r-pls', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mda', type=('build', 'run'))
    depends_on('r-rpart', type=('build', 'run'))
    depends_on('r-randomforest', type=('build', 'run'))
    depends_on('r-adabag', type=('build', 'run'))
    depends_on('r-party', type=('build', 'run'))
    depends_on('r-cubist', type=('build', 'run'))
    depends_on('r-kernlab', type=('build', 'run'))
    depends_on('r-e1071', type=('build', 'run'))
    depends_on('r-glmnet', type=('build', 'run'))
    depends_on('r-xgboost', type=('build', 'run'))
