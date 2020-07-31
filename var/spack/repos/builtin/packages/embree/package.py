# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Embree(CMakePackage):
    """High-performance ray tracing kernel"""

    homepage = "https://embree.github.io/"
    url = "https://github.com/embree/embree/archive/v3.5.1.tar.gz"
    generator = 'Ninja'

    version('3.11.0', sha256='2ccc365c00af4389aecc928135270aba7488e761c09d7ebbf1bf3e62731b147d')
    version('3.10.0', sha256='378783983262593e1e096d2bb9af5c626d5640aec5ca82a2d60563c1fd865420')
    version('3.9.0', sha256='8ab88965456b70553f62f08dda16dd7d87c6021d5a3a1fd4a7611b90a9f2949d')
    version('3.8.0', sha256='3153e32aca07b38b804353ae2f31ddc8d25201fcffb7b506aa7f2e8f36448fb7')
    version('3.7.0', sha256='2b6300ebe30bb3d2c6e5f23112b4e21a25a384a49c5e3c35440aa6f3c8d9fe84')
    version('3.6.1', sha256='9030ab589cf7134b5995af3639b5e3e9aacaab95d839f619817e2c1348c9b51a')
    version('3.6.0', sha256='a8bdb4420f29c09c31bc094021b3a48305de770f662c37c879e9b54d67f94156')
    version('3.5.2', sha256='245af8820a820af94679fa1d43a05a9c825451be0d603b6165229556adf49517')

    depends_on('cmake@2.8.11:', type='build')
    depends_on('cmake@3.1:', type='build', when='@3.10:')
    depends_on('ispc', type='build')
    depends_on('ninja', type='build')
    depends_on('tbb')

    def cmake_args(self):
        return ['-DEMBREE_TUTORIALS=OFF', '-DEMBREE_IGNORE_INVALID_RAYS=ON']
