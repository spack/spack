# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Rockets(CMakePackage):
    """REST and websockets C++ library"""

    homepage = "https://github.com/BlueBrain/Rockets"
    git = "https://github.com/BlueBrain/Rockets.git"
    generator = 'Ninja'

    version('develop', submodules=True)
    version('1.0.0', tag='1.0.0', submodules=True, preferred=True)

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')
    depends_on('boost', type='build')  # For tests

    depends_on('libwebsockets@3.0.1 +libuv')

    patch('the_forgotten_headers.patch')

    def cmake_args(self):
        return ['-DDISABLE_SUBPROJECTS=ON']
