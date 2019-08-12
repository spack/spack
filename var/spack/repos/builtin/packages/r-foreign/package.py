# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RForeign(RPackage):
    """Functions for reading and writing data stored by some versions of Epi
    Info, Minitab, S, SAS, SPSS, Stata, Systat and Weka and for reading and
    writing some dBase files."""

    homepage = "https://cran.r-project.org/web/packages/foreign/index.html"
    url      = "https://cran.r-project.org/src/contrib/foreign_0.8-66.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/foreign"

    version('0.8-66', 'ff12190f4631dca31e30ca786c2c8f62')
