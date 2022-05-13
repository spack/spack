# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ectrans(CMakePackage):
    """Ectrans is the global spherical Harmonics transforms library, extracted from the IFS.
    It is using a hybrid of MPI and OpenMP parallelisation strategies. The package contains
    both single- and double precision Fortran libraries (trans_sp, trans_dp), as well as a
    C interface to the double-precision version (transi_dp)."""

    homepage = "https://github.com/ecmwf-ifs/ectrans"
    git = "https://github.com/ecmwf-ifs/ectrans.git"

    maintainers = ['climbfuji']

    version('develop', branch='develop', no_cache=True, preferred=True)
    version('main', branch='main', no_cache=True, preferred=False)

    variant('mpi', default=True, description='Use MPI?')
    variant('openmp', default=True, description='Use OpenMP?')

    variant('double_precision', default=True, description='Support for double precision?')
    variant('single_precision', default=True, description='Support for single precision?')

    variant('mkl',  default=False, description='Use MKL?')
    variant('fftw', default=True, description='Use FFTW?')

    variant('transi', default=True, description='Compile TransI C-interface to trans?')

    depends_on('ecbuild', type=('build'))
    #depends_on('ecbuild')
    depends_on('mpi',  when='+mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw-api', when='+fftw')
    depends_on('mkl', when='+mkl')

    depends_on('fiat~mpi',  when='~mpi')
    depends_on('fiat+mpi',  when='+mpi')

    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_MPI', 'mpi'),
            self.define_from_variant('ENABLE_OMP', 'openmp'),
            self.define_from_variant('ENABLE_DOUBLE_PRECISION', 'double_precision'),
            self.define_from_variant('ENABLE_SINGLE_PRECISION', 'single_precision'),
            self.define_from_variant('ENABLE_FFTW', 'fftw'),
            self.define_from_variant('ENABLE_MKL', 'mkl'),
            self.define_from_variant('ENABLE_TRANSI', 'transi')
        ]

        return args
