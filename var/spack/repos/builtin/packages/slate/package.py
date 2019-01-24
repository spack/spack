# ------------------------------------------------------------------------------
# Copyright (c) 2017, University of Tennessee
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University of Tennessee nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL UNIVERSITY OF TENNESSEE BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ------------------------------------------------------------------------------


from spack import *
from shutil import copytree, copy


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

    version('develop', hg=hg)

    variant('cuda',   default=True, description='Build with CUDA support.')
    # variant('mkl',  default=True, description='Build using Intel MKL.')
    variant('mpi',    default=True, description='Build with MPI support.')
    variant('openmp', default=True, description='Build with OpenMP support.')

    depends_on('cuda@9:', when='+cuda')
    depends_on('intel-mkl')
    # depends_on('cblas')
    # depends_on('scalapack')
    depends_on('mpi', when='+mpi')

    conflicts('%gcc@:5')

    def setup_environment(self, spack_env, run_env):
        if('+cuda' in self.spec):
            spack_env.prepend_path('CPATH', self.spec['cuda'].prefix.include)
        spack_env.prepend_path('CPATH', self.spec['intel-mkl'].prefix
                               + '/mkl/include')

    def install(self, spec, prefix):
        f_cuda = "1" if spec.variants['cuda'].value else "0"
        f_mpi = "1" if spec.variants['mpi'].value else "0"
        f_openmp = "1" if spec.variants['openmp'].value else "0"

        compiler = 'mpicxx' if spec.variants['mpi'].value else ''

        make('mpi=' + f_mpi, 'mkl=1', 'cuda=' + f_cuda, 'openmp=' + f_openmp,
             'CXX=' + compiler)
        copytree('lib', prefix.lib)
        copytree('test', prefix.test)
        mkdirp(prefix.include)
        copy('slate.hh', prefix.include)
        copy('lapack_api/lapack_slate.hh',
             prefix.include + "/slate_lapack_api.hh")
        copy('scalapack_api/scalapack_slate.hh',
             prefix.include + "/slate_scalapack_api.hh")
