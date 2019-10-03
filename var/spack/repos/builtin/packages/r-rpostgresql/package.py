# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRpostgresql(RPackage):
    """Database interface and PostgreSQL driver for R This package provides a
    Database Interface (DBI) compliant driver for R to access PostgreSQL
    database systems. In order to build and install this package from source,
    PostgreSQL itself must be present your system to provide PostgreSQL
    functionality via its libraries and header files. These files are provided
    as postgresql-devel package under some Linux distributions. On Microsoft
    Windows system the attached libpq library source will be used. A wiki and
    issue tracking system for the package are available at Google Code at
    https://code.google.com/p/rpostgresql/."""

    homepage = "https://code.google.com/p/rpostgresql/"
    url      = "https://cloud.r-project.org/src/contrib/RPostgreSQL_0.4-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RPostgreSQL"

    version('0.6-2', sha256='080118647208bfa2621bcaac0d324891cc513e07618fa22e3c50ec2050e1b0d5')
    version('0.4-1', 'e7b22e212afbb2cbb88bab937f93e55a')

    depends_on('r@2.9.0:', type=('build', 'run'))
    depends_on('r-dbi@0.3:', type=('build', 'run'))
    depends_on('postgresql')
