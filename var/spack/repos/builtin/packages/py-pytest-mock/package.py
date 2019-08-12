# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytestMock(PythonPackage):
    """Thin-wrapper around the mock package for easier use with py.test"""

    homepage = "https://github.com/pytest-dev/pytest-mock"
    url      = "https://pypi.io/packages/source/p/pytest-mock/pytest-mock-1.2.zip"

    version('1.2', 'a7fa820f7bc71698660945836ff93c73')

    extends('python', ignore=r'bin/*')

    depends_on('py-setuptools',  type='build')
    depends_on('py-pytest@2.7:', type=('build', 'run'))
    depends_on('py-mock',        type=('build', 'run'))
