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
    hg      = "https://bitbucket.org/icl/slate"
    maintainers = ['G-Ragghianti']

    version('develop', hg=hg)

    variant('cuda',   default=True, description='Build with CUDA support.')
    variant('mpi',    default=True, description='Build with MPI support.')
    variant('openmp', default=True, description='Build with OpenMP support.')

    depends_on('cuda@9:', when='+cuda')
    depends_on('intel-mkl')
    depends_on('mercurial', type='build')
    depends_on('mpi', when='+mpi')

    conflicts('%gcc@:5')

    def setup_build_environment(self, env):
        if('+cuda' in self.spec):
            env.prepend_path('CPATH', self.spec['cuda'].prefix.include)
        env.prepend_path('CPATH', self.spec['intel-mkl'].prefix.mkl.include)

    def install(self, spec, prefix):
        f_cuda = "1" if spec.variants['cuda'].value else "0"
        f_mpi = "1" if spec.variants['mpi'].value else "0"
        f_openmp = "1" if spec.variants['openmp'].value else "0"

        compiler = 'mpicxx' if spec.variants['mpi'].value else ''

        make('mpi=' + f_mpi, 'mkl=1', 'cuda=' + f_cuda, 'openmp=' + f_openmp,
             'CXX=' + compiler)
        install_tree('lib', prefix.lib)
        install_tree('test', prefix.test)
        mkdirp(prefix.include)
        install('include/slate/slate.hh', prefix.include)
        install('lapack_api/lapack_slate.hh',
                prefix.include + "/slate_lapack_api.hh")
        install('scalapack_api/scalapack_slate.hh',
                prefix.include + "/slate_scalapack_api.hh")
