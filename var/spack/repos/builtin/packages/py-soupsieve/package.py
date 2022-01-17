# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySoupsieve(PythonPackage):
    """A modern CSS selector implementation for Beautiful Soup."""

    homepage = "https://github.com/facelessuser/soupsieve"
    pypi = "soupsieve/soupsieve-1.9.3.tar.gz"

    version('2.2.1', sha256='052774848f448cf19c7e959adf5566904d525f33a3f8b6ba6f6f8f26ec7de0cc')
    version('1.9.6', sha256='7985bacc98c34923a439967c1a602dc4f1e15f923b6fcf02344184f86cc7efaa')
    version('1.9.3', sha256='8662843366b8d8779dec4e2f921bebec9afd856a5ff2e82cd419acc5054a1a92')

    depends_on('python@3.6:', when='@2.2:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools@42:', when='@2.2:', type='build')
    depends_on('py-backports-functools-lru-cache', when='^python@:2', type=('build', 'run'))
