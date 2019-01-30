# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Xsbench(MakefilePackage):
    """XSBench is a mini-app representing a key computational
       kernel of the Monte Carlo neutronics application OpenMC.
       A full explanation of the theory and purpose of XSBench
       is provided in docs/XSBench_Theory.pdf."""

    homepage = "https://github.com/ANL-CESAR/XSBench/"
    url = "https://github.com/ANL-CESAR/XSBench/archive/v13.tar.gz"

    tags = ['proxy-app', 'ecp-proxy-app']

    version('18', sha256='a9a544eeacd1be8d687080d2df4eeb701c04eda31d3806e7c3ea1ff36c26f4b0')
    version('14', '94d5d28eb031fd4ef35507c9c1862169')
    version('13', '72a92232d2f5777fb52f5ea4082aff37')

    variant('mpi', default=True, description='Build with MPI support')
    variant('openmp', default=True, description='Build with OpenMP support')

    depends_on('mpi', when='+mpi')

    build_directory = 'src'

    @property
    def build_targets(self):

        targets = []

        cflags = '-std=gnu99'
        if '+mpi' in self.spec:
            targets.append('CC={0}'.format(self.spec['mpi'].mpicc))
        else:
            targets.append('CC={0}'.format(self.compiler.cxx))

        if '+openmp' in self.spec:
            cflags += ' ' + self.compiler.openmp_flag
        targets.append('CFLAGS={0}'.format(cflags))
        targets.append('LDFLAGS=-lm')

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('src/XSBench', prefix.bin)
