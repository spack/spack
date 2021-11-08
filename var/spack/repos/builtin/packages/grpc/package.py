# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Grpc(CMakePackage):
    """A high performance, open-source universal RPC framework."""

    maintainers = ['nazavode']

    homepage = "https://grpc.io"
    url      = "https://github.com/grpc/grpc/archive/v1.39.0.tar.gz"

    version('1.39.0', sha256='b16992aa1c949c10d5d5ce2a62f9d99fa7de77da2943e643fb66dcaf075826d6')
    version('1.38.1', sha256='f60e5b112913bf776a22c16a3053cc02cf55e60bf27a959fd54d7aaf8e2da6e8')
    version('1.38.0', sha256='abd9e52c69000f2c051761cfa1f12d52d8b7647b6c66828a91d462e796f2aede')
    version('1.37.1', sha256='acf247ec3a52edaee5dee28644a4e485c5e5badf46bdb24a80ca1d76cb8f1174')
    version('1.37.0', sha256='c2dc8e876ea12052d6dd16704492fd8921df8c6d38c70c4708da332cf116df22')
    version('1.36.4', sha256='8eb9d86649c4d4a7df790226df28f081b97a62bf12c5c5fe9b5d31a29cd6541a')
    version('1.36.3', sha256='bb6de0544adddd54662ba1c314eff974e84c955c39204a4a2b733ccd990354b7')
    version('1.33.1', sha256='58eaee5c0f1bd0b92ebe1fa0606ec8f14798500620e7444726afcaf65041cb63')
    version('1.32.0', sha256='f880ebeb2ccf0e47721526c10dd97469200e40b5f101a0d9774eb69efa0bd07a')
    version('1.31.0', sha256='1236514199d3deb111a6dd7f6092f67617cd2b147f7eda7adbafccea95de7381')
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
    variant('cxxstd',
            default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('protobuf')
    depends_on('openssl')
    depends_on('zlib')
    depends_on('c-ares')
    depends_on('abseil-cpp', when='@1.27:')
    depends_on('re2+pic', when='@1.33.1:')

    def cmake_args(self):
        args = [
            define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            define_from_variant('gRPC_BUILD_CODEGEN', 'codegen'),
            define_from_variant('CMAKE_CXX_STANDARD', 'cxxstd'),
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
        if self.spec.satisfies('@1.33.1:'):
            args.append('-DgRPC_RE2_PROVIDER:String=package')
        return args
