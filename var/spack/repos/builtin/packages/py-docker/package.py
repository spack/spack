# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyDocker(PythonPackage):
    """A Python library for the Docker Engine API."""

    homepage = "https://github.com/docker/docker-py"
    pypi = "docker/docker-4.2.1.tar.gz"

    version('4.4.1', sha256='0604a74719d5d2de438753934b755bfcda6f62f49b8e4b30969a4b0a2a8a1220')
    version('4.4.0', sha256='cffc771d4ea1389fc66bc95cb72d304aa41d1a1563482a9a000fba3a84ed5071')
    version('4.3.1', sha256='bad94b8dd001a8a4af19ce4becc17f41b09f228173ffe6a4e0355389eef142f2')
    version('4.3.0', sha256='431a268f2caf85aa30613f9642da274c62f6ee8bae7d70d968e01529f7d6af93')
    version('4.2.2', sha256='26eebadce7e298f55b76a88c4f8802476c5eaddbdbe38dbc6cce8781c47c9b54')
    version('4.2.1', sha256='380a20d38fbfaa872e96ee4d0d23ad9beb0f9ed57ff1c30653cbeb0c9c0964f2')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.4.0:', type=('build', 'run'))
    depends_on('py-websocket-client@0.32.0:', type=('build', 'run'))
    depends_on('py-requests@2.14.2:2.17.999,2.18.1:', type=('build', 'run'))
    depends_on('py-backports-ssl-match-hostname@3.5:', when='^python@:3.4', type=('build', 'run'))
    depends_on('py-ipaddress@1.0.16:', when='^python@:3.2', type=('build', 'run'))
