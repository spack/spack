# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Assimp(CMakePackage):
    """Open Asset Import Library (Assimp) is a portable Open Source library to
    import various well-known 3D model formats in a uniform manner."""

    homepage = "https://www.assimp.org"
    url      = "https://github.com/assimp/assimp/archive/v4.0.1.tar.gz"
    git      = "https://github.com/assimp/assimp.git"

    version('master', branch='master')
    version('5.1.4', sha256='bd32cdc27e1f8b7ac09d914ab92dd81d799c97e9e47315c1f40dcb7c6f7938c6')
    version('5.1.3', sha256='50a7bd2c8009945e1833c591d16f4f7c491a3c6190f69d9d007167aadb175c35')
    version('5.0.1', sha256='11310ec1f2ad2cd46b95ba88faca8f7aaa1efe9aa12605c55e3de2b977b3dbfc')
    version('4.0.1', sha256='60080d8ab4daaab309f65b3cffd99f19eb1af8d05623fff469b9b652818e286e')

    variant('shared',  default=True,
            description='Enables the build of shared libraries')

    depends_on('zlib')
    depends_on('boost')

    def cmake_args(self):
        args = [
            '-DASSIMP_BUILD_TESTS=OFF',
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
        ]
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
        return (None, None, flags)
