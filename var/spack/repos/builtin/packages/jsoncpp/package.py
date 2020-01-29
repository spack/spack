# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jsoncpp(CMakePackage):
    """JsonCpp is a C++ library that allows manipulating JSON values,
    including serialization and deserialization to and from strings.
    It can also preserve existing comment in unserialization/serialization
    steps, making it a convenient format to store user input files."""

    homepage = "https://github.com/open-source-parsers/jsoncpp"
    url      = "https://github.com/open-source-parsers/jsoncpp/archive/1.7.3.tar.gz"

    version('1.9.1', sha256='c7b40f5605dd972108f503f031b20186f5e5bca2b65cd4b8bd6c3e4ba8126697')
    version('1.9.0', sha256='bdd3ba9ed1f110b3eb57474d9094e90ab239b93b4803b4f9b1722c281e85a4ac')
    version('1.8.4', sha256='c49deac9e0933bcb7044f08516861a2d560988540b23de2ac1ad443b219afdb6')
    version('1.8.3', sha256='3671ba6051e0f30849942cc66d1798fdf0362d089343a83f704c09ee7156604f')
    version('1.8.2', sha256='811f5aee20df2ef0868a73a976ec6f9aab61f4ca71c66eddf38094b2b3078eef')
    version('1.8.1', sha256='858db2faf348f89fdf1062bd3e79256772e897e7f17df73e0624edf004f2f9ac')
    version('1.8.0', sha256='5deb2462cbf0c0121c9d6c9823ec72fe71417e34242e3509bc7c003d526465bc')
    version('1.7.7', sha256='087640ebcf7fbcfe8e2717a0b9528fff89c52fcf69fa2a18cc2b538008098f97')
    version('1.7.6', sha256='07cf5d4f184394ec0a9aa657dd4c13ea682c52a1ab4da2fb176cb2d5501101e8')
    version('1.7.5', sha256='4338c6cab8af8dee6cdfd54e6218bd0533785f552c6162bb083f8dd28bf8fbbe')
    version('1.7.4', sha256='10dcd0677e80727e572a1e462193e51a5fde3e023b99e144b2ee1a469835f769')
    version('1.7.3', sha256='1cfcad14054039ba97c22531888796cb9369e6353f257aacaad34fda956ada53')

    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo',
                    'MinSizeRel', 'Coverage'))

    variant('cxxstd',
            default='default',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('cmake@3.1:', type='build')
    depends_on('python', type='test')

    def cmake_args(self):
        args = ['-DBUILD_SHARED_LIBS=ON']
        cxxstd = self.spec.variants['cxxstd'].value
        if cxxstd != 'default':
            args.append('-DCMAKE_CXX_STANDARD={0}'.format(cxxstd))
        if self.run_tests:
            args.append('-DJSONCPP_WITH_TESTS=ON')
        else:
            args.append('-DJSONCPP_WITH_TESTS=OFF')
        return args
