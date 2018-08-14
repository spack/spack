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


class Miniaero(MakefilePackage):
    """Proxy Application. MiniAero is a mini-application for the evaulation
       of programming models and hardware for next generation platforms.
    """

    homepage = "http://mantevo.org"
    git      = "https://github.com/Mantevo/miniAero.git"

    tags = ['proxy-app']

    version('2016-11-11', commit='f46d135479a5be19ec5d146ccaf0e581aeff4596')

    depends_on('kokkos')

    @property
    def build_targets(self):
        targets = [
            '--directory=kokkos',
            'CXX=c++',
            'KOKKOS_PATH={0}'.format(self.spec['kokkos'].prefix)
        ]

        return targets

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install('kokkos/miniAero.host', prefix.bin)
        install('kokkos/README', prefix.doc)
        install('kokkos/tests/3D_Sod_Serial/miniaero.inp', prefix.bin)
        install_tree('kokkos/tests', prefix.doc.tests)
