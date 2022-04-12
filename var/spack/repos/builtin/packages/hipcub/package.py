# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hipcub(CMakePackage):
    """ Radeon Open Compute Parallel Primitives Library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipCUB"
    git      = "https://github.com/ROCmSoftwarePlatform/hipCUB.git"
    url      = "https://github.com/ROCmSoftwarePlatform/hipCUB/archive/rocm-5.0.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('5.1.0', sha256='b30d51fc5fca2584f0c9a6fa8dafc9fbdda96a3acff30288e49b397f8842f705')
    version('5.0.2', sha256='22effb18f2c38d76fa379f14c9f9ee7a11987a5d1ae4a7e837af87232c8c9183')
    version('5.0.0', sha256='09c4f1b88aa5f50f04043d379e4960dab556e0fbdf8e25ab03d02a07c1ff7b2f')
    version('4.5.2', sha256='bec9ba1a6aa0475475ee292e54807accc839ed001338275f48da13e3bfb77514')
    version('4.5.0', sha256='5902fae0485789f1d1cc6b8e81d9f1b39338170d3139844d5edf0d324f9694c9')
    version('4.3.1', sha256='20fcd34323c541c182655b7ff6dc6ff268c0127596f0d9993884621c2b14b67a')
    version('4.3.0', sha256='733499a8d55e2d73bf874d43a98ee7425e4325f77e03fb0c80debf36c740cb70')
    version('4.2.0', sha256='56b50e185b7cdf4615d2f56d3a4e86fe76f885e9ad04845f3d0671afcb315c69')
    version('4.1.0', sha256='6d33cc371b9a5ac9c0ab9853bac736f6cea0d2192f4dc9e6d8175d207ee4b4f2', deprecated=True)
    version('4.0.0', sha256='656bd6ec547810fd74bcebba41453e6e729f3fdb7346f5564ab71fc0346c3fb5', deprecated=True)
    version('3.10.0', sha256='759da5c6ef0cc1e4ecf2083659e78b8bbaa015f0bb360177674e0feb3032c5be', deprecated=True)
    version('3.9.0', sha256='c46995f9f18733ec18e370c21d7c0d6ac719e8e9d3254c6303a20ba90831e12e', deprecated=True)
    version('3.8.0', sha256='11d7d97268aeb953c34a80125c4577e27cb57cb6095606533105cecf2bd2ec9c', deprecated=True)
    version('3.7.0', sha256='a2438632ea1606e83a8c0e1a8777aa5fdca66d77d90862642eb0ec2314b4978d', deprecated=True)
    version('3.5.0', sha256='1eb2cb5f6e90ed1b7a9ac6dd86f09ec2ea27bceb5a92eeffa9c2123950c53b9d', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('numactl', type='link', when='@3.7.0:')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0',
                '5.0.2', '5.1.0']:
        depends_on('hip@' + ver, when='@' + ver)
        depends_on('rocprim@' + ver, when='@' + ver)
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        args = [
            self.define('CMAKE_MODULE_PATH', self.spec['hip'].prefix.cmake)
        ]

        if self.spec.satisfies('^cmake@3.21.0:3.21.2'):
            args.append(self.define('__skip_rocmclang', 'ON'))

        return args
