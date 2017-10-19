##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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

import tarfile

from spack import *


class Minife(MakefilePackage):
    """Proxy Application. MiniFE is an proxy application
       for unstructured implicit finite element codes.
    """

    homepage = "https://mantevo.org/"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/MiniFE/miniFE-2.0.1.tgz"

    tags = ['proxy-app']

    version('2.0.1', '3113d7c8fc01495d08552672b0dbd015')

    variant('build', default='ref', description='Type of Parallelism',
            values=('ref', 'openmp_ref', 'qthreads', 'kokkos'))

    depends_on('mpi')
    depends_on('qthreads', when='build=qthreads')

    @property
    def build_version(self):
        return self.version.up_to(2)

    @property
    def build_targets(self):
        targets = [
            '--directory=miniFE-{0}_{1}/src'.format(
                self.build_version, self.spec.variants['build'].value),
            'CXX={0}'.format(self.spec['mpi'].mpicxx),
            'CC={0}'.format(self.spec['mpi'].mpicc)
        ]

        return targets

    def edit(self, spec, prefix):
        inner_tar = tarfile.open(name='miniFE-{0}_{1}.tgz'.format(
                                 self.build_version,
                                 self.spec.variants['build'].value))
        inner_tar.extractall()

        makefile = FileFilter('miniFE-{0}_{1}/src/Makefile'.format(
                              self.build_version,
                              self.spec.variants['build'].value))

        makefile.filter('-fopenmp', self.compiler.openmp_flag, string=True)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('miniFE-{0}_{1}/src/miniFE.x'.format(
                self.build_version, self.spec.variants['build'].value),
                prefix.bin)
