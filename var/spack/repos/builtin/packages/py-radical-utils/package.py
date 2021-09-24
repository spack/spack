# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRadicalUtils(PythonPackage):
    """RADICAL-Utils contains shared code and tools for various
    RADICAL-Cybertools packages."""

    homepage = 'https://radical-cybertools.github.io'
    git      = 'https://github.com/radical-cybertools/radical.utils.git'
    pypi     = 'radical.utils/radical.utils-1.8.0.tar.gz'

    maintainers = ['andre-merzky']

    version('develop', branch='devel')
    version('1.8.0',   sha256='8582c65593f51d394fc263c6354ec5ad9cc7173369dcedfb2eef4f5e8146cf03')
    version('1.6.7',   sha256='552f6c282f960ccd9d2401d686b0b3bfab35dfa94a26baeb2d3b4e45211f05a9')

    version('0.45',    sha256='1333cff1a69532e51d4484fbac3fad6b172d415d2055a3141117c7cf8bdee6c5', deprecated=True)
    version('0.41.1',  sha256='582900e0434f49b69885a89bc65dc787362756e1014d52a4afac0bb61bcaa3ce', deprecated=True)

    depends_on('py-radical-gtod', type=('build', 'run'))

    depends_on('python@3.6:',     type=('build', 'run'))
    depends_on('py-colorama',     type=('build', 'run'))
    depends_on('py-msgpack',      type=('build', 'run'))
    depends_on('py-netifaces',    type=('build', 'run'))
    depends_on('py-ntplib',       type=('build', 'run'))
    depends_on('py-pymongo',      type=('build', 'run'))
    depends_on('py-pyzmq',        type=('build', 'run'))
    depends_on('py-regex',        type=('build', 'run'))
    depends_on('py-setproctitle', type=('build', 'run'))
    depends_on('py-setuptools',   type='build')
