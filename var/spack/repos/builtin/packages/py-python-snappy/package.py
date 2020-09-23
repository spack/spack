# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys
import os
import platform


class PyPythonSnappy(PythonPackage):
    """ Python bindings for the snappy google library."""

    homepage = "https://github.com/andrix/python-snappy"
    url      = "https://github.com/andrix/python-snappy/archive/0.5.4.tar.gz"

    version('0.5.4', sha256='92fddfe0ea42c0011227850ee545081975ffe9de5da339d437a178e8015206e9')
    version('0.5.3', sha256='8bbd0d2b5d3b37287cae2460f252f3f3564663e36f769d81bf0bd6d0e6627961')
    version('0.5.2', sha256='d142282a494eaeea26b65cb7867357943095c973ed3c6d048332379fc19ac3bd')
    version('0.5.1', sha256='cf530b5a3e05e220003cdaf09150b56620c12a6e28557def9bbf01989e193931')

    depends_on('python@2.7,3.5:', type=('build', 'run'))
    depends_on('snappy',          type=('build', 'run'))
    depends_on('py-setuptools',   type='build')
    if 'PyPy' in sys.version:
        depends_on('py-cffi',     type=('build', 'run'))

    phases = ['configure', 'build', 'install']

    def configure(self, spec, prefix):
        args = []
        snappy_headers = HeaderList([])
        snappy_headers = spec['snappy'].headers
        snappy_header_dirs = ':'.join(snappy_headers.directories)
        
        self.setup_py('config', '--with-includepath={0}'.format(snappy_header_dirs))
