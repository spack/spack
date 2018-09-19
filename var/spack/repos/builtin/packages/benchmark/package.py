##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
