# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAnimation(RPackage):
    """Provides functions for animations in statistics, covering topics
    in probability theory, mathematical statistics, multivariate statistics,
    non-parametric statistics, sampling survey, linear models, time series,
    computational statistics, data mining and machine learning.
    These functions maybe helpful in teaching statistics and data analysis."""

    homepage = "https://cran.r-project.org/package=animation"
    url = "https://cran.r-project.org/src/contrib/animation_2.5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/animation"

    version('2.5', sha256='b232fef1b318c79710e5e1923d87baba4c85ffe2c77ddb188130e0911d8cb55f')

    extends('r')
    depends_on('r', type=('build', 'run'))
