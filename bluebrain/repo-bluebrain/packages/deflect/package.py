# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Deflect(CMakePackage):
    """A C++ library for streaming pixels to other Deflect-based
       applications."""

    homepage = "https://github.com/BlueBrain/Deflect"
    git = "https://github.com/BlueBrain/Deflect.git"
    generator = 'Ninja'

    version('develop', submodules=True)
    version('1.0.3', tag='1.0.3', submodules=True, preferred=True)

    variant('deflect-qt', default=False, description="Build DeflectQt library")

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')

    depends_on('boost')
    depends_on('qt +opengl', when='+deflect-qt')
    depends_on('qt ~opengl', when='~deflect-qt')

    def cmake_args(self):
        if self.spec.satisfies('@develop'):
            return []
        return [
            "-DCOMMON_WARN_DEPRECATED:BOOL=OFF",
            "-DCOMMON_DISABLE_WERROR:BOOL=ON",
        ]

    def check(self):
        with working_dir(self.build_directory):
            ninja('tests')
