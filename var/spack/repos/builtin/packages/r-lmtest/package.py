# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLmtest(RPackage):
    """A collection of tests, data sets, and examples for diagnostic checking
    in linear regression models. Furthermore, some generic tools for inference
    in parametric models are provided."""

    homepage = "https://cran.r-project.org/package=lmtest"
    url      = "https://cran.r-project.org/src/contrib/lmtest_0.9-34.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/lmtest"

    version('0.9-34', 'fcdf7286bb5ccc2ca46be00bf25ac2fe')

    depends_on('r-zoo', type=('build', 'run'))
