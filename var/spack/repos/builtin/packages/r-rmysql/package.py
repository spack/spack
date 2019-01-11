# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRmysql(RPackage):
    """Implements 'DBI' Interface to 'MySQL' and 'MariaDB' Databases."""

    homepage = "https://github.com/rstats-db/rmysql"
    url      = "https://cran.r-project.org/src/contrib/RMySQL_0.10.9.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RMySQL"

    version('0.10.9', '3628200a1864ac3005cfd55cc7cde17a')

    depends_on('r-dbi', type=('build', 'run'))
    depends_on('mariadb')
