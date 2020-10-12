# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Blaspp(CMakePackage, CudaPackage):
    """C++ API for the Basic Linear Algebra Subroutines. Developed by the
       Innovative Computing Laboratory at the University of Tennessee,
       Knoxville."""

    homepage = 'https://bitbucket.org/icl/blaspp'
    url = 'https://bitbucket.org/icl/blaspp/downloads/blaspp-2020.09.00.tar.gz'
    maintainers = ['teonnik', 'Sely85', 'G-Ragghianti', 'mgates3']

    version('develop', git=homepage)
    version('2020.09.00', sha256='ee5d29171bbed515734007dd121ce2e733e2f83920c4d5ede046e657f4a513ef')

    variant('openmp',
            default=True,
            description='Use OpenMP internally.')

    variant('cuda', default=True,
            description='Build with CUDA')

    variant('shared',
            default=True,
            description='Build shared libraries')

    depends_on('cmake@3.15.0:', type='build')
    depends_on('blas')

    conflicts('^openblas@0.3.6:', msg='Testing errors in OpenBLAS >=0.3.6')

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append('-Dbuild_tests={0}'.format(
            'ON' if self.run_tests else 'OFF'))

        args.append('-Duse_openmp={0}'.format(
            'ON' if '+openmp' in spec else 'OFF'))

        args.append('-DBUILD_SHARED_LIBS={0}'.format(
            'ON' if '+shared' in spec else 'OFF'))

        args.append('-Duse_cuda={0}'.format(
            'ON' if '+cuda' in spec else 'OFF'))

        args.append('-DBLAS_LIBRARIES=%s' % spec['blas'].libs.joined(';'))
        return args

    def check(self):
        with working_dir(join_path(self.build_directory, 'test')):
            if os.system('./run_tests.py --quick'):
                raise Exception('Tests were not all successful!')
