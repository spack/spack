# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMysqlclient(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://pypi.io/packages/source/m/mysqlclient/mysqlclient-1.4.4.tar.gz"

    version('1.4.4', sha256='9c737cc55a5dc8dd3583a942d5a9b21be58d16f00f5fefca4e575e7d9682e98c')

    depends_on('py-setuptools', type='build')
    depends_on('mysql cxxstd=14')
#
#    def install(self, spec, prefix):
#        # FIXME: Unknown build system
#        make()
#        make('install')
