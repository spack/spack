# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    git      = "https://github.com/apache/arrow.git"

    version('0.17.1', tag='apache-arrow-0.17.1')
    version('0.15.0', sha256='be92f0169747c99282da71e951a8fbe72fef2058ee95a207ad484b5307b5003c')
    version('0.14.1', sha256='69d9de9ec60a3080543b28a5334dbaf892ca34235b8bd8f8c1c01a33253926c1')
    version('0.14.0', sha256='e6444a73cc7987245e0c89161e587337469d26a518c9af1e6d7dba47027e0cd1')
    version('0.13.0', sha256='380fcc51f0bf98e13148300c87833e734cbcd7b74dddc4bce93829e7f7e4208b')
    version('0.12.1', sha256='aae68622edc3dcadaa16b2d25ae3f00290d5233100321993427b03bcf5b1dd3b')
    version('0.11.0', sha256='0ac629a7775d86108e403eb66d9f1a3d3bdd6b3a497a86228aa4e8143364b7cc')
    version('0.9.0', sha256='65f89a3910b6df02ac71e4d4283db9b02c5b3f1e627346c7b6a5982ae994af91')
    version('0.8.0', sha256='c61a60c298c30546fc0b418a35be66ef330fb81b06c49928acca7f1a34671d54')

    depends_on('boost@1.60:')
    depends_on('cmake@3.2.0:', type='build')
    depends_on('flatbuffers build_type=Release')  # only Release contains flatc
    depends_on('gettext', when='+python')
    depends_on('python', when='+python')
    depends_on('py-numpy', when='+python')
    depends_on('rapidjson')
    depends_on('snappy~shared')
    depends_on('zlib+pic')
    depends_on('zstd+pic')

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'FastDebug', 'Release'))
    variant('python', default=False, description='Build Python interface')
    variant('parquet', default=False, description='Build Parquet interface')

    root_cmakelists_dir = 'cpp'

    def patch(self):
        """Prevent `-isystem /usr/include` from appearing, since this confuses gcc.
        """
        filter_file(r'(include_directories\()SYSTEM ',
                    r'\1',
                    'cpp/cmake_modules/ThirdpartyToolchain.cmake')

    def cmake_args(self):
        args = [
            "-DBoost_DEBUG=ON",
            "-DARROW_USE_SSE=ON",
            "-DARROW_BUILD_SHARED=ON",
            "-DARROW_BUILD_STATIC=ON",
            "-DARROW_BUILD_TESTS=OFF",
            "-DARROW_WITH_BROTLI=OFF",
            "-DARROW_WITH_LZ4=OFF",
            "-DARROW_WITH_SNAPPY=ON",
        ]
        if self.spec.satisfies('+python'):
            args.append("-DARROW_PYTHON:BOOL=ON")
        if self.spec.satisfies('+parquet'):
            args.append("-DARROW_PARQUET:BOOL=ON")
        for dep in ('flatbuffers', 'rapidjson', 'snappy', 'zlib', 'zstd'):
            args.append("-D{0}_HOME={1}".format(dep.upper(),
                                                self.spec[dep].prefix))
        args.append("-DZLIB_LIBRARIES={0}".format(self.spec['zlib'].libs))
        return args
