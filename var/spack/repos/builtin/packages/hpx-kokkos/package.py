# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class HpxKokkos(CMakePackage, CudaPackage, ROCmPackage):
    """HPXKokkos is an interoperability library for HPX and Kokkos"""

    homepage = 'https://github.com/STEllAR-GROUP/hpx-kokkos'
    url = "https://github.com/STEllAR-GROUP/hpx-kokkos/archive/0.0.0.tar.gz"
    maintainers = ['G-071', 'msimberg']

    version('master', git='https://github.com/STEllAR-GROUP/hpx-kokkos.git', branch='master')
    version('0.3.0', sha256='83c1d11dab95552ad0abdae767c71f757811d7b51d82bd231653dc942e89a45d')
    version('0.2.0', sha256='289b711cea26afe80be002fc521234c9194cd0e8f69863f3b08b654674dbe5d5')
    version('0.1.0', sha256='24edb817d0969f4aea1b68eab4984c2ea9a58f4760a9b8395e20f85b178f0850')

    cxxstds = ('14', '17', '20')
    variant('cxxstd', default='14', values=cxxstds, description='Use the specified C++ standard when building.')

    depends_on('cmake@3.19:', type='build')

    depends_on('hpx')
    depends_on('kokkos +hpx +hpx_async_dispatch')

    depends_on('hpx@1.8:', when='@0.3:')
    depends_on('kokkos@3.6:', when='@0.3:')

    depends_on('hpx@1.7', when='@0.2')
    depends_on('kokkos@3.6:', when='@0.2')

    depends_on('hpx@1.6', when='@0.1')
    depends_on('kokkos@3.2:3.5', when='@0.1')

    for cxxstd in cxxstds:
        depends_on('hpx cxxstd={0}'.format(cxxstd), when='cxxstd={0}'.format(cxxstd))
        depends_on('kokkos std={0}'.format(cxxstd), when='cxxstd={0}'.format(cxxstd))

    # HPXKokkos explicitly supports CUDA and ROCm. Other GPU backends can be
    # used but without support in HPXKokkos. Other CPU backends, except Serial,
    # can't be used together with the HPX backend.
    depends_on('hpx +cuda', when='+cuda')
    depends_on('kokkos +cuda +cuda_lambda +cuda_constexpr', when='+cuda')

    depends_on('hpx +rocm', when='+rocm')
    depends_on('kokkos +rocm', when='+rocm')
