# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xsimd(CMakePackage):
    """C++ wrappers for SIMD intrinsics"""

    homepage = "http://quantstack.net/xsimd"
    url      = "https://github.com/QuantStack/xsimd/archive/3.1.0.tar.gz"
    git      = "https://github.com/QuantStack/xsimd.git"

    maintainers = ['ax3l']

    version('develop', branch='master')
    version('7.2.3', sha256='bbc673ad3e9d4523503a4222da05886e086b0e0bd6bd93d03ea3b663c74297b9')
    version('4.0.0', '4186ec94985daa3fc284d9d0d4aa03e8')
    version('3.1.0', '29c1c525116cbda28f610e2bf24a827e')

    depends_on('googletest', type='test')

    # C++14 support
    conflicts('%gcc@:4.8')
    conflicts('%clang@:3.6')
    # untested: conflicts('%intel@:15')
    # untested: conflicts('%pgi@:14')

    def cmake_args(self):
        args = [
            '-DBUILD_TESTS:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF')
        ]

        return args
