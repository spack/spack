# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGgridges(RPackage):
    """Ridgeline plots provide a convenient way of visualizing changes in
    distributions over time or space."""

    homepage = "https://cran.r-project.org/web/packages/ggridges/index.html"
    url      = "https://cran.r-project.org/src/contrib/ggridges_0.4.1.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/ggridges"

    version('0.4.1', '21d53b3f7263beb17f629f0ebfb7b67a')
    version('0.4.0', 'da94ed1ee856a7fa5fb87712c84ec4c9')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-ggplot2', type=('build', 'run'))
