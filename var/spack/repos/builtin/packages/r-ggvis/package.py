# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGgvis(RPackage):
    """An implementation of an interactive grammar of graphics, taking the best
    parts of 'ggplot2', combining them with the reactive framework from 'shiny'
    and web graphics from 'vega'."""

    homepage = "http://ggvis.rstudio.com/"
    url      = "https://cran.rstudio.com/src/contrib/ggvis_0.4.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ggvis"

    version('0.4.3', '30297d464278a7974fb125bcc7d84e77')
    version('0.4.2', '039f45e5c7f1e0652779163d7d99f922')

    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-shiny', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
