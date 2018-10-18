# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Arrow(CMakePackage):
    """A cross-language development platform for in-memory data.

    This package contains the C++ bindings.
    """

    homepage = "http://arrow.apache.org"
    url      = "https://github.com/apache/arrow/archive/apache-arrow-0.9.0.tar.gz"

    version('0.9.0', 'ebbd36c362b9e1d398ca612f6d2531ec')
    version('0.8.0', '56436f6f61ccc68686b7e0ea30bf4d09')

    depends_on('boost@1.60:')
    depends_on('cmake@3.2.0:', type='build')
    depends_on('flatbuffers@1.8.0 build_type=Release')  # only Release contains flatc
    depends_on('rapidjson')
    depends_on('snappy~shared')
    depends_on('zlib+pic')
    depends_on('zstd+pic')

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'FastDebug', 'Release'))

    root_cmakelists_dir = 'cpp'

    def patch(self):
        """Prevent `-isystem /usr/include` from appearing, since this confuses gcc.
        """
        filter_file(r'(include_directories\()SYSTEM ',
                    r'\1',
                    'cpp/cmake_modules/ThirdpartyToolchain.cmake')

    def cmake_args(self):
        args = [
            "-DARROW_USE_SSE=ON",
            "-DARROW_BUILD_SHARED=ON",
            "-DARROW_BUILD_STATIC=OFF",
            "-DARROW_BUILD_TESTS=OFF",
            "-DARROW_WITH_BROTLI=OFF",
            "-DARROW_WITH_LZ4=OFF",
        ]
        for dep in ('flatbuffers', 'rapidjson', 'snappy', 'zlib', 'zstd'):
            args.append("-D{0}_HOME={1}".format(dep.upper(),
                                                self.spec[dep].prefix))
        args.append("-DZLIB_LIBRARIES={0}".format(self.spec['zlib'].libs))
        return args
