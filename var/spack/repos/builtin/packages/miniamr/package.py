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


class Miniamr(MakefilePackage):
    """Proxy Application. 3D stencil calculation with
       Adaptive Mesh Refinement (AMR)
    """

    homepage = "https://mantevo.org"
    url      = "https://github.com/Mantevo/miniAMR/archive/v1.4.0.tar.gz"

    tags = ['proxy-app', 'ecp-proxy-app']

    version('1.4.0', '3aab0247047a94e343709cf2e51cc46e')

    variant('mpi', default=True, description='Build with MPI support')

    depends_on('mpi', when="+mpi")

    @property
    def build_targets(self):
        targets = []
        if '+mpi' in self.spec:
            targets.append('CC={0}'.format(self.spec['mpi'].mpicc))
            targets.append('LD={0}'.format(self.spec['mpi'].mpicc))
            targets.append('LDLIBS=-lm')
        else:
            targets.append('CC={0}'.format(self.compiler.cc))
            targets.append('LD={0}'.format(self.compiler.cc))
        targets.append('--directory=ref')

        return targets

    def install(self, spec, prefix):
        # Manual installation
        mkdir(prefix.bin)
        mkdir(prefix.doc)

        install('ref/ma.x', prefix.bin)
        # Install Support Documents
        install('ref/README', prefix.doc)
