# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGgally(RPackage):
    """The R package 'ggplot2' is a plotting system based on the grammar of
       graphics. 'GGally' extends 'ggplot2' by adding several functions to
       reduce the complexity of combining geometric objects with transformed
       data. Some of these functions include a pairwise plot matrix, a two
       group pairwise plot matrix, a parallel coordinates plot, a survival
       plot, and several functions to plot networks."""

    homepage = "https://cran.r-project.org/package=GGally"
    url      = "https://cran.r-project.org/src/contrib/GGally_1.3.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/GGally"

    version('1.3.2', 'efe58133ba8431198af7afb6bcb76264')

    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-gtable', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-progress', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-reshape', type=('build', 'run'))
