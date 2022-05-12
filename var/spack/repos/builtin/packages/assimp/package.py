# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Assimp(CMakePackage):
    """Open Asset Import Library (Assimp) is a portable Open Source library to
    import various well-known 3D model formats in a uniform manner."""

    homepage = "https://www.assimp.org"
    url      = "https://github.com/assimp/assimp/archive/v4.0.1.tar.gz"
    git      = "https://github.com/assimp/assimp.git"

    maintainers = ['wdconinc']

    version('master', branch='master')
    version('5.2.3', sha256='b20fc41af171f6d8f1f45d4621f18e6934ab7264e71c37cd72fd9832509af2a8')
    version('5.2.2', sha256='ad76c5d86c380af65a9d9f64e8fc57af692ffd80a90f613dfc6bd945d0b80bb4')
    version('5.2.1', sha256='c9cbbc8589639cd8c13f65e94a90422a70454e8fa150cf899b6038ba86e9ecff')
    version('5.1.4', sha256='bd32cdc27e1f8b7ac09d914ab92dd81d799c97e9e47315c1f40dcb7c6f7938c6')
    version('5.1.3', sha256='50a7bd2c8009945e1833c591d16f4f7c491a3c6190f69d9d007167aadb175c35')
    version('5.0.1', sha256='11310ec1f2ad2cd46b95ba88faca8f7aaa1efe9aa12605c55e3de2b977b3dbfc')
    version('4.0.1', sha256='60080d8ab4daaab309f65b3cffd99f19eb1af8d05623fff469b9b652818e286e')

    patch('https://patch-diff.githubusercontent.com/raw/assimp/assimp/pull/4203.patch',
          sha256='a227714a215023184536e38b4bc7f8341f635e16bfb3b0ea029d420c29aacd2d',
          when='@5.1:5.2.2')

    variant('shared',  default=True,
            description='Enables the build of shared libraries')

    depends_on('pkgconfig', type='build')
    depends_on('zlib')

    def patch(self):
        filter_file('-Werror', '', 'code/CMakeLists.txt')

    def cmake_args(self):
        args = [
            '-DASSIMP_HUNTER_ENABLED=OFF',
            '-DASSIMP_BUILD_ZLIB=OFF',
            '-DASSIMP_BUILD_MINIZIP=OFF',
            '-DASSIMP_BUILD_TESTS=OFF',
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
        ]
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
        return (None, None, flags)
