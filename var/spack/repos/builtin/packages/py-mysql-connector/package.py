# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMysqlConnector(PythonPackage):
    """MySQL Connector/Python is implementing the MySQL Client/Server
    protocol completely in Python. No MySQL libraries are needed, and
    no compilation is necessary to run this Python DB API v2.0
    compliant driver."""

    homepage = "https://github.com/mysql/mysql-connector-python"
    url      = "https://github.com/mysql/mysql-connector-python/archive/8.0.13.tar.gz"
    git      = "https://github.com/mysql/mysql-connector-python.git"

    version('8.0.13', sha256='d4c0834c583cdb90c0aeae90b1917d58355a4bf9b0266c16fd58874a5607f9d4')

    # See not on PythonPackage for why this is type='run', not type='build'
    # Like py-basemap, py-mysql-connector does not depend on py-setuptools
    depends_on('py-setuptools', type='run')
