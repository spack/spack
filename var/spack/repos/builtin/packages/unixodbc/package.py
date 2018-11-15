# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Unixodbc(AutotoolsPackage):
    """ODBC is an open specification for providing application developers with
    a predictable API with which to access Data Sources. Data Sources include
    SQL Servers and any Data Source with an ODBC Driver."""

    homepage = "http://www.unixodbc.org/"
    url      = "http://www.unixodbc.org/unixODBC-2.3.4.tar.gz"

    version('2.3.4', 'bd25d261ca1808c947cb687e2034be81')

    depends_on('libiconv')
    depends_on('libtool')
