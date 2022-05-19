# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocmBandwidthTest(CMakePackage):
    """Test to measure PciE bandwidth on ROCm platforms"""

    homepage = "https://github.com/RadeonOpenCompute/rocm_bandwidth_test"
    git      = "https://github.com/RadeonOpenCompute/rocm_bandwidth_test.git"
    url      = "https://github.com/RadeonOpenCompute/rocm_bandwidth_test/archive/rocm-5.0.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('master', branch='master')
    version('5.1.0', sha256='18fe51f0ba61760fc89ffc81f737fd4fa20fb4b00df3f35145be77c3e0a6162b')
    version('5.0.2', sha256='c93f7dbb37233aa32d81057fa8b3fa88d7c7be9b7916430b5ffc701600a5ff45')
    version('5.0.0', sha256='b33c6a12ad8de1d7ea9b8b380b8fa5db6b601ed426c3d3940134863f7d10740f')
    version('4.5.2', sha256='559ca7ef582d81047c5dd5a908f3989cb2694e89577f7f556214e324ba65e75e')
    version('4.5.0', sha256='4d20a6017ca6975df98f3ca61ba95fa0c7c62fbf63cd6abae3396c30a423933f')
    version('4.3.1', sha256='a4804c28586457c231594b4e7689872eaf91972119d892325468f3fe8fdbe5ef', deprecated=True)
    version('4.3.0', sha256='c6eb406cd2836af61dd5987f6b761340a1be20f66a9325f480423d10b9d3ec1b', deprecated=True)
    version('4.2.0', sha256='d268365e3bb8031c1201c05e705074d1fd794d236843f80064855cf31e4412f5', deprecated=True)
    version('4.1.0', sha256='4e34b60a7e4090d6475f0cdd86594b1b9a7b85d4e343999b9e148e196f0c2f4c', deprecated=True)
    version('4.0.0', sha256='bde2aa743979eac195dd13ec8d0fcb7da183fff489da32c28b872eed7f6681b3', deprecated=True)
    version('3.10.0', sha256='ad1dedad9023ccb050082c866fa5131665d9c3b50de0b78e4618730c29a07773', deprecated=True)
    version('3.9.0', sha256='f366299b48a29b419febb2ba398d1abe4cd01425d33254777e426966b722d3b1', deprecated=True)
    version('3.8.0', sha256='7de71a2ba17bbeea9107f2e9e65729f507234d6cbbb44f251240d64683027497', deprecated=True)
    version('3.7.0', sha256='9aa1d4b7b01ee4d443effc76ed5f6f43a051fd815692b59dfccf0ecbfeaeed03', deprecated=True)
    version('3.5.0', sha256='fbb63fb8713617fd167d9c1501acbd92a6b189ee8e1a8aed668fa6666baae389', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0', '5.0.2',
                '5.1.0', 'master']:
        depends_on('hsa-rocr-dev@' + ver, when='@' + ver)
        depends_on('hsakmt-roct@' + ver, when='@' + ver)

    build_targets = ['package']
