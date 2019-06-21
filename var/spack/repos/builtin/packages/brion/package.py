# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Brion(CMakePackage):
    """Blue Brain C++ File IO Library"""

    homepage = "https://github.com/BlueBrain/Brion"
    git = "https://github.com/BlueBrain/Brion.git"
    generator = 'Ninja'

    version('develop', submodules=True)
    version('3.0.0', tag='3.0.0', submodules=True, preferred=True)

    variant('python', default=False, description='Build Python wrapping')

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')

    depends_on('python', type=('build', 'run'), when='+python')
    depends_on('py-numpy', type=('build', 'run'), when='+python')
    depends_on('boost +python', when='+python')

    depends_on('boost@1.65.0')
    depends_on('lunchbox')
    depends_on('vmmlib')
    depends_on('highfive@2.1: +boost ~mpi')
    depends_on('mvdtool ~mpi')

    def cmake_args(self):
        return ['-DDISABLE_SUBPROJECTS=ON']
