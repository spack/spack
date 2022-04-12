# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack import *


class Rocrand(CMakePackage):
    """The rocRAND project provides functions that generate
       pseudo-random and quasi-random numbers."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocRAND"
    git      = "https://github.com/ROCmSoftwarePlatform/rocRAND.git"
    url      = "https://github.com/ROCmSoftwarePlatform/rocRAND/archive/rocm-5.0.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('5.1.0', sha256='0c6f114a775d0b38be71f3f621a10bde2104a1f655d5d68c5fecb79b8b51a815')
    version('5.0.2', sha256='2dbce2a7fb273c2f9456c002adf3a510b9ec79f2ff32dfccdd59948f3ddb1505')
    version('5.0.0', sha256='356a03a74d6d5df3ae2d38da07929f23d90bb4dee71f88792c25c25069e673bc')
    version('4.5.2', sha256='1523997a21437c3b74d47a319d81f8cc44b8e96ec5174004944f2fb4629900db')
    version('4.5.0', sha256='fd391f81b9ea0b57808d93e8b72d86eec1b4c3529180dfb99ed6d3e2aa1285c2')
    version('4.3.1', sha256='b3d6ae0cdbbdfb56a73035690f8cb9e173fec1ccaaf9a4c5fdbe5e562e50c901')
    version('4.3.0', sha256='a85ced6c155befb7df8d58365518f4d9afc4407ee4e01d4640b5fd94604ca3e0')
    version('4.2.0', sha256='15725c89e9cc9cc76bd30415fd2c0c5b354078831394ab8b23fe6633497b92c8')
    version('4.1.0', sha256='94327e38739030ab6719a257f5a928a35842694750c7f46d9e11ff2164c2baed', deprecated=True)
    version('4.0.0', sha256='1cafdbfa15cde635bd424d2a858dc5cc94d668f9a211ff39606ee01ed1715f41', deprecated=True)
    version('3.10.0', sha256='f55e2b49b4dfd887e46eea049f3359ae03c60bae366ffc979667d364205bc99c', deprecated=True)
    version('3.9.0', sha256='a500a3a83be36b6c91aa062dc6eef1f9fc1d9ee62422d541cc279513d98efa91', deprecated=True)
    version('3.8.0', sha256='79eb84d41363a46ed9bb18d9757cf6a419d2f48bb6a71b8e4db616a5007a6560', deprecated=True)
    version('3.7.0', sha256='5e43fe07afe2c7327a692b3b580875bae6e6ee790e044c053fffafbfcbc14860', deprecated=True)
    version('3.5.0', sha256='592865a45e7ef55ad9d7eddc8082df69eacfd2c1f3e9c57810eb336b15cd5732', deprecated=True)

    amdgpu_targets = ('gfx803', 'gfx900:xnack-', 'gfx906:xnack-', 'gfx908:xnack-',
                      'gfx90a:xnack-', 'gfx90a:xnack+',
                      'gfx1030')

    variant('amdgpu_target', values=auto_or_any_combination_of(*amdgpu_targets))
    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3.10.2:', type='build', when='@4.5.0:')
    depends_on('cmake@3.5.1:', type='build')

    depends_on('googletest@1.10.0:', type='test')

    resource(name='hipRAND',
             git='https://github.com/ROCmSoftwarePlatform/hipRAND.git',
             branch='develop',
             destination='',
             placement='hiprand',
             when='@5.1.0')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0', '5.0.2',
                '5.1.0']:
        depends_on('hip@' + ver, when='@' + ver)
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)

    def patch(self):
        if self.spec.satisfies('@5.1.0:'):
            os.rmdir('hipRAND')
            os.rename('hiprand','hipRAND')
    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    @run_after('install')
    def fix_library_locations(self):
        """Fix the rocRAND and hipRAND libraries location"""
        # rocRAND installs librocrand.so* and libhiprand.so* to rocrand/lib and
        # hiprand/lib, respectively. This confuses spack's RPATH management. We
        # fix it by adding a symlink to the libraries.
        if self.spec.satisfies('@:5.0.2'):
            hiprand_lib_path = join_path(self.prefix, 'hiprand', 'lib')
            rocrand_lib_path = join_path(self.prefix, 'rocrand', 'lib')
            mkdirp(self.prefix.lib)
            with working_dir(hiprand_lib_path):
                hiprand_libs = glob.glob('*.so*')
                for lib in hiprand_libs:
                    os.symlink(join_path(hiprand_lib_path, lib),
                               join_path(self.prefix.lib, lib))
            with working_dir(rocrand_lib_path):
                rocrand_libs = glob.glob('*.so*')
                for lib in rocrand_libs:
                    os.symlink(join_path(rocrand_lib_path, lib),
                               join_path(self.prefix.lib, lib))
            """Fix the rocRAND and hipRAND include path"""
            # rocRAND installs irocrand*.h* and hiprand*.h* rocrand/include and
            # hiprand/include, respectively. This confuses spack's RPATH management. We
            # fix it by adding a symlink to the header files.
            hiprand_include_path = join_path(self.prefix, 'hiprand', 'include')
            rocrand_include_path = join_path(self.prefix, 'rocrand', 'include')

            with working_dir(hiprand_include_path):
                 hiprand_includes = glob.glob('*.h*')
            hiprand_path = join_path(self.prefix, 'hiprand')
            with working_dir(hiprand_path):
                for header_file in hiprand_includes:
                    os.symlink(join_path('include', header_file), header_file)
            with working_dir(rocrand_include_path):
                rocrand_includes = glob.glob('*.h*')
            rocrand_path = join_path(self.prefix, 'rocrand')
            with working_dir(rocrand_path):
                for header_file in rocrand_includes:
                    os.symlink(join_path('include', header_file), header_file)
        else:
            os.mkdir(os.path.join(self.prefix, 'hiprand'))
            os.mkdir(os.path.join(self.prefix, 'hiprand', 'include'))
            hiprand_include_path = join_path(self.prefix, 'include', 'hiprand')
            with working_dir(hiprand_include_path):
                 hiprand_includes = glob.glob('*.h*')
            hiprand_path = join_path(self.prefix, 'hiprand', 'include')
            with working_dir(hiprand_path):
                for header_file in hiprand_includes:
                    os.symlink(join_path('../../include/hiprand', header_file), header_file)


    def cmake_args(self):
        args = [
            self.define('BUILD_BENCHMARK', 'OFF'),
            self.define('BUILD_TEST', self.run_tests)
        ]

        if 'auto' not in self.spec.variants['amdgpu_target']:
            args.append(self.define_from_variant('AMDGPU_TARGETS', 'amdgpu_target'))

        if self.spec.satisfies('^cmake@3.21.0:3.21.2'):
            args.append(self.define('__skip_rocmclang', 'ON'))
        if '@5.1.0:' in self.spec:
            args.append(self.define('BUILD_HIPRAND', 'ON'))


        return args
