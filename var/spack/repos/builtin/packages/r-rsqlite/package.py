# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRsqlite(RPackage):
    """This package embeds the SQLite database engine in R and provides an
    interface compliant with the DBI package. The source for the SQLite engine
    (version 3.8.6) is included."""

    homepage = "https://cran.rstudio.com/web/packages/RSQLite/index.html"
    url      = "https://cran.r-project.org/src/contrib/RSQLite_2.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RSQLite"

    version('2.0', '63842410e78ccdfc52d4ee97992521d5')

    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-bit64', type=('build', 'run'))
    depends_on('r-blob', type=('build', 'run'))
    depends_on('r-memoise', type=('build', 'run'))
    depends_on('r-pkgconfig', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'run'))
    depends_on('r-plogr', type=('build', 'run'))
