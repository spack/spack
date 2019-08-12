# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRpartPlot(RPackage):
    """Plot 'rpart' models. Extends plot.rpart() and text.rpart() in the
    'rpart' package."""

    homepage = "https://cran.r-project.org/package=rpart.plot"
    url      = "https://cran.r-project.org/src/contrib/rpart.plot_2.1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rpart.plot"

    version('2.1.0', 'fb0f8edfe22c464683ee82aa429136f9')

    depends_on('r-rpart@4.1-0:', type=('build', 'run'))
