# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Assimp(CMakePackage):
    """Open Asset Import Library (Assimp) is a portable Open Source library to
    import various well-known 3D model formats in a uniform manner."""

    homepage = "https://www.assimp.org"
    url      = "https://github.com/assimp/assimp/archive/v4.0.1.tar.gz"

    version('4.0.1', '23a6301c728a413aafbfa1cca19ba91f')

    variant('shared',  default=True,
            description='Enables the build of shared libraries')

    depends_on('boost')

    def cmake_args(self):
        args = [
            '-DASSIMP_BUILD_TESTS=OFF',
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in self.spec else 'OFF'),
        ]
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
        return (None, None, flags)
