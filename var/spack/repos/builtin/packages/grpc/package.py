# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Grpc(CMakePackage):
    """A high performance, open-source universal RPC framework."""

    maintainers = ['nazavode']

    homepage = "https://grpc.io"
    url      = "https://github.com/grpc/grpc/archive/v1.30.0.tar.gz"

    version('1.35.0', sha256='27dd2fc5c9809ddcde8eb6fa1fa278a3486566dfc28335fca13eb8df8bd3b958')
    version('1.34.1', sha256='c260a1dcdd26a78a9596494a3f41f9594ab5ec3a4d65cba4658bdee2b55ac844')
    version('1.34.0', sha256='7372a881122cd85a7224435a1d58bc5e11c88d4fb98a64b83f36f3d1c2f16d39')
    version('1.33.2', sha256='2060769f2d4b0d3535ba594b2ab614d7f68a492f786ab94b4318788d45e3278a')
    version('1.33.1', sha256='58eaee5c0f1bd0b92ebe1fa0606ec8f14798500620e7444726afcaf65041cb63')
    version('1.33.0', sha256='06a87c5feb7efb979243c054dca2ea52695618c02fde54af8a85d71269f97102')
    version('1.30.0', sha256='419dba362eaf8f1d36849ceee17c3e2ff8ff12ac666b42d3ff02a164ebe090e9')
    version('1.29.1', sha256='0343e6dbde66e9a31c691f2f61e98d79f3584e03a11511fad3f10e3667832a45')
    version('1.29.0', sha256='c0a6b40a222e51bea5c53090e9e65de46aee2d84c7fa7638f09cb68c3331b983')
    version('1.28.2', sha256='4bec3edf82556b539f7e9f3d3801cba540e272af87293a3f4178504239bd111e')
    version('1.28.1', sha256='4cbce7f708917b6e58b631c24c59fe720acc8fef5f959df9a58cdf9558d0a79b')
    version('1.28.0', sha256='d6277f77e0bb922d3f6f56c0f93292bb4cfabfc3c92b31ee5ccea0e100303612')
    version('1.27.0', sha256='3ccc4e5ae8c1ce844456e39cc11f1c991a7da74396faabe83d779836ef449bce')
    version('1.26.0', sha256='2fcb7f1ab160d6fd3aaade64520be3e5446fc4c6fa7ba6581afdc4e26094bd81')
    version('1.25.0', sha256='ffbe61269160ea745e487f79b0fd06b6edd3d50c6d9123f053b5634737cf2f69')
    version('1.24.3', sha256='c84b3fa140fcd6cce79b3f9de6357c5733a0071e04ca4e65ba5f8d306f10f033')
    version('1.23.1', sha256='dd7da002b15641e4841f20a1f3eb1e359edb69d5ccf8ac64c362823b05f523d9')

    variant('shared', default=False,
            description='Build shared instead of static libraries')
    variant('codegen', default=True,
            description='Builds code generation plugins for protobuf '
                        'compiler (protoc)')

    depends_on('protobuf')
    depends_on('openssl')
    depends_on('zlib')
    depends_on('c-ares')
    depends_on('abseil-cpp', when='@1.27:')

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS:Bool={0}'.format(
                'ON' if '+shared' in self.spec else 'OFF'),
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
        if self.spec.satisfies('@1.27.0:'):
            args.append('-DgRPC_ABSL_PROVIDER:String=package')
        return args
