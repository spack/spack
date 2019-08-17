# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRvcheck(RPackage):
    """Check latest release version of R and R package (both in 'CRAN',
    'Bioconductor' or 'Github')."""

    homepage = "https://cran.r-project.org/package=rvcheck"
    url      = "https://cran.rstudio.com/src/contrib/rvcheck_0.0.9.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/rvcheck"

    version('0.0.9', '7e9821de754577f94fdcbf7b02a20edc')
