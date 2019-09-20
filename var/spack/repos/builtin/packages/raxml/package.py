# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.spec import ConflictsInSpecError
import glob


class Raxml(Package):
    """RAxML (Randomized Axelerated Maximum Likelihood) is a program for
       sequential and parallel Maximum Likelihood based inference of large
       phylogenetic trees."""

    homepage = "https://sco.h-its.org/exelixis/web/software/raxml"
    url      = "https://github.com/stamatak/standard-RAxML/archive/v8.2.11.tar.gz"

    version('8.2.11', '6bd5c4e1f93003ccf13c9b59a5d080ab')

    variant('mpi', default=True, description='Enable MPI parallel support')
    variant('pthreads', default=False, description='Enable pthreads version')
    variant('sse', default=False, description='Enable SSE in order to substantially speed up execution')
    variant('avx', default=False, description='Enable AVX in order to substantially speed up execution')

    depends_on('mpi', when='+mpi')

    patch('nox86.patch')

    # Compiles with either GCC or ICC.
    conflicts('%cce')
    conflicts('%clang')
    conflicts('%nag')
    conflicts('%pgi')
    conflicts('%xl')
    conflicts('%xl_r')

    # can't build multiple binaries in parallel without things breaking
    parallel = False

    def flag_handler(self, name, flags):
        arch = ''
        spec = self.spec
        if spec.satisfies("platform=cray"):
            # FIXME; It is assumed that cray is x86_64.
            # If you support arm on cray, you need to fix it.
            arch = 'x86_64'
        if arch != 'x86_64' and not spec.target.family == 'x86_64':
            if spec.satisfies("+sse"):
                raise ConflictsInSpecError(
                    spec,
                    [(
                        spec,
                        spec.architecture.target,
                        spec.variants['sse'],
                        '+sse is valid only on x86_64'
                    )]
                )
            if spec.satisfies("+avx"):
                raise ConflictsInSpecError(
                    spec,
                    [(
                        spec,
                        spec.architecture.target,
                        spec.variants['avx'],
                        '+avx is valid only on x86_64'
                    )]
                )
        return (flags, None, None)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        files = glob.iglob("Makefile.*")
        for file in files:
            makefile = FileFilter(file)
            makefile.filter('gcc', spack_cc)
            if spec.satisfies('+mpi'):
                makefile.filter('mpicc', self.spec['mpi'].mpicc)

        if spec.target.family == 'x86_64':
            if spec.satisfies('+mpi +avx +pthreads'):
                make('-f', 'Makefile.AVX.HYBRID.gcc')
                install('raxmlHPC-HYBRID-AVX', prefix.bin)

            if spec.satisfies('+mpi +sse +pthreads'):
                make('-f', 'Makefile.SSE3.HYBRID.gcc')
                install('raxmlHPC-HYBRID-SSE3', prefix.bin)

            if spec.satisfies('+mpi +pthreads'):
                make('-f', 'Makefile.HYBRID.gcc')
                install('raxmlHPC-HYBRID', prefix.bin)

            if spec.satisfies('+mpi +avx'):
                make('-f', 'Makefile.AVX.MPI.gcc')
                install('raxmlHPC-MPI-AVX', prefix.bin)

            if spec.satisfies('+mpi +sse'):
                make('-f', 'Makefile.SSE3.MPI.gcc')
                install('raxmlHPC-MPI-SSE3', prefix.bin)

            if spec.satisfies('+mpi'):
                make('-f', 'Makefile.MPI.gcc')
                install('raxmlHPC-MPI', prefix.bin)

            if spec.satisfies('+pthreads +avx'):
                make('-f', 'Makefile.AVX.PTHREADS.gcc')
                install('raxmlHPC-PTHREADS-AVX', prefix.bin)

            if spec.satisfies('+pthreads +sse'):
                make('-f', 'Makefile.SSE3.PTHREADS.gcc')
                install('raxmlHPC-PTHREADS-SSE3', prefix.bin)

            if spec.satisfies('+pthreads'):
                make('-f', 'Makefile.PTHREADS.gcc')
                install('raxmlHPC-PTHREADS', prefix.bin)

            if spec.satisfies('+sse'):
                make('-f', 'Makefile.SSE3.gcc')
                install('raxmlHPC-SSE3', prefix.bin)

            if spec.satisfies('+avx'):
                make('-f', 'Makefile.AVX.gcc')
                install('raxmlHPC-AVX', prefix.bin)

            make('-f', 'Makefile.gcc')
            install('raxmlHPC', prefix.bin)
        else:
            if spec.satisfies('+mpi +pthreads'):
                make('-f', 'Makefile.HYBRID.nox86.gcc')
                install('raxmlHPC-HYBRID', prefix.bin)

            if spec.satisfies('+mpi'):
                make('-f', 'Makefile.MPI.nox86.gcc')
                install('raxmlHPC-MPI', prefix.bin)

            if spec.satisfies('+pthreads'):
                make('-f', 'Makefile.PTHREADS.nox86.gcc')
                install('raxmlHPC-PTHREADS', prefix.bin)

            make('-f', 'Makefile.nox86.gcc')
            install('raxmlHPC', prefix.bin)
