# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRpartPlot(RPackage):
    """Plot 'rpart' models. Extends plot.rpart() and text.rpart() in the
    'rpart' package."""

    homepage = "https://cloud.r-project.org/package=rpart.plot"
    url      = "https://cloud.r-project.org/src/contrib/rpart.plot_2.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rpart.plot"

    version('3.0.7', sha256='04e7fcadfa907507b74529c3ecfae4a0c782badf55e87d9c62dbd9a536ea9144')
    version('3.0.6', sha256='1c584290c8f58ded5c3f0638790a0da63408eca3ecd5d5c4d8c46954de9f4b02')
    version('2.1.0', 'fb0f8edfe22c464683ee82aa429136f9')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-rpart@4.1-10:', type=('build', 'run'))
