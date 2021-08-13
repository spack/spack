# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRadicalSaga(PythonPackage):
    """RADICAL-SAGA (RS) implements the interface specification of the Open
    Grid Forum (OGF) Simple API for Grid Applications (SAGA) standard. RS works
    as a light-weight access layer for distributed computing infrastructures,
    providing adaptors for different middleware systems and services."""

    homepage = 'https://radical-cybertools.github.io'
    git      = 'https://github.com/radical-cybertools/radical.saga.git'
    pypi     = 'radical.saga/radical.saga-1.6.10.tar.gz'

    maintainers = ['andre-merzky']

    version('develop', branch='devel')
    version('1.6.10',  sha256='8fe7e281e9f81234f34f5c7c7986871761e9e37230d2a874c65d18daeccd976a')
    version('1.6.8',   sha256='d5e9f95a027087fb637cef065ff3af848e5902e403360189e36c9aa7c3f6f29b')

    depends_on('py-radical-utils',   type=('build', 'run'))

    depends_on('python@3.6:',        type=('build', 'run'))
    depends_on('py-apache-libcloud', type=('build', 'run'))
    depends_on('py-parse',           type=('build', 'run'))
    depends_on('py-setuptools',      type='build')
