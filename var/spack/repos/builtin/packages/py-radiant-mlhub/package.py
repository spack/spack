# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRadiantMlhub(PythonPackage):
    """A Python client for Radiant MLHub."""

    homepage = "https://github.com/radiantearth/radiant-mlhub"
    pypi     = "radiant-mlhub/radiant_mlhub-0.2.1.tar.gz"

    maintainers = ['adamjstewart']

    version('0.4.1', sha256='1d95475ec9d4cf460d5201425ba843523b1885a9384b9c1adb81a4a1088adb0f')
    version('0.4.0', sha256='0208881601216f895a1c084a3ca9e5c46b09dbc09dca0447540192e4abb847b1')
    version('0.3.1', sha256='3a5a8e971132d5b4cd9e412c7f6d87894fc588655ae0e93006646927b1ecb902')
    version('0.3.0', sha256='dd66479f12317e7bf366abe8d692841485e9497918c30ab14cd6db9e69ce3dbb')
    version('0.2.2', sha256='0d9f634b7e29c7f7294b81a10cf712ac63251949a9c5a07aa6c64c0d5b77e1ba')
    version('0.2.1', sha256='75a2f096b09a87191238fe557dc64dda8c44156351b4026c784c848c7d84b6fb')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('python@3.7:', when='@0.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-requests@2.25.1:2.25', when='@:0.2', type=('build', 'run'))
    depends_on('py-requests@2.25:2', when='@0.3:', type=('build', 'run'))
    depends_on('py-pystac@0.5.4', when='@:0.2', type=('build', 'run'))
    depends_on('py-pystac@1.1:1', when='@0.3:', type=('build', 'run'))
    depends_on('py-click@7.1.2:7.1', when='@:0.2', type=('build', 'run'))
    depends_on('py-click@7.1.2:8', when='@0.3:', type=('build', 'run'))
    depends_on('py-tqdm@4.56', when='@:0.2', type=('build', 'run'))
    depends_on('py-tqdm@4.56:4', when='@0.3:', type=('build', 'run'))
    depends_on('py-typing-extensions@3.7:', when='@0.4.1: ^python@:3.7', type=('build', 'run'))
