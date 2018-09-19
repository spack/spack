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


class Minitri(MakefilePackage):
    """A simple, triangle-based data analytics proxy application."""

    homepage = "https://github.com/Mantevo/miniTri"
    url      = "https://github.com/Mantevo/miniTri/archive/v1.0.tar.gz"

    version('1.0', '947e296ca408275232f47724267a85ce')

    variant('mpi', default=True, description='Build with MPI support')

    depends_on('mpi', when="+mpi")

    tags = ['proxy-app', 'ecp-proxy-app']

    @property
    def build_targets(self):
        targets = []
        if '+mpi' in self.spec:
            targets.append('CCC={0}'.format(self.spec['mpi'].mpicxx))
            targets.append('--directory=miniTri/linearAlgebra/MPI')
        else:
            targets.append('CCC={0}'.format(self.compiler.cxx))
            targets.append('--directory=miniTri/linearAlgebra/serial')

        targets.append('--file=Makefile')
        return targets

    def install(self, spec, prefix):
        # Manual installation
        mkdir(prefix.bin)
        mkdir(prefix.doc)

        if '+mpi' in spec:
            install('miniTri/linearAlgebra/MPI/miniTri.exe', prefix.bin)
        else:
            install('miniTri/linearAlgebra/serial/miniTri.exe', prefix.bin)
