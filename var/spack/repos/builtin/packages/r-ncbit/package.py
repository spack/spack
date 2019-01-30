# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNcbit(RPackage):
    """Making NCBI taxonomic data locally available and searchable as an R
       object."""

    homepage = "https://cran.r-project.org/package=ncbit"
    url      = "https://cran.r-project.org/src/contrib/ncbit_2013.03.29.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ncbit"

    version('2013.03.29', '29582d7e5c8bbf9683c57c4f6ac3e891')
