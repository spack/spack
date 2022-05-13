# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Highfive(CMakePackage):
    """HighFive - Header only C++ HDF5 interface"""

    homepage = "https://github.com/BlueBrain/HighFive"
    url      = "https://github.com/BlueBrain/HighFive/archive/v2.0.tar.gz"
    git      = "https://github.com/BlueBrain/HighFive.git"

    version('master', branch='master')
    version('2.4.1', tag='v2.4.1')
    version('2.4.0', tag='v2.4.0')
    version('2.3.1', tag='v2.3.1')
    version('2.3', tag='v2.3')
    version('2.2.2', tag='v2.2.2')
    version('2.2.1', tag='v2.2.1')
    version('2.1.1', tag='v2.1.1')
    version('2.0', sha256='deee33d7f578e33dccb5d04771f4e01b89a980dd9a3ff449dd79156901ee8d25')
    version('1.5', sha256='f194bda482ab15efa7c577ecc4fb7ee519f6d4bf83470acdb3fb455c8accb407')
    version('1.2', sha256='4d8f84ee1002e8fd6269b62c21d6232aea3d56ce4171609e39eb0171589aab31')
    version('1.1', sha256='430fc312fc1961605ffadbfad82b9753a5e59482e9fbc64425fb2c184123d395')
    version('1.0', sha256='d867fe73d00817f686d286f3c69a23731c962c3e2496ca1657ea7302cd0bb944')

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
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        return [
            '-DUSE_BOOST:Bool=' + str(self.spec.satisfies('+boost')),
            '-DUSE_EIGEN:Bool=' + str(self.spec.satisfies('+eigen')),
            '-DUSE_XTENSOR:Bool=' + str(self.spec.satisfies('+xtensor')),
            '-DHIGHFIVE_PARALLEL_HDF5:Bool='
            + str(self.spec.satisfies('+mpi')),
            '-DHIGHFIVE_EXAMPLES:Bool='
            + str(self.spec.satisfies('@develop')),
            '-DHIGHFIVE_UNIT_TESTS:Bool='
            + str(self.spec.satisfies('@develop')),
            '-DHIGHFIVE_TEST_SINGLE_INCLUDES:Bool='
            + str(self.spec.satisfies('@develop')),
            '-DHDF5_NO_FIND_PACKAGE_CONFIG_FILE=1',  # Dont use targets
            '-DHIGHFIVE_USE_INSTALL_DEPS:Bool=ON',
        ]
