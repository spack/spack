# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDiptest(RPackage):
    """diptest: Hartigan's Dip Test Statistic for Unimodality - Corrected"""

    homepage = "https://CRAN.R-project.org/package=diptest"
    url      = "https://cran.r-project.org/src/contrib/diptest_0.75-7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/diptest"

    version('0.75-7', '1a4a958fda763f7c99cb485dbe5954ab')
