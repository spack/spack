# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytestCov(PythonPackage):
    """Pytest plugin for measuring coverage."""

    homepage = "https://github.com/pytest-dev/pytest-cov"
    pypi = "pytest-cov/pytest-cov-2.8.1.tar.gz"

    version('2.11.1', sha256='359952d9d39b9f822d9d29324483e7ba04a3a17dd7d05aa6beb7ea01e359e5f7')
    version('2.11.0', sha256='e90e034cde61dacb1394639a33f449725c591025b182d69752c1dd0bfec639a7')
    version('2.10.1', sha256='47bd0ce14056fdd79f93e1713f88fad7bdcc583dcd7783da86ef2f085a0bb88e')
    version('2.10.0', sha256='1a629dc9f48e53512fcbfda6b07de490c374b0c83c55ff7a1720b3fccff0ac87')
    version('2.9.0',  sha256='b6a814b8ed6247bd81ff47f038511b57fe1ce7f4cc25b9106f1a4b106f1d9322')
    version('2.8.1', sha256='cc6742d8bac45070217169f5f72ceee1e0e55b0221f54bcf24845972d3a47f2b')
    version('2.3.1', sha256='fa0a212283cdf52e2eecc24dd6459bb7687cc29adb60cb84258fab73be8dda0f')

    extends('python', ignore=r'bin/*')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest@3.6:', type=('build', 'run'))
    depends_on('py-coverage@4.4:', type=('build', 'run'))
