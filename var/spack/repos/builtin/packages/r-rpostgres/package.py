# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RRpostgres(RPackage):
    """'Rcpp' Interface to 'PostgreSQL'.

    Fully 'DBI'-compliant 'Rcpp'-backed interface to 'PostgreSQL'
    <https://www.postgresql.org/>, an open-source relational database."""

    cran = "RPostgres"

    version('1.4.3', sha256='a5be494a54b6e989fadafdc6ee2dc5c4c15bb17bacea9ad540b175c693331be2')
    version('1.3.1', sha256='f68ab095567317ec32d3faa10e5bcac400aee5aeca8d7132260d4e90f82158ea')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-bit64', type=('build', 'run'))
    depends_on('r-blob@1.2.0:', type=('build', 'run'))
    depends_on('r-dbi@1.1.0:', type=('build', 'run'))
    depends_on('r-hms@0.5.0:', type=('build', 'run'))
    depends_on('r-hms@1.0.0:', type=('build', 'run'), when='@1.4.3:')
    depends_on('r-lubridate', type=('build', 'run'))
    depends_on('r-rcpp@0.11.4.2:', type=('build', 'run'))
    depends_on('r-rcpp@1.0.7:', type=('build', 'run'), when='@1.4.3:')
    depends_on('r-withr', type=('build', 'run'))
    depends_on('r-plogr@0.2.0:', type=('build', 'run'))
    depends_on('postgresql@9.0:')

    depends_on('r-bh', type=('build', 'run'), when='@:1.3.1')
