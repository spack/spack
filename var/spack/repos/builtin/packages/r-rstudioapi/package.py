# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRstudioapi(RPackage):
    """Access the RStudio API (if available) and provide informative error
    messages when it's not."""

    homepage = "https://cran.r-project.org/web/packages/rstudioapi/index.html"
    url      = "https://cran.r-project.org/src/contrib/rstudioapi_0.7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rstudioapi"

    version('0.7', 'ee4ab567a7a9fdfac1a6fd01fe38de4a')
    version('0.6', 'fdb13bf46aab02421557e713fceab66b')
    version('0.5', '6ce1191da74e7bcbf06b61339486b3ba')
