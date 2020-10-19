# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Slate(MakefilePackage):
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

    depends_on('bash', type='build')
    depends_on('scalapack')
    depends_on('blas')
    depends_on('cuda@9:10', when='+cuda')
    depends_on('mpi',       when='+mpi')

    conflicts('%gcc@:5')

    def edit(self, spec, prefix):
        if '^openblas' in spec:
            blas = 'openblas'
        elif '^intel-mkl' in spec:
            blas = 'mkl'
        elif '^essl' in spec:
            blas = 'essl'
        else:
            raise InstallError('Supports only BLAS provider '
                               'openblas, intel-mkl, or essl')
        config = [
            'SHELL=bash',
            'prefix=%s' % prefix,
            'mpi=%i'    % ('+mpi' in spec),
            'cuda=%i'   % ('+cuda' in spec),
            'openmp=%i' % ('+openmp' in spec),
            'blas=%s'   % blas
        ]
        if '+mpi' in spec:
            config.append('CXX=' + spec['mpi'].mpicxx)
            config.append('FC=' + spec['mpi'].mpifc)

        with open('make.inc', 'w') as inc:
            for line in config:
                inc.write('{0}\n'.format(line))
