# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    version('3.3.6', sha256='6019aff3c9c32bc72f1a82590e66d0efdcea0eb669b487e66e772c80f12d674d')
    version('3.3.5', sha256='7352bff3ea299e4c7d7fbe31c504f8eb9149d7e685dec5a12fbaa26379f603e2')
    version('3.3.4', sha256='dd254beb0bafc695d0f62ae1a222ff85b52dbaa3a16f76e781dce22d0d20a4a6')
    version('3.3.3', sha256='a4143fc45e4454b4b98fcea3516b3a79b8cdb3bc7fadf996d088c6a0d805fea1')
    version('3.3.2', sha256='3e1fa6e8c45635938193f84fee6c35a87fac26ee7c39c68c230e5080c4a8fe98')
    version('3.3.1', sha256='a0b4cebaabd8f371d1b364f9723585fbcc7c9640ca60273b99835e6cf115f056')
    version('3.3.0', sha256='e3cf8f9289de20540a79c9c5653bbe623cadd6202bfe9692e95c420b5adbb7e7')
    version('3.2.10', 'a85bb68c82988648c3d53ba9768d7dcbcfe105f8')
    version('3.2.9', '59ab81212f8eb2534b1545a9b42c38bf618a0d71')
    version('3.2.8', '64f4aef8012a424c7e079eaf0be71793ab9bc6e0')
    version('3.2.7', 'cc1bacbad97558b97da6b77c9644f184')

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

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('CPATH',
                             join_path(self.prefix, 'include', 'eigen3'))

    @property
    def headers(self):
        headers = find_all_headers(self.prefix.include)
        headers.directories = [self.prefix.include.eigen3]
        return headers
