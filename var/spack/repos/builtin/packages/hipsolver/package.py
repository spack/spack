# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hipsolver(CMakePackage):
    """hipSOLVER is a LAPACK marshalling library, with multiple supported backends.
        It sits between the application and a 'worker' LAPACK library, marshalling
        inputs into the backend library and marshalling results back to the application.
        hipSOLVER exports an interface that does not require the client to change,
        regardless of the chosen backend. Currently, hipSOLVER supports rocSOLVER
        and cuSOLVER as backends."""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipSOLVER"
    git      = "https://github.com/ROCmSoftwarePlatform/hipSOLVER.git"
    url      = "https://github.com/ROCmSoftwarePlatform/hipSOLVER/archive/rocm-4.5.0.tar.gz"

    maintainers = ['srekolam']

    version('master', branch='develop')
    version('4.5.2', sha256='9807bf1da0da25940b546cf5d5d6064d46d837907e354e10c6eeb2ef7c296a93')
    version('4.5.0', sha256='ee1176e977736a6e6fcba507fe6f56fcb3cefd6ba741cceb28464ea8bc476cd8')

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    for ver in ['4.5.0', '4.5.2', 'master']:
        depends_on('hip@' + ver, when='@' + ver)
        depends_on('rocblas@' + ver, when='@' + ver)
        depends_on('rocsolver@' + ver, when='@' + ver)
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        args = [
            self.define('BUILD_CLIENTS_SAMPLES', 'OFF'),
        ]
        return args
