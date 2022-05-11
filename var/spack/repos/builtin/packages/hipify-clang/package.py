# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class HipifyClang(CMakePackage):
    """hipify-clang is a clang-based tool for translation CUDA
    sources into HIP sources"""

    homepage = "https://github.com/ROCm-Developer-Tools/HIPIFY"
    git      = "https://github.com/ROCm-Developer-Tools/HIPIFY.git"
    url      = "https://github.com/ROCm-Developer-Tools/HIPIFY/archive/rocm-5.0.2.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('master', branch='master')
    version('5.1.0', sha256='ba792294cbdcc880e0f02e38ee352dff8d4a2c183430e13d1c5ed176bd46cfc5')
    version('5.0.2', sha256='812bccfeb044483a1c7df89f45843afcb28d8146f348c792f082b693cbff3984')
    version('5.0.0', sha256='06fbb3259b6d014bc24fb3c05f71026bc39ae564559d40f2ca37236044c7ba17')
    version('4.5.2', sha256='f0d401e634642a1d6659b9163a38661ee38da1e1aceabb1f16f78f8fce048a4e')
    version('4.5.0', sha256='1f6e1bd4b9d64eed67f519c453fa65b362a20583df1f35fd09d08de831f3c8de')
    version('4.3.1', sha256='c5754f7c2c68ea4f65cc0ffc1e8ccc30634181525b25c10817e07eaa75ca8157')
    version('4.3.0', sha256='182b336a994e3de0dfbce935dc35091388d18a29e3cfdadb2ab7da8a2dc121a2')
    version('4.2.0', sha256='afdc82ae00e14e8e742be6cd47d8fb120d18fc52fe96cba8d8ac4c56176a432e')
    version('4.1.0', sha256='ec9cc410167b6ab31706742f3d7a77dbd29eb548e7371134b3aace8597665475', deprecated=True)
    version('4.0.0', sha256='9d3906d606fca2bcb58f5f2a70cc4b9e298ca0e12a84ee5f18e42b7df97b38a4', deprecated=True)
    version('3.10.0', sha256='7ebba22ed70100150bedddffa08a84f91b546347662862487b6703a1edce2623', deprecated=True)
    version('3.9.0', sha256='07adb98e91ddd7420d873806866d53eaf77527fac57799e846823522191ba89a', deprecated=True)
    version('3.8.0', sha256='095b876a750a0dc1ae669102ba53d668f65062b823f8be745411db86a2db7916', deprecated=True)
    version('3.7.0', sha256='dd58c8b88d4b7877f2521b02954de79d570fa36fc751a17d33e56436ee02571e', deprecated=True)
    version('3.5.0', sha256='31e7c11d3e221e15a2721456c4f8bceea9c28fd37345464c86ea74cf05ddf2c9', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3.5:', type='build')
    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0', '5.0.2',
                '5.1.0', 'master']:
        depends_on('llvm-amdgpu@' + ver, when='@' + ver)

    def setup_run_environment(self, env):
        # The installer puts the binaries directly into the prefix
        # instead of prefix/bin, so add prefix to the PATH
        env.prepend_path('PATH', self.spec.prefix)
