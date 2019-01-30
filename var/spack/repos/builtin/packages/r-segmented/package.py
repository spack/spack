# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSegmented(RPackage):
    """Given a regression model, segmented 'updates' the model by adding
    one or more segmented (i.e., piecewise-linear) relationships. Several
    variables with multiple breakpoints are allowed."""

    homepage = "https://CRAN.R-project.org/package=segmented"
    url      = "https://cran.r-project.org/src/contrib/segmented_0.5-1.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/segmented"

    version('0.5-2.2', '1511ec365aea289d5f0a574f6d10d2d6')
    version('0.5-1.4', 'f9d76ea9e22ef5f40aa126b697351cae')
