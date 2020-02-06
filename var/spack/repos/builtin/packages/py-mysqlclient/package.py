# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMysqlclient(PythonPackage):
    """Python interface to MySQL"""

    # Note: _mysql module can be imported via "from MySQLdb import _mysql"
    # The documentation is misleading about this.

    homepage = "https://github.com/PyMySQL/mysqlclient-python"
    url      = "https://pypi.io/packages/source/m/mysqlclient/mysqlclient-1.4.4.tar.gz"

    version('1.4.4', sha256='9c737cc55a5dc8dd3583a942d5a9b21be58d16f00f5fefca4e575e7d9682e98c')
    version('1.3.13', sha256='ff8ee1be84215e6c30a746b728c41eb0701a46ca76e343af445b35ce6250644f')

    depends_on('py-setuptools', type='build')
    # Below: cxxstd=17 also works
    depends_on('mysql cxxstd=14')
