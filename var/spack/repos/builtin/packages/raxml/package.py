##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        files = glob.iglob("Makefile.*")
        for file in files:
            makefile = FileFilter(file)
            makefile.filter('gcc', spack_cc)

        if '+mpi' and '+avx' and '+pthreads' in spec:
            make('-f', 'Makefile.AVX.HYBRID.gcc')
            install('raxmlHPC-HYBRID-AVX', prefix.bin)

        elif '+mpi' and '+sse' and '+pthreads' in spec:
            make('-f', 'Makefile.SSE3.HYBRID.gcc')
            install('raxmlHPC-HYBRID-SSE3', prefix.bin)

        elif '+mpi' and '+pthreads' in spec:
            make('-f', 'Makefile.HYBRID.gcc')
            install('raxmlHPC-HYBRID', prefix.bin)

        elif '+mpi' and '+avx' in spec:
            make('-f', 'Makefile.AVX.MPI.gcc')
            install('raxmlHPC-MPI-AVX', prefix.bin)

        elif '+mpi' and '+sse' in spec:
            make('-f', 'Makefile.SSE3.MPI.gcc')
            install('raxmlHPC-MPI-SSE3', prefix.bin)

        elif '+mpi' in spec:
            make('-f', 'Makefile.MPI.gcc')
            install('raxmlHPC-MPI', prefix.bin)

        elif '+pthreads' and '+avx' in spec:
            make('-f', 'Makefile.AVX.PTHREADS.gcc')
            install('raxmlHPC-PTHREADS-AVX', prefix.bin)

        elif '+pthreads' and '+sse' in spec:
            make('-f', 'Makefile.SSE3.PTHREADS.gcc')
            install('raxmlHPC-PTHREADS-SSE3', prefix.bin)

        elif '+pthreads' in spec:
            make('-f', 'Makefile.PTHREADS.gcc')
            install('raxmlHPC-PTHREADS', prefix.bin)

        elif '+sse' in spec:
            make('-f', 'Makefile.SSE3.gcc')
            install('raxmlHPC-SSE3', prefix.bin)

        elif '+avx' in spec:
            make('-f', 'Makefile.AVX.gcc')
            install('raxmlHPC-AVX', prefix.bin)

        else:
            make('-f', 'Makefile.gcc')
            install('raxmlHPC', prefix.bin)
