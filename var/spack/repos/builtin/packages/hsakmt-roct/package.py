# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class HsakmtRoct(CMakePackage):
    """This is a thunk python recipe to build and install Thunk Interface.
       Thunk Interface is a user-mode API interfaces used to interact
       with the ROCk driver."""

    homepage = "https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface"
    git      = "https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface.git"
    url      = "https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface/archive/rocm-5.0.2.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('master', branch='master')
    version('5.0.2', sha256='f2a27ac18aada1dc0dba6455beb7dd7d88a4457c1917024ea372fecb03356e97')
    version('5.0.0', sha256='1d803572eac0d6186260b5671268bad7513aa9433f9c2e99f14c8bf766c02122')
    version('4.5.2', sha256='fb8e44226b9e393baf51bfcb9873f63ce7e4fcf7ee7f530979cf51857ea4d24b')
    version('4.5.0', sha256='620b39959e0ee5d709b8cf6eb3cc06c8356d72838343756230c638899b10bb9a')
    version('4.3.1', sha256='9d0727e746d4ae6e2709e3534d91046640be511a71c027f47db25e529fe3b4d4')
    version('4.3.0', sha256='1ef5fe687bc23ffda17841fe354c1fb94e9aaf276ca9e5757488852f9066f231')
    version('4.2.0', sha256='cc325d4b9a96062f2ad0515fce724a8c64ba56a7d7f1ac4a0753941b8599c52e')
    version('4.1.0', sha256='8443ed5907a7ba9ad4003a49d90ff7b8886e1b2a5e90f14e4035765a7f64d7ca', deprecated=True)
    version('4.0.0', sha256='a6960fffc8388731ee18953faae12d1449c582e3b3594418845a544455895f42', deprecated=True)
    version('3.10.0', sha256='a3d629247a763cc36f5d48e9122cee8498574af628e14e3c38686c05f66e3e06', deprecated=True)
    version('3.9.0', sha256='e1bb8b010855736d8a97957222f648532d42646ec2964776a9a1455dc81104a3', deprecated=True)
    version('3.8.0', sha256='cd5440f31f592737b5d05448704bd01f91f73cfcab8a7829922e81332575cfe8', deprecated=True)
    version('3.7.0', sha256='b357fe7f425996c49f41748923ded1a140933de7564a70a828ed6ded6d896458', deprecated=True)
    version('3.5.0', sha256='d9f458c16cb62c3c611328fd2f2ba3615da81e45f3b526e45ff43ab4a67ee4aa', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')
    variant('shared', default=True, description='Build shared or static library')

    depends_on('pkgconfig', type='build', when='@4.5.0:')
    depends_on('cmake@3:', type='build')
    depends_on('numactl')
    depends_on('libdrm', when='@4.5.0:')

    # See https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface/issues/72
    # and https://github.com/spack/spack/issues/28398
    patch('0001-Remove-compiler-support-libraries-and-libudev-as-req.patch', when='@4.5.0:')

    @property
    def install_targets(self):
        if self.version == Version('3.5.0'):
            return ['install', 'install-dev']
        else:
            return ['install']

    def cmake_args(self):
        return [
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared')
        ]
