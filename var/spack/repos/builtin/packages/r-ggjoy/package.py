# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGgjoy(RPackage):
    """Joyplots provide a convenient way of visualizing changes in distributions
    over time or space."""

    homepage = "https://cran.r-project.org/web/packages/ggjoy/index.html"
    url      = "https://cran.r-project.org/src/contrib/ggjoy_0.4.0.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/ggjoy"

    version('0.4.0', 'c63782e2395a9cfc435d08e078e6596b')
    version('0.3.0', '59bd34a846270d43f2eeb1e90b03a127')
    version('0.2.0', '8584cd154e228f8505b324e91d2e50d7')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-ggridges', type=('build', 'run'))
