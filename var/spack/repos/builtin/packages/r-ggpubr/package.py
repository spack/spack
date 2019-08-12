# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGgpubr(RPackage):
    """ggpubr: 'ggplot2' Based Publication Ready Plots"""

    homepage = "http://www.sthda.com/english/rpkgs/ggpubr"
    url      = "https://cran.r-project.org/src/contrib/ggpubr_0.1.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ggpubr"

    version('0.1.2', '42a5749ae44121597ef511a7424429d1')

    depends_on('r@3.1.0:')
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-ggrepel', type=('build', 'run'))
    depends_on('r-ggsci', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
