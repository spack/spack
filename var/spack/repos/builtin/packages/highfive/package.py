# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Highfive(CMakePackage):
    """HighFive - Header only C++ HDF5 interface"""

    homepage = "https://github.com/BlueBrain/HighFive"
    url      = "https://github.com/BlueBrain/HighFive/archive/v2.0.tar.gz"
    git      = "https://github.com/BlueBrain/HighFive.git"

    version('develop', branch='master')
    version('2.1.1', tag='v2.1.1')
    version('2.0', '51676953bfeeaf5f0368840525d269e3')
    version('1.5', '5e631c91d2ea7f3677e99d6bb6db8167')
    version('1.2', '030728d53519c7e13b5a522d34240301')
    version('1.1', '986f0bd18c5264709688a536c02d2b2a')
    version('1.0', 'e44e548560ea92afdb244c223b7655b6')

    # This is a header-only lib so dependencies shall be specified in the
    # target project directly and never specified here since they get truncated
    # when installed as external packages (which makes sense to improve reuse)
    variant('boost',   default=True,  description='Support Boost')
    variant('mpi',     default=True,  description='Support MPI')
    variant('eigen',   default=False, description='Support Eigen')
    variant('xtensor', default=False, description='Support xtensor')

    # Develop builds tests which require boost
    conflicts('~boost', when='@develop')

    depends_on('boost @1.41:', when='+boost')
    depends_on('hdf5 ~mpi', when='~mpi')
    depends_on('hdf5 +mpi', when='+mpi')
    depends_on('eigen', when='+eigen')
    depends_on('xtensor', when='+xtensor')

    def cmake_args(self):
        return [
            '-DUSE_EIGEN:Bool=' + ('TRUE' if '+eigen' in self.spec else 'FALSE'),
            '-DUSE_XTENSOR:Bool=' + ('TRUE' if '+xtensor' in self.spec else 'FALSE'),
            '-DUSE_BOOST:Bool={0}'.format('+boost' in self.spec),
            '-DHIGHFIVE_PARALLEL_HDF5:Bool={0}'.format('+mpi' in self.spec),
            '-DHIGHFIVE_EXAMPLES:Bool={0}'.format(self.spec.satisfies('@develop')),
            '-DHIGHFIVE_UNIT_TESTS:Bool={0}'.format(self.spec.satisfies('@develop')),
            '-DHIGHFIVE_TEST_SINGLE_INCLUDES:Bool={0}'.format(self.spec.satisfies('@develop')),
            '-DHDF5_NO_FIND_PACKAGE_CONFIG_FILE=1',  # Dont use targets
        ]
