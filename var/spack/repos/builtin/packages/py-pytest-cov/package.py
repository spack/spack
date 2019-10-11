# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytestCov(PythonPackage):
    """Pytest plugin for measuring coverage."""

    homepage = "https://github.com/pytest-dev/pytest-cov"
    url      = "https://pypi.io/packages/source/p/pytest-cov/pytest-cov-2.3.1.tar.gz"

    version('2.3.1', sha256='fa0a212283cdf52e2eecc24dd6459bb7687cc29adb60cb84258fab73be8dda0f')

    extends('python', ignore=r'bin/*')

    depends_on('py-setuptools',      type='build')
    depends_on('py-pytest@2.6.0:',   type=('build', 'run'))
    depends_on('py-coverage@3.7.1:', type=('build', 'run'))
