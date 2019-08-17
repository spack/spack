# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMaldiquant(RPackage):
    """A complete analysis pipeline for matrix-assisted laser
       desorption/ionization-time-of-flight (MALDI-TOF) and other
       two-dimensional mass spectrometry data. In addition to commonly used
       plotting and processing methods it includes distinctive features,
       namely baseline subtraction methods such as morphological filters
       (TopHat) or the statistics-sensitive non-linear iterative peak-clipping
       algorithm (SNIP), peak alignment using warping functions, handling of
       replicated measurements as well as allowing spectra with different
       resolutions."""

    homepage = "https://cran.r-project.org/package=MALDIquant"
    url      = "https://cran.r-project.org/src/contrib/MALDIquant_1.16.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/MALDIquant"

    version('1.16.4', '83200e7496d05c5a99292e45d2b11c67')

    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-testthat', type=('build', 'run'))
