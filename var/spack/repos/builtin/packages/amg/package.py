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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 0s2111-1307 USA
##############################################################################
from spack import *


class Amg(MakefilePackage):
    """AMG is a parallel algebraic multigrid solver for linear systems arising
       from problems on unstructured grids.  The driver provided with AMG
       builds linear systems for various 3-dimensional problems.
    """
    tags = ['proxy-app', 'ecp-proxy-app']

    homepage = "https://computation.llnl.gov/projects/co-design/amg2013"
    git      = "https://github.com/LLNL/AMG.git"

    version('develop', branch='master')
    version('1.0', tag='1.0')

    variant('openmp', default=True, description='Build with OpenMP support')
    variant('optflags', default=False, description='Additional optimizations')
    variant('int64', default=False, description='Use 64-bit integers for global variables')

    depends_on('mpi')

    @property
    def build_targets(self):
        targets = []

        include_cflags = ['-DTIMER_USE_MPI']
        include_lflags = ['-lm']

        if '+openmp' in self.spec:
            include_cflags.append('-DHYPRE_USING_OPENMP')
            include_cflags.append(self.compiler.openmp_flag)
            include_lflags.append(self.compiler.openmp_flag)
            if '+optflags' in self.spec:
                include_cflags.append('-DHYPRE_USING_PERSISTENT_COMM')
                include_cflags.append('-DHYPRE_HOPSCOTCH')

        if '+int64' in self.spec:
            include_cflags.append('-DHYPRE_BIGINT')

        targets.append('INCLUDE_CFLAGS={0}'.format(' '.join(include_cflags)))
        targets.append('INCLUDE_LFLAGS={0}'.format(' '.join(include_lflags)))
        targets.append('CC={0}'.format(self.spec['mpi'].mpicc))

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('test/amg', prefix.bin)
        install_tree('docs', prefix.docs)
