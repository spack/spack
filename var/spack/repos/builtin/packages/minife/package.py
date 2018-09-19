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


class Minife(MakefilePackage):
    """Proxy Application. MiniFE is an proxy application
       for unstructured implicit finite element codes.
    """

    homepage = "https://mantevo.org/"
    url      = "https://github.com/Mantevo/miniFE/archive/v2.1.0.tar.gz"

    tags = ['proxy-app', 'ecp-proxy-app']

    version('2.1.0', '930a6b99c09722428a6f4d795b506a62')

    variant('build', default='ref', description='Type of Parallelism',
            values=('ref', 'openmp_ref', 'qthreads', 'kokkos'))

    depends_on('mpi')
    depends_on('qthreads', when='build=qthreads')

    @property
    def build_targets(self):
        targets = [
            '--directory={0}/src'.format(self.spec.variants['build'].value),
            'CXX={0}'.format(self.spec['mpi'].mpicxx),
            'CC={0}'.format(self.spec['mpi'].mpicc)
        ]

        return targets

    def edit(self, spec, prefix):
        makefile = FileFilter('{0}/src/Makefile'.format(
                              self.spec.variants['build'].value))

        makefile.filter('-fopenmp', self.compiler.openmp_flag, string=True)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('{0}/src/miniFE.x'.format(self.spec.variants['build'].value),
                prefix.bin)
