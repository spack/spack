# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGrpcio(PythonPackage):
    """HTTP/2-based RPC framework."""

    homepage = "https://grpc.io/"
    url      = "https://pypi.io/packages/source/g/grpcio/grpcio-1.27.2.tar.gz"

    version('1.27.2', sha256='5ae532b93cf9ce5a2a549b74a2c35e3b690b171ece9358519b3039c7b84c887e')
    version('1.25.0', sha256='c948c034d8997526011960db54f512756fb0b4be1b81140a15b4ef094c6594a4')

    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.5.2:', type=('build', 'run'))
    depends_on('py-futures@2.2.0:', when='^python@:3.1', type=('build', 'run'))
    depends_on('py-enum34@1.0.4:', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-cython@0.23:', type='build')
    depends_on('openssl')
    depends_on('zlib')
    depends_on('c-ares')

    def setup_build_environment(self, env):
        env.set('GRPC_PYTHON_BUILD_WITH_CYTHON', True)
        env.set('GRPC_PYTHON_BUILD_SYSTEM_OPENSSL', True)
        env.set('GRPC_PYTHON_BUILD_SYSTEM_ZLIB', True)
        env.set('GRPC_PYTHON_BUILD_SYSTEM_CARES', True)
