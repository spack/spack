# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
import os


class Shengbte(Package):
    """ShengBTE is a software package for solving the Boltzmann Transport Equation for phonons."""

    homepage = "www.shengbte.org"
    url      = "www.shengbte.org/downloads/ShengBTE-v1.1.1-8a63749.tar.bz2"

    version('1.1.1-8a63749', sha256='43920740d19ae854c8ecae0b648acfdf1d7726ca4c2b44f1a1684457f2f88522')

    depends_on('mpi')
    depends_on('spglib')
    depends_on('intel-mkl')

    def edit(self, spec, prefix):
        arch_make = join_path(self.stage.source_path, 'Src', 'arch.make')
        copy('arch.make.example', arch_make)
        filter_file('export FFLAGS=.*', 'export FFLAGS=-debug -O2', arch_make)
        filter_file('export LDFLAGS=.*',
                    'export LDFLAGS=-L%s -lsymspg' % spec['spglib'].prefix.lib,
                    arch_make)
        filter_file('export MPIFC=.*',
                    'export MPIFC=%s' % spec['mpi'].mpifc,
                    arch_make)
        filter_file('LAPACK=.*',
                    'LAPACK=$(MKLROOT)/lib/intel64_lin/libmkl_lapack95_lp64.a -Wl,--start-group \\\n \
                    $(MKLROOT)/lib/intel64_lin/libmkl_intel_lp64.a \\\n \
                    $(MKLROOT)/lib/intel64_lin/libmkl_sequential.a \\\n \
                    $(MKLROOT)/lib/intel64_lin/libmkl_core.a -Wl,--end-group -lpthread -lm -ldl',
                    arch_make)

    def build(self, spec, prefix):
        with working_dir(join_path(self.stage.source_path, 'Src')):
            os.system('make')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.stage.source_path):
            install('ShengBTE', prefix.bin)
