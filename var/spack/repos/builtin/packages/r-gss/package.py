# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGss(RPackage):
    """A comprehensive package for structural multivariate function
    estimation using smoothing splines."""

    homepage = "https://cran.r-project.org/package=gss"
    url      = "https://cran.rstudio.com/src/contrib/gss_2.1-7.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/gss"

    version('2.1-7', '4a6bd96339d22b40c932895b64504fb2')
