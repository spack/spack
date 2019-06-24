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

class Minivite(MakefilePackage):
    """miniVite is a proxy application that implements a single phase of
       Louvain method in distributed memory for graph community detection.
    """
    tags = ['proxy-app', 'ecp-proxy-app']

    homepage = "http://hpc.pnl.gov/people/hala/grappolo.html"
    git      = "https://github.com/Exa-Graph/miniVite.git"

    version('develop', branch='master')
    version('1.0', tag='v1.0')
    version('1.1', tag='v1.1')

    variant('openmp', default=True, description='Build with OpenMP support')
    variant('opt', default=True, description='Optimization flags')

    depends_on('mpi')

    @property
    def build_targets(self):
        targets = []
        cxxflags = ['-std=c++11 -g -DCHECK_NUM_EDGES -DPRINT_EXTRA_NEDGES']
        ldflags = []

        if '+openmp' in self.spec:
            cxxflags.append(self.compiler.openmp_flag)
            ldflags.append(self.compiler.openmp_flag)
        if '+opt' in self.spec:
            cxxflags.append(' -O3 ')

        targets.append('CXXFLAGS={0}'.format(' '.join(cxxflags)))
        targets.append('OPTFLAGS={0}'.format(' '.join(ldflags)))
        targets.append('CXX={0}'.format(self.spec['mpi'].mpicxx))

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if (self.version == Version('1.0')):
            install('dspl', prefix.bin)
        elif (self.version == Version('1.1')):
            install('miniVite', prefix.bin)
