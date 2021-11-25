# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAiohttp(PythonPackage):
    """Supports both client and server side of HTTP protocol.
    Supports both client and server Web-Sockets out-of-the-box and
    avoids Callbacks.  Provides Web-server with middlewares and
    plugable routing."""

    homepage = "https://github.com/aio-libs/aiohttp"
    url      = "https://github.com/aio-libs/aiohttp/archive/v3.6.2.tar.gz"

    version('3.7.4', sha256='d90ace66b55747e49531b13bf0a9c7ae9d1e14f315a56ea6b54c0dc1b6facd6e')
    version('3.6.2', sha256='4ad2d8393843ea0c7b50a93bf04fb1cf20b93c0a5e958de128efcd2e5f8adf80')

    depends_on('py-setuptools', type='build')
    depends_on('python@3.5.3:', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'), when='@3.7:')
    depends_on('py-attrs@17.3.0:', type=('build', 'run'))
    depends_on('py-chardet@2.0:3', type=('build', 'run'))
    depends_on('py-multidict@4.5:4', type=('build', 'run'))
    depends_on('py-multidict@4.5:6', type=('build', 'run'), when='@3.6.3:')
    depends_on('py-async-timeout@3.0:3', type=('build', 'run'))
    depends_on('py-yarl@1.0:1', type=('build', 'run'))
    depends_on('py-idna-ssl@1.0:', type=('build', 'run'), when='^python@:3.6')
    depends_on('py-typing-extensions@3.6.5:', type=('build', 'run'), when='^python@:3.6')
    depends_on('py-typing-extensions@3.6.5:', type=('build', 'run'), when='@3.7.1:')
