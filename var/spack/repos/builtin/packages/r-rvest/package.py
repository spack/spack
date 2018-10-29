# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRvest(RPackage):
    """Wrappers around the 'xml2' and 'httr' packages to make it easy to
       download, then manipulate, HTML and XML."""

    homepage = "https://github.com/hadley/rvest"
    url      = "https://cran.r-project.org/src/contrib/rvest_0.3.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rvest"

    version('0.3.2', '78c88740850e375fc5da50d37734d1b2')

    depends_on('r-xml2', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-selectr', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
