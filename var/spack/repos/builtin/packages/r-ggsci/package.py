# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGgsci(RPackage):
    """ggsci: Scientific Journal and Sci-Fi Themed Color Palettes for
    'ggplot2'"""

    homepage = "https://github.com/road2stat/ggsci"
    url      = "https://cran.r-project.org/src/contrib/ggsci_2.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ggsci"

    version('2.4', '8e5dc2fcf84352cacbb91363e26c7175')

    depends_on('r@3.0.2:')
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-ggplot2@2.0.0:', type=('build', 'run'))
