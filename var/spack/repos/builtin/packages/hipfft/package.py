# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Hipfft(CMakePackage):
    """hipFFT is an FFT marshalling library. Currently, hipFFT supports
       either rocFFT or cuFFT as backends.hipFFT exports an interface that
       does not require the client to change, regardless of the chosen backend.
       It sits between the application and the backend FFT library, marshalling
       inputs into the backend and results back to the application."""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipFFT"
    git      = "https://github.com/ROCmSoftwarePlatform/hipFFT.git"
    url      = "https://github.com/ROCmSoftwarePlatform/hipfft/archive/rocm-4.3.0.tar.gz"

    maintainers = ['arjun-raj-kuppala', 'srekolam']

    version('master', branch='master')

    version('4.3.1', sha256='429cfd40415856da8f5c2c321b612800d6826ee121df5a4e6d1596cad5b51727')
    version('4.3.0', sha256='6e52e0eb5b2a13adaf317fe5b20b3e059589aabf2af87e4c67cb1022b861ba84')
    version('4.2.0', sha256='74253b0d92feff55ebb39b3fe4a22a6454160a60bdad37384aa5340fd8843f8a')
    version('4.1.0', sha256='885ffd4813f2c271150f1b8b386f0af775b38fc82b96ce6fd94eb4ba0c0180be')

    depends_on('cmake@3:', type='build')

    for ver in ['4.1.0', '4.2.0', '4.3.0', '4.3.1']:
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)
        depends_on('hip@' + ver, when='@' + ver)
        depends_on('rocfft@' + ver, when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        args = [
            # Make sure find_package(HIP) finds the module.
            self.define('CMAKE_MODULE_PATH', self.spec['hip'].prefix.cmake),
            self.define('BUILD_CLIENTS_SAMPLES', 'OFF')
        ]

        if self.spec.satisfies('^cmake@3.21.0:3.21.2'):
            args.append(self.define('__skip_rocmclang', 'ON'))

        return args
