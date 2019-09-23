# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RVisnetwork(RPackage):
    """Provides an R interface to the 'vis.js' JavaScript charting library. It
    allows an interactive visualization of networks."""

    homepage = "https://github.com/datastorm-open/visNetwork"
    url      = "https://cloud.r-project.org/src/contrib/visNetwork_1.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/visNetwork"

    version('2.0.7', sha256='15ad01636a3a19e1901be6743052805a5b6a9ac1240fb3dab765252b1e865128')
    version('2.0.6', sha256='ec2478e6a2af446569ef2d5210a2bc6b2600bcb7fd9908cef8f8c80b01e9c8aa')
    version('1.0.1', 'dfc9664a5165134d8dbdcd949ad73cf7')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
