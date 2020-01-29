# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Eigen(CMakePackage):
    """Eigen is a C++ template library for linear algebra matrices,
    vectors, numerical solvers, and related algorithms.
    """

    homepage = 'http://eigen.tuxfamily.org/'
    url      = 'https://bitbucket.org/eigen/eigen/get/3.3.4.tar.bz2'

    version('3.3.7', sha256='9f13cf90dedbe3e52a19f43000d71fdf72e986beb9a5436dddcd61ff9d77a3ce')
    version('3.3.5', sha256='7352bff3ea299e4c7d7fbe31c504f8eb9149d7e685dec5a12fbaa26379f603e2')
    version('3.3.4', sha256='dd254beb0bafc695d0f62ae1a222ff85b52dbaa3a16f76e781dce22d0d20a4a6')
    version('3.3.3', sha256='a4143fc45e4454b4b98fcea3516b3a79b8cdb3bc7fadf996d088c6a0d805fea1')
    version('3.3.1', sha256='a0b4cebaabd8f371d1b364f9723585fbcc7c9640ca60273b99835e6cf115f056')
    version('3.2.10', sha256='760e6656426fde71cc48586c971390816f456d30f0b5d7d4ad5274d8d2cb0a6d')
    version('3.2.9', sha256='4d1e036ec1ed4f4805d5c6752b76072d67538889f4003fadf2f6e00a825845ff')
    version('3.2.8', sha256='722a63d672b70f39c271c5e2a4a43ba14d12015674331790414fcb167c357e55')
    version('3.2.7', sha256='e58e1a11b23cf2754e32b3c5990f318a8461a3613c7acbf6035870daa45c2f3e')

    variant('metis', default=False,
            description='Enables metis permutations in sparse algebra')
    variant('scotch', default=False,
            description='Enables scotch/pastix sparse factorization methods')
    variant('fftw', default=False,
            description='Enables FFTW backend for the FFT plugin')
    variant('suitesparse', default=False,
            description='Enables SuiteSparse sparse factorization methods')
    variant('mpfr', default=False,
            description='Enables the multi-precisions floating-point plugin')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo'))

    # TODO : dependency on googlehash, superlu, adolc missing
    depends_on('metis@5:', when='+metis')
    depends_on('scotch', when='+scotch')
    depends_on('fftw', when='+fftw')
    depends_on('suite-sparse', when='+suitesparse')
    depends_on('mpfr@2.3.0:', when='+mpfr')
    depends_on('gmp', when='+mpfr')

    patch('find-ptscotch.patch', when='@3.3.4')

    def setup_run_environment(self, env):
        env.prepend_path('CPATH', self.prefix.include.eigen3)

    @property
    def headers(self):
        headers = find_all_headers(self.prefix.include)
        headers.directories = [self.prefix.include.eigen3]
        return headers
