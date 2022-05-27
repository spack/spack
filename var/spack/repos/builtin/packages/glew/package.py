# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Glew(CMakePackage):
    """The OpenGL Extension Wrangler Library."""

    homepage = "http://glew.sourceforge.net/"
    url      = "https://github.com/nigels-com/glew/releases/download/glew-2.1.0/glew-2.1.0.tgz"
    root_cmakelists_dir = "build/cmake"

    version('2.2.0',  sha256='d4fc82893cfb00109578d0a1a2337fb8ca335b3ceccf97b97e5cc7f08e4353e1')
    version('2.1.0',  sha256='04de91e7e6763039bc11940095cd9c7f880baba82196a7765f727ac05a993c95')
    version('2.0.0',  sha256='c572c30a4e64689c342ba1624130ac98936d7af90c3103f9ce12b8a0c5736764')

    depends_on('gl')
    depends_on('glx', when='platform=linux')

    # glu is already forcibly disabled in the CMakeLists.txt.  This prevents
    # it from showing up in the .pc file
    patch('remove-pkgconfig-glu-dep.patch')

    def cmake_args(self):
        args = [
            self.define('BUILD_UTILS', True),
            self.define('GLEW_REGAL', False),
            self.define('GLEW_OSMESA', False),
        ]

        return args
