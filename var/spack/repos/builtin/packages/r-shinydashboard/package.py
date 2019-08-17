# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RShinydashboard(RPackage):
    """Create Dashboards with 'Shiny'"""

    homepage = "https://cloud.r-project.org/package=shinydashboard"
    url      = "https://cloud.r-project.org/src/contrib/shinydashboard_0.7.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/shinydashboard"

    version('0.7.1', sha256='51a49945c6b8a684111a2ba4b2a5964e3a50610286ce0378e37ae02316620a4e')
    version('0.7.0', 'a572695884e3b45320b0ab5a7b364ffd')
    version('0.6.1', '0f6ad0448237e10d53d4d27ade1c6863')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-htmltools@0.2.6:', type=('build', 'run'))
    depends_on('r-shiny@1.0.0:', type=('build', 'run'))
    depends_on('r-promises', when='@0.7.1:', type=('build', 'run'))
