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


class Simplemoc(MakefilePackage):
    """The purpose of this mini-app is to demonstrate the performance
        characterterics and viability of the Method of Characteristics (MOC)
        for 3D neutron transport calculations in the context of full scale
        light water reactor simulation."""

    homepage = "https://github.com/ANL-CESAR/SimpleMOC/"
    url = "https://github.com/ANL-CESAR/SimpleMOC/archive/v4.tar.gz"

    version('4', sha256='a39906014fdb234c43bf26e1919bdc8a13097788812e0b353a492b8e568816a6')

    tags = ['proxy-app']

    variant('mpi', default=True, description='Build with MPI support')

    depends_on('mpi', when='+mpi')

    build_directory = 'src'

    @property
    def build_targets(self):

        targets = []

        cflags = '-std=gnu99'
        ldflags = '-lm'

        if self.compiler.name == 'gcc' or self.compiler.name == 'intel':
            cflags += ' ' + self.compiler.openmp_flag
        if '+mpi' in self.spec:
            targets.append('CC={0}'.format(self.spec['mpi'].mpicc))

        targets.append('CFLAGS={0}'.format(cflags))
        targets.append('LDFLAGS={0}'.format(ldflags))

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('src/SimpleMOC', prefix.bin)
