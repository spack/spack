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


class SstCore(AutotoolsPackage):
    """The Structural Simulation Toolkit (SST) was developed to explore
    innovations in highly concurrent systems where the ISA, microarchitecture,
    and memory interact with the programming model and communications system"""

    homepage = "http://sst-simulator.org/"
    url      = "https://github.com/sstsimulator/sst-core/releases/download/v8.0.0_Final/sstcore-8.0.0.tar.gz"
    git      = "https://github.com/sstsimulator/sst-core.git"

    version('develop', branch='devel')
    version('8.0.0', sha256='34a62425c3209cf80b6bca99cb0dcc328b67fb84ed92d5e6d6c975ad9319ba8a')

    variant('mpi', default=True, description='Support multi-node simulations using MPI')
    variant('boost', default=False, description='Use boost')

    depends_on('autoconf@1.68:', type='build', when='@develop')
    depends_on('automake@1.11.1:', type='build', when='@develop')
    depends_on('libtool@1.2.4:', type='build', when='@develop')
    depends_on('m4', type='build', when='@develop')

    depends_on('python@:2')
    depends_on('zlib', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('boost@1.56.0:', type='build', when='+boost')

    def configure_args(self):
        args = []
        spec = self.spec

        if '~mpi' in spec:
            args.append('--disable-mpi')

        if '+boost' in spec:
            args.append('--with-boost=%s' % spec['boost'].prefix)

        return args
