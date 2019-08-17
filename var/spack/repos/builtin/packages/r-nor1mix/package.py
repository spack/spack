# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNor1mix(RPackage):
    """Onedimensional Normal Mixture Models Classes, for, e.g., density
       estimation or clustering algorithms research and teaching; providing
       the widely used Marron-Wand densities. Efficient random number
       generation and graphics; now fitting to data by ML (Maximum Likelihood)
       or EM estimation."""

    homepage = "https://CRAN.R-project.org/package=nor1mix"
    url      = "https://cran.rstudio.com/src/contrib/nor1mix_1.2-3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/nor1mix"

    version('1.2-3', '60eb5cc1ea6b366f53042087a080b105')
