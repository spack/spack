# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGgrepel(RPackage):
    """ggrepel: Repulsive Text and Label Geoms for 'ggplot2'"""

    homepage = "http://github.com/slowkow/ggrepel"
    url      = "https://cran.r-project.org/src/contrib/ggrepel_0.6.5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ggrepel"

    version('0.6.5', '7e2732cd4840efe2dc9e4bc689cf1ee5')

    depends_on('r@3.0.0:')
    depends_on('r-ggplot2@2.0.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-scales@0.3.0:', type=('build', 'run'))
