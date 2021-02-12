# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyodbc(PythonPackage):
    """A Python DB API 2 module for ODBC. This project provides an up-to-date,
       convenient interface to ODBC using native data types like datetime and
       decimal."""

    homepage = "https://github.com/mkleehammer/pyodbc"
    pypi = "pyodbc/pyodbc-4.0.26.tar.gz"

    version('4.0.30', sha256='852b5deeeb3366af8b4408efed993501708be45d221881bce60c9aac54be726a')
    version('4.0.28', sha256='510643354c4c687ed96bf7e7cec4d02d6c626ecf3e18696f5a0228dd6d11b769')
    version('4.0.27', sha256='2b5628e1bb56e60f22514b058b591a60b013fcfa5c6d712265608cc0e089a2cd')
    version('4.0.26', sha256='e52700b5d24a846483b5ab80acd9153f8e593999c9184ffea11596288fb33de3')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('unixodbc',        type=('build', 'run'))

    phases = ['build_ext', 'install']

    def build_ext_args(self, spec, prefix):

        args = (['--rpath=%s' % (spec['unixodbc'].prefix.lib)])
        return args
