# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPy(PythonPackage):
    """Library with cross-python path, ini-parsing, io, code, log facilities"""

    homepage = "http://pylib.readthedocs.io/en/latest/"
    url      = "https://pypi.io/packages/source/p/py/py-1.5.4.tar.gz"

    import_modules = [
        'py', 'py._process', 'py._vendored_packages', 'py._path',
        'py._log', 'py._code', 'py._io'
    ]

    version('1.5.4',  '7502d66fa68ea4ae5b61c511cd177d6a')
    version('1.5.3',  '667d37a148ad9fb81266492903f2d880')
    version('1.4.33', '15d7107cbb8b86593bf9afa16e56da65')
    version('1.4.31', '5d2c63c56dc3f2115ec35c066ecd582b')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    def test(self):
        # Tests require pytest, creating a circular dependency
        pass
