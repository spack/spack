# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCar(RPackage):
    """Functions and Datasets to Accompany J. Fox and S. Weisberg, An R
    Companion to Applied Regression, Second Edition, Sage, 2011."""

    homepage = "https://r-forge.r-project.org/projects/car/"
    url      = "https://cran.r-project.org/src/contrib/car_2.1-4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/car"

    version('2.1-4', 'a66c307e8ccf0c336ed197c0f1799565')
    version('2.1-2', '0f78ad74ef7130126d319acec23951a0')

    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mgcv', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-pbkrtest', type=('build', 'run'))
    depends_on('r-quantreg', type=('build', 'run'))
