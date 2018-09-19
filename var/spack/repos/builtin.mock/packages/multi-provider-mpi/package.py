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


class MultiProviderMpi(Package):
    """This is a fake MPI package used to test packages providing multiple
       virtuals at the same version."""
    homepage = "http://www.spack-fake-mpi.org"
    url      = "http://www.spack-fake-mpi.org/downloads/multi-mpi-1.0.tar.gz"

    version('2.0.0', 'foobarbaz')
    version('1.10.3', 'foobarbaz')
    version('1.10.2', 'foobarbaz')
    version('1.10.1', 'foobarbaz')
    version('1.10.0', 'foobarbaz')
    version('1.8.8', 'foobarbaz')
    version('1.6.5', 'foobarbaz')

    provides('mpi@3.1', when='@2.0.0')
    provides('mpi@3.0', when='@1.10.3')
    provides('mpi@3.0', when='@1.10.2')
    provides('mpi@3.0', when='@1.10.1')
    provides('mpi@3.0', when='@1.10.0')
    provides('mpi@3.0', when='@1.8.8')
    provides('mpi@2.2', when='@1.6.5')

    def install(self, spec, prefix):
        pass
