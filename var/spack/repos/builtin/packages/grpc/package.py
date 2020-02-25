# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Grpc(CMakePackage):
    """A high performance, open-source universal RPC framework."""

    homepage = "https://grpc.io"
    url      = "https://github.com/grpc/grpc/archive/v1.27.0.tar.gz"

    version('1.27.0', sha256='3ccc4e5ae8c1ce844456e39cc11f1c991a7da74396faabe83d779836ef449bce')
    version('1.26.0', sha256='2fcb7f1ab160d6fd3aaade64520be3e5446fc4c6fa7ba6581afdc4e26094bd81')
    version('1.25.0', sha256='ffbe61269160ea745e487f79b0fd06b6edd3d50c6d9123f053b5634737cf2f69')
    version('1.24.3', sha256='c84b3fa140fcd6cce79b3f9de6357c5733a0071e04ca4e65ba5f8d306f10f033')
    version('1.23.1', sha256='dd7da002b15641e4841f20a1f3eb1e359edb69d5ccf8ac64c362823b05f523d9')

    variant('codegen', default=True,
            description='Builds code generation plugins for protobuf '
                        'compiler (protoc)')

    depends_on('protobuf')
    depends_on('openssl')
    depends_on('zlib')
    depends_on('c-ares')

    def cmake_args(self):
        args = [
            '-DgRPC_BUILD_CODEGEN:Bool={0}'.format(
                'ON' if '+codegen' in self.spec else 'OFF'),
            '-DgRPC_BUILD_CSHARP_EXT:Bool=OFF',
            '-DgRPC_INSTALL:Bool=ON',
            # Tell grpc to skip vendoring and look for deps via find_package:
            '-DgRPC_CARES_PROVIDER:String=package',
            '-DgRPC_ZLIB_PROVIDER:String=package',
            '-DgRPC_SSL_PROVIDER:String=package',
            '-DgRPC_PROTOBUF_PROVIDER:String=package',
            '-DgRPC_USE_PROTO_LITE:Bool=OFF',
            '-DgRPC_PROTOBUF_PACKAGE_TYPE:String=CONFIG',
            # Disable tests:
            '-DgRPC_BUILD_TESTS:BOOL=OFF',
            '-DgRPC_GFLAGS_PROVIDER:String=none',
            '-DgRPC_BENCHMARK_PROVIDER:String=none',
        ]
        return args
