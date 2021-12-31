# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAsyncTimeout(PythonPackage):
    """asyncio-compatible timeout context manager."""

    homepage = "https://github.com/aio-libs/async-timeout"
    url      = "https://github.com/aio-libs/async-timeout/archive/v3.0.1.tar.gz"

    version('4.0.2', sha256='2163e1640ddb52b7a8c80d0a67a08587e5d245cc9c553a74a847056bc2976b15')
    version('4.0.1', sha256='b930cb161a39042f9222f6efb7301399c87eeab394727ec5437924a36d6eef51')
    version('4.0.0', sha256='2116e8c7412929579e1d4e1b3c5fdfe3835c2002a0189451d183148239c05a17')
    version('3.0.1', sha256='d0a7a927ed6b922835e1b014dfcaa9982caccbb25131320582cc660af7c93949')

    depends_on('py-setuptools', type='build')
    depends_on('python@3.5.3:', type=('build', 'run'))
    depends_on('py-typing-extensions@3.6.5:', type=('build', 'run'), when='@4.0.1')
    depends_on('py-typing-extensions@3.6.5:', type=('build', 'run'), when='@4.0.2: ^python@:3.7')
