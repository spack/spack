# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
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
    variant('sse', default=True, description='Enable SSE in order to substantially speed up execution')
    variant('avx', default=False, description='Enable AVX in order to substantially speed up execution')

    depends_on('mpi', when='+mpi')

    # Compiles with either GCC or ICC.
    conflicts('%cce')
    conflicts('%clang')
    conflicts('%nag')
    conflicts('%pgi')
    conflicts('%xl')
    conflicts('%xl_r')

    # can't build multiple binaries in parallel without things breaking
    parallel = False

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        files = glob.iglob("Makefile.*")
        for file in files:
            makefile = FileFilter(file)
            makefile.filter('gcc', spack_cc)

        if '+mpi' and '+avx' and '+pthreads' in spec:
            make('-f', 'Makefile.AVX.HYBRID.gcc')
            install('raxmlHPC-HYBRID-AVX', prefix.bin)

        if '+mpi' and '+sse' and '+pthreads' in spec:
            make('-f', 'Makefile.SSE3.HYBRID.gcc')
            install('raxmlHPC-HYBRID-SSE3', prefix.bin)

        if '+mpi' and '+pthreads' in spec:
            make('-f', 'Makefile.HYBRID.gcc')
            install('raxmlHPC-HYBRID', prefix.bin)

        if '+mpi' and '+avx' in spec:
            make('-f', 'Makefile.AVX.MPI.gcc')
            install('raxmlHPC-MPI-AVX', prefix.bin)

        if '+mpi' and '+sse' in spec:
            make('-f', 'Makefile.SSE3.MPI.gcc')
            install('raxmlHPC-MPI-SSE3', prefix.bin)

        if '+mpi' in spec:
            make('-f', 'Makefile.MPI.gcc')
            install('raxmlHPC-MPI', prefix.bin)

        if '+pthreads' and '+avx' in spec:
            make('-f', 'Makefile.AVX.PTHREADS.gcc')
            install('raxmlHPC-PTHREADS-AVX', prefix.bin)

        if '+pthreads' and '+sse' in spec:
            make('-f', 'Makefile.SSE3.PTHREADS.gcc')
            install('raxmlHPC-PTHREADS-SSE3', prefix.bin)

        if '+pthreads' in spec:
            make('-f', 'Makefile.PTHREADS.gcc')
            install('raxmlHPC-PTHREADS', prefix.bin)

        if '+sse' in spec:
            make('-f', 'Makefile.SSE3.gcc')
            install('raxmlHPC-SSE3', prefix.bin)

        if '+avx' in spec:
            make('-f', 'Makefile.AVX.gcc')
            install('raxmlHPC-AVX', prefix.bin)

        make('-f', 'Makefile.gcc')
        install('raxmlHPC', prefix.bin)
