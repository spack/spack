# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCoda(RPackage):
    """Provides functions for summarizing and plotting the output from
       Markov Chain Monte Carlo (MCMC) simulations, as well as
       diagnostic tests of convergence to the equilibrium distribution
       of the Markov chain."""

    homepage = "https://cran.r-project.org/web/packages/coda/index.html"
    url      = "https://cran.r-project.org/src/contrib/coda_0.19-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/coda"

    version('0.19-1', '0d2aca6a5a3bdae9542708817c1ec001')

    depends_on('r-lattice', type=('build', 'run'))
