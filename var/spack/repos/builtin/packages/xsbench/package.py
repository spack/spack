##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Xsbench(MakefilePackage):
    """XSBench is a mini-app representing a key computational
       kernel of the Monte Carlo neutronics application OpenMC.
       A full explanation of the theory and purpose of XSBench
       is provided in docs/XSBench_Theory.pdf."""

    homepage = "https://github.com/ANL-CESAR/XSBench/"
    url = "https://github.com/ANL-CESAR/XSBench/archive/v13.tar.gz"

    tags = ['proxy-app', 'ecp-proxy-app']

    version('14', '94d5d28eb031fd4ef35507c9c1862169')
    version('13', '72a92232d2f5777fb52f5ea4082aff37')

    variant('mpi', default=False, description='Build with MPI support')

    depends_on('mpi', when='+mpi')

    build_directory = 'src'

    @property
    def build_targets(self):

        targets = []

        cflags = '-std=gnu99'
        if '+mpi' in self.spec:
            targets.append('CC={0}'.format(self.spec['mpi'].mpicc))

        cflags += ' ' + self.compiler.openmp_flag
        targets.append('CFLAGS={0}'.format(cflags))
        targets.append('LDFLAGS=-lm')

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('src/XSBench', prefix.bin)
