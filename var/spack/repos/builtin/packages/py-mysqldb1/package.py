# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMysqldb1(PythonPackage):
    """Legacy mysql bindings for python"""
    homepage = "https://github.com/farcepest/MySQLdb1"
    url      = "https://github.com/farcepest/MySQLdb1/archive/MySQLdb-1.2.5.tar.gz"

    version('1.2.5', '332c8f4955b6bc0c79ea15170bf7321b',
            url="https://github.com/farcepest/MySQLdb1/archive/MySQLdb-1.2.5.tar.gz")

    # FIXME: Missing dependency on mysql

    depends_on('py-setuptools', type='build')
