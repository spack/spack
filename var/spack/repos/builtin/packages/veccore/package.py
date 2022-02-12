# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Veccore(CMakePackage, CudaPackage):
    """SIMD Vectorization Library for VecGeom and GeantV"""

    homepage = "https://gitlab.cern.ch/VecGeom/VecCore"
    url = "https://gitlab.cern.ch/VecGeom/VecCore/-/archive/v0.6.0/VecCore-v0.6.0.tar.gz"
    git = "https://gitlab.cern.ch/VecGeom/VecCore.git"

    maintainers = ['drbenmorgan', 'sethrj']

    version('master', branch='master')
    # Note: 0.8.0 tag is currently unofficial but it is needed explicitly for
    # VecGeom 1.1.18
    version('0.8.0', commit='6038e4732394413b0661fede171c77e75ed9bd71')
    version('0.7.0', sha256='8aa97e19c455382f1a3dae07ffa5e49f2982f09e75b25a3f98d7b94cd43d6001')
    version('0.6.0', sha256='e7ff874ba2a8201624795cbe11c84634863e4ac7da691a936772d4202ef54413')
    version('0.5.2', sha256='0cfaa830b9d10fb9df4ced5208a742623da08520fea5949461fe81637a27db15')
    version('0.5.1', sha256='5ef3a8d8692d8f82641aae76b58405b8b3a1539a8f21b23d66a5df8327eeafc4')
    version('0.5.0', sha256='aba3e0217c0cd829290c9fe63f1db865838aa25312ae0a09effdcb186f7771be')
    version('0.4.2', sha256='4a3bb944bce63dc1dc9757ba53624b822e1aff5ed088d542039a20227ed2b715')

    variant('cxxstd',
            default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')
    conflicts('cxxstd=14', when='@:0.5')
    conflicts('cxxstd=17', when='@:0.5')

    def cmake_args(self):
        define = CMakePackage.define
        return [
            define('VC', False),
            define('UMESIMD', False),
            self.define_from_variant('CMAKE_CXX_STANDARD', 'cxxstd'),
            self.define_from_variant('CUDA'),
        ]
