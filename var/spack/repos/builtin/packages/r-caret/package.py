# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCaret(RPackage):
    """Misc functions for training and plotting classification and regression
    models."""

    homepage = "https://github.com/topepo/caret/"
    url      = "https://cran.r-project.org/src/contrib/caret_6.0-73.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/caret"

    version('6.0-73', 'ca869e3357b5358f028fb926eb62eb70')
    version('6.0-70', '202d7abb6a679af716ea69fb2573f108')

    depends_on('r@2.10:')

    depends_on('r-lattice@0.20:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-car', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-modelmetrics@1.1.0:', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
