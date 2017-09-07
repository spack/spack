##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 0s2111-1307 USA
##############################################################################
from spack import *


class Amg2013(MakefilePackage):
    """AMG2013 is a parallel algebraic multigrid solver for linear
    systems arising from problems on unstructured grids.
    It has been derived directly from the BoomerAMG solver in the
    hypre library, a large linear solver library that is being developed
    in the Center for Applied Scientific Computing (CASC) at LLNL.
    """
    tags = ['proxy-app']
    homepage = "https://codesign.llnl.gov/amg2013.php"
    url      = "https://codesign.llnl.gov/amg2013/amg2013.tgz"

    version('master', '9d918d2a69528b83e6e0aba6ba601fef',
            url='https://codesign.llnl.gov/amg2013/amg2013.tgz')

    variant('openmp', default=True, description='Build with OpenMP support')
    variant('assumepartition', default=False, description='Assumed partition (for thousands of processors)')

    depends_on('mpi')

    @property
    def build_targets(self):
        targets = []

        include_cflags = ' -DTIMER_USE_MPI '
        include_lflags = ' -lm '

        if '+assumepartition' in self.spec:
            include_cflags += ' -DHYPRE_NO_GLOBAL_PARTITION '

        if '+openmp' in self.spec:
            include_cflags += ' -DHYPRE_USING_OPENMP '
            include_cflags += self.compiler.openmp_flag
            include_lflags += ' ' + self.compiler.openmp_flag

        targets.append('INCLUDE_CFLAGS={0}'.format(' '.join(include_cflags)))
        targets.append('INCLUDE_LFLAGS={0}'.format(' '.join(include_lflags)))
        targets.append('CC={0}'.format(self.spec['mpi'].mpicc))

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('test/amg2013', prefix.bin)
        install_tree('docs', prefix.doc)
        install('COPYRIGHT', prefix.doc)
        install('COPYING.LESSER', prefix.doc)