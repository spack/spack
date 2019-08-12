# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Simul(Package):
    """simul is an MPI coordinated test of parallel
    filesystem system calls and library functions. """

    homepage = "https://github.com/LLNL/simul"
    url      = "https://github.com/LLNL/simul/archive/1.16.tar.gz"

    version('1.16', 'd616c1046a170c1e1b7956c402d23a95')
    version('1.15', 'a5744673c094a87c05c6f0799d1f496f')
    version('1.14', 'f8c14f0bac15741e2af354e3f9a0e30f')
    version('1.13', '8a80a62d569557715d6c9c326e39a8ef')

    depends_on('mpi')

    def install(self, spec, prefix):
        filter_file('mpicc',  '$(MPICC)',  'Makefile', string=True)
        filter_file('inline void',  'void',  'simul.c', string=True)
        make('simul')
        mkdirp(prefix.bin)
        install('simul', prefix.bin)
