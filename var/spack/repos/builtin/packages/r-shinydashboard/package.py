# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RShinydashboard(RPackage):
    """Create Dashboards with 'Shiny'"""

    homepage = "https://cran.r-project.org/package=shinydashboard"
    url      = "https://cran.r-project.org/src/contrib/shinydashboard_0.7.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/shinydashboard"

    version('0.7.0', 'a572695884e3b45320b0ab5a7b364ffd')
    version('0.6.1', '0f6ad0448237e10d53d4d27ade1c6863')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-htmltools@0.2.6:', type=('build', 'run'))
    depends_on('r-shiny@1.0.0:', type=('build', 'run'))
