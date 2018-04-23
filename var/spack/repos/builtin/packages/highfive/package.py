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


class Highfive(CMakePackage):
    """HighFive - Header only C++ HDF5 interface"""

    homepage = "https://github.com/BlueBrain/HighFive"
    url      = "https://github.com/BlueBrain/HighFive/archive/v1.2.tar.gz"

    version('1.5', '5e631c91d2ea7f3677e99d6bb6db8167')
    version('1.2', '030728d53519c7e13b5a522d34240301')
    version('1.1', '986f0bd18c5264709688a536c02d2b2a')
    version('1.0', 'e44e548560ea92afdb244c223b7655b6')

    variant('boost', default=False, description='Support Boost')
    variant('mpi', default=True, description='Support MPI')

    depends_on('boost @1.41:', when='+boost')
    depends_on('hdf5')
    depends_on('hdf5 +mpi', when='+mpi')

    def cmake_args(self):
        args = [
            '-DUSE_BOOST:Bool={0}'.format('+boost' in self.spec),
            '-DHIGHFIVE_PARALLEL_HDF5:Bool={0}'.format('+mpi' in self.spec),
            '-DUNIT_TESTS:Bool=false',
            '-DHIGHFIVE_EXAMPLES:Bool=false']
        return args
