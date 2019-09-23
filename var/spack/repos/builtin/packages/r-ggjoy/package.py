# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGgjoy(RPackage):
    """Joyplots provide a convenient way of visualizing changes in distributions
    over time or space."""

    homepage = "https://cloud.r-project.org/package=ggjoy"
    url      = "https://cloud.r-project.org/src/contrib/ggjoy_0.4.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggjoy"

    version('0.4.1', sha256='d2f778bc40203d7fbb7c81b40beed8614c36ea10448e911663cc6109aa685504')
    version('0.4.0', 'c63782e2395a9cfc435d08e078e6596b')
    version('0.3.0', '59bd34a846270d43f2eeb1e90b03a127')
    version('0.2.0', '8584cd154e228f8505b324e91d2e50d7')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-ggridges@0.4.0:', type=('build', 'run'))
