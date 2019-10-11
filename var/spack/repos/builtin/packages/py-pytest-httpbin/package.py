# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytestHttpbin(PythonPackage):
    """Easily test your HTTP library against a local copy of httpbin"""

    homepage = "https://github.com/kevin1024/pytest-httpbin"
    url      = "https://pypi.io/packages/source/p/pytest-httpbin/pytest-httpbin-0.2.3.tar.gz"

    version('0.2.3', sha256='c5b698dfa474ffc9caebcb35e34346b753eb226aea5c2e1b69fefedbcf161bf8')

    extends('python', ignore=r'bin/flask')

    depends_on('py-setuptools', type='build')
    depends_on('py-flask',      type=('build', 'run'))
    depends_on('py-decorator',  type=('build', 'run'))
    depends_on('py-httpbin',    type=('build', 'run'))
    depends_on('py-six',        type=('build', 'run'))
