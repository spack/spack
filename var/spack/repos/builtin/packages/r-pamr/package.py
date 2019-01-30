# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPamr(RPackage):
    """Some functions for sample classification in microarrays."""

    homepage = "https://cran.r-project.org/package=pamr"
    url      = "https://cran.rstudio.com/src/contrib/pamr_1.55.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/pamr"

    version('1.55', '108932d006a4de3a178b6f57f5d1a006')
