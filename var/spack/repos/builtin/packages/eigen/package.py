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

    version('3.3.5', 'e83549a79d1b721da0f8899ab34edf95')
    version('3.3.4', 'a7aab9f758249b86c93221ad417fbe18')
    version('3.3.3', 'b2ddade41040d9cf73b39b4b51e8775b')
    version('3.3.1', 'edb6799ef413b0868aace20d2403864c')
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
