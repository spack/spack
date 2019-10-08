# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTornado(PythonPackage):
    """Tornado is a Python web framework and asynchronous networking
    library."""
    homepage = "https://github.com/tornadoweb/tornado"
    url      = "https://github.com/tornadoweb/tornado/archive/v6.0.3.tar.gz"

    version('6.0.3',   sha256='a97ac3b8c95867e534b48cb6fbbf156f5ca5b20c423bb06894c17b240d7a18fc')
    version('6.0.2',   sha256='a5f744b5516d8a94171db5e02096dbd5169a5df2034a2b562a150b53b6d4db70')
    version('6.0.1',   sha256='02e41f5d7a55b78e002675ccdbbd181a0ce9b5f857b5a717227521f10a11c583')
    version('6.0.0b1', sha256='54d20962d0bc8c6a05792c39349de9ad5d8f51605e1c071cc68a0241622bfa18')
    version('6.0.0',   sha256='759ab1672d1d8b903fef6b4c1b9594a9f67f4ef834a68d1ef18937a3d5f22f74')
    version('5.1.1',   sha256='a1da335a2978b9a8c3544cab10076d799442d7988ed0b4f2be035fe4388ca8dd')
    version('5.1.0b1', sha256='a86b15f8a1952ec8ccc1f6967a5b1444658be6459eb763c41c0de747a54216dc')
    version('5.1.0',   sha256='612679a0c5eabb88a172f35ba58921b445935c83cf440f58dbb3048d958739c9')
    version('5.0.2',   sha256='1f7489e263c80cdc294ba0afe54d8745f767c3b1701600fc38503458d01be62e')
    version('5.0.1',   sha256='f0cba59528eca427880338f120fa0e8f7a65776ec24359a65b3cfb3b5ea8d96f')
    version('4.4.0', 'c28675e944f364ee96dda3a8d2527a87ed28cfa3')

    depends_on('py-setuptools', type='build')

    # requirements from setup.py
    depends_on('python@3.5:', when='@6:', type=('build', 'run'))
    depends_on('py-backports-ssl-match-hostname', when='^python@:2.7.8', type=('build', 'run'))
    depends_on('py-singledispatch', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-certifi', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-backports-abc@0.4:', when='^python@:3.4', type=('build', 'run'))
