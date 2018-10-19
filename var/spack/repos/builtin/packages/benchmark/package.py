# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Benchmark(CMakePackage):
    """A microbenchmark support library"""

    homepage = "https://github.com/google/benchmark"
    url      = "https://github.com/google/benchmark/archive/v1.1.0.tar.gz"
    git      = "https://github.com/google/benchmark.git"

    # first properly installed CMake config packages in
    # 1.2.0 release: https://github.com/google/benchmark/issues/363

    version('develop', branch='master')
    version('1.4.0', 'ccfaf2cd93ae20191b94f730b945423e')
    version('1.3.0', '19ce86516ab82d6ad3b17173cf307aac')
    version('1.2.0', '48d0b090cd7a84af2c4a28c8dc963c74')
    version('1.1.0', '66b2a23076cf70739525be0092fc3ae3')
    version('1.0.0', '1474ff826f8cd68067258db75a0835b8')

    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo',
                    'MinSizeRel', 'Coverage'))

    depends_on("cmake@2.8.11:", type="build", when="@:1.1.0")
    depends_on("cmake@2.8.12:", type="build", when="@1.2.0:")

    def cmake_args(self):
        # No need for testing for the install
        args = ["-DBENCHMARK_ENABLE_TESTING=OFF"]
        return args

    def patch(self):
        filter_file(
            r'add_cxx_compiler_flag..fstrict.aliasing.',
            r'##### add_cxx_compiler_flag(-fstrict-aliasing)',
            'CMakeLists.txt'
        )
        filter_file(
            r'add_cxx_compiler_flag..Werror',
            r'##### add_cxx_compiler_flag(-Werror',
            'CMakeLists.txt'
        )
