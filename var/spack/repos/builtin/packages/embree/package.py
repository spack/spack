# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Embree(CMakePackage):
    """Intel Embree High Performance Ray Tracing Kernels"""

    homepage = "https://embree.org"
    url      = "https://github.com/embree/embree/archive/v3.7.0.tar.gz"
    maintainers = ['aumuell']

    version('3.13.1', sha256='00dbd852f19ae2b95f5106dd055ca4b304486436ced0ccf842aec4e38a4df425')
    version('3.13.0', sha256='4d86a69508a7e2eb8710d571096ad024b5174834b84454a8020d3a910af46f4f')
    version('3.12.2', sha256='22a527622497e07970e733f753cc9c10b2bd82c3b17964e4f71a5fd2cdfca210')
    version('3.12.1', sha256='0c9e760b06e178197dd29c9a54f08ff7b184b0487b5ba8b8be058e219e23336e')
    version('3.12.0', sha256='f3646977c45a9ece1fb0cfe107567adcc645b1c77c27b36572d0aa98b888190c')
    version('3.11.0', sha256='2ccc365c00af4389aecc928135270aba7488e761c09d7ebbf1bf3e62731b147d')
    version('3.10.0', sha256='f1f7237360165fb8859bf71ee5dd8caec1fe02d4d2f49e89c11d250afa067aff')
    version('3.9.0',  sha256='53855e2ceb639289b20448ae9deab991151aa5f0bc7f9cc02f2af4dd6199d5d1')
    version('3.8.0',  sha256='40cbc90640f63c318e109365d29aea00003e4bd14aaba8bb654fc1010ea5753a')
    version('3.7.0',  sha256='2b6300ebe30bb3d2c6e5f23112b4e21a25a384a49c5e3c35440aa6f3c8d9fe84')

    # default to Release, as RelWithDebInfo creates a lot of overhead
    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    variant('ispc', default=True, description='Enable ISPC support')
    depends_on('ispc', when='+ispc', type='build')

    depends_on('tbb')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DBUILD_TESTING=OFF',
            '-DEMBREE_TUTORIALS=OFF',
            '-DEMBREE_IGNORE_CMAKE_CXX_FLAGS=ON',
            self.define_from_variant('EMBREE_ISPC_SUPPORT', 'ispc'),

            # code selection and defines controlling namespace names are based on
            # defines controlled by compiler flags, so disable ISAs below compiler
            # flags chosen by spack
            self.define('EMBREE_ISA_SSE2', 'sse4_2' not in spec.target),
            self.define('EMBREE_ISA_SSE42', 'avx' not in spec.target),
            self.define('EMBREE_ISA_AVX', 'avx2' not in spec.target),
            self.define('EMBREE_ISA_AVX2', 'avx512' not in spec.target),
            self.define('EMBREE_ISA_AVX512SKX', True),
        ]

        if spec.satisfies('%gcc@:7'):
            # remove unsupported -mprefer-vector-width=256, otherwise copied
            # from common/cmake/gnu.cmake
            args.append('-DFLAGS_AVX512SKX=-mavx512f -mavx512dq -mavx512cd'
                        ' -mavx512bw -mavx512vl -mf16c -mavx2 -mfma -mlzcnt'
                        ' -mbmi -mbmi2')

        return args
