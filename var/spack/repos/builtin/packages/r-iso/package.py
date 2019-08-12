# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIso(RPackage):
    """Linear order and unimodal order (univariate) isotonic regression;
    bivariate isotonic regression with linear order on both variables."""

    homepage = "https://cran.r-project.org/package=Iso"
    url      = "https://cran.rstudio.com/src/contrib/Iso_0.0-17.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/Iso"

    version('0.0-17', 'bf99821efb6a44fa75fdbf5e5c4c91e4')
