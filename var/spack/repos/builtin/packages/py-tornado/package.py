# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTornado(PythonPackage):
    """Tornado is a Python web framework and asynchronous networking
    library."""

    homepage = "https://github.com/tornadoweb/tornado"
    pypi = "tornado/tornado-6.1.tar.gz"

    version('6.1', sha256='33c6e81d7bd55b468d2e793517c909b139960b6c790a60b7991b9b6b76fb9791')
    version('6.0.3', sha256='c845db36ba616912074c5b1ee897f8e0124df269468f25e4fe21fe72f6edd7a9')
    version('5.1.1', sha256='4e5158d97583502a7e2739951553cbd88a72076f152b4b11b64b9a10c4c49409')
    version('4.4', sha256='3176545b6cb2966870db4def4f646da6ab7a0c19400576969c57279a7561ab02')

    depends_on('py-setuptools', type='build')

    depends_on('python@3.5.2:', when='@6:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-backports-ssl-match-hostname', when='@:4 ^python@:2.7.8', type=('build', 'run'))
    depends_on('py-singledispatch', when='@:5.99 ^python@:3.3', type=('build', 'run'))
    depends_on('py-certifi', when='@:4 ^python@:3.3', type=('build', 'run'))
    depends_on('py-backports-abc@0.4:5.99', when='^python@:3.4', type=('build', 'run'))
    depends_on('py-futures', when='@5:5.99 ^python@:3.1', type=('build', 'run'))
