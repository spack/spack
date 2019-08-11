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
    url      = "https://cloud.r-project.org/src/contrib/ggvis_0.4.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggvis"

    version('0.4.4', sha256='1332ea122b768688c8a407a483be80febc4576de0ec8929077738421b27cafaf')
    version('0.4.3', '30297d464278a7974fb125bcc7d84e77')
    version('0.4.2', '039f45e5c7f1e0652779163d7d99f922')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-jsonlite@0.9.11:', type=('build', 'run'))
    depends_on('r-shiny@0.11.1:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-dplyr@0.4.0:', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-htmltools@0.2.4:', type=('build', 'run'))
