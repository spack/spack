# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


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
