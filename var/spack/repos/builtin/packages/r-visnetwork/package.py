# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RVisnetwork(RPackage):
    """Provides an R interface to the 'vis.js' JavaScript charting library. It
    allows an interactive visualization of networks."""

    homepage = "https://github.com/datastorm-open/visNetwork"
    url      = "https://cran.r-project.org/src/contrib/visNetwork_1.0.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/visNetwork"

    version('1.0.1', 'dfc9664a5165134d8dbdcd949ad73cf7')

    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
