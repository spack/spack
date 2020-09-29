# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Slate(Package):
    """The Software for Linear Algebra Targeting Exascale (SLATE) project is
    to provide fundamental dense linear algebra capabilities to the US
    Department of Energy and to the high-performance computing (HPC) community
    at large. To this end, SLATE will provide basic dense matrix operations
    (e.g., matrix multiplication, rank-k update, triangular solve), linear
    systems solvers, least square solvers, singular value and eigenvalue
    solvers."""

    homepage = "https://icl.utk.edu/slate/"
    git      = "https://bitbucket.org/icl/slate"
    maintainers = ['G-Ragghianti', 'mgates3']

    version('develop', submodules=True)

    variant('cuda',   default=True, description='Build with CUDA support.')
    variant('mpi',    default=True, description='Build with MPI support.')
    variant('openmp', default=True, description='Build with OpenMP support.')

    depends_on('scalapack')
    depends_on('blas')
    depends_on('cuda@9:10', when='+cuda')
    depends_on('mpi',       when='+mpi')

    conflicts('%gcc@:5')

    def install(self, spec, prefix):
        f_cuda = "1" if spec.variants['cuda'].value   else "0"
        f_mpi  = "1" if spec.variants['mpi'].value    else "0"
        f_omp  = "1" if spec.variants['openmp'].value else "0"

        comp_cxx = comp_for = ''
        if '+mpi' in spec:
            comp_cxx = 'mpicxx'
            comp_for = 'mpif90'

        if '^openblas' in spec:
            blas = 'openblas'
        elif '^intel-mkl' in spec:
            blas = 'mkl'
        elif '^essl' in spec:
            blas = 'essl'
        else:
            raise InstallError('Supports only BLAS provider openblas, intel-mkl, or essl')


        make('all', 'install',
             'prefix=' + prefix,
             'mpi=' + f_mpi,
             'blas=' + blas,
             'cuda=' + f_cuda,
             'openmp=' + f_omp,
             'c_api=1',
             'fortran_api=1',
             'CXX=' + comp_cxx,
             'FC=' + comp_for)
