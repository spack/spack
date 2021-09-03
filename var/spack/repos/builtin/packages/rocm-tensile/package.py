# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocmTensile(CMakePackage):
    """Radeon Open Compute Tensile library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/Tensile/"
    git      = "https://github.com/ROCmSoftwarePlatform/Tensile.git"
    url      = "https://github.com/ROCmSoftwarePlatform/Tensile/archive/rocm-4.3.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']

    version('4.3.1', sha256='6fce0ac22051a454fe984283766eb473dc50752cd30bad05acb3dbde6ef4f8b1')
    version('4.3.0', sha256='911c0cdb0146d43a2a59170e6a803f414a2b68df7d9ff369ab784d11a08d7264')
    version('4.2.0', sha256='198e357a14a79366b27b1097856d4821996bc36163be0cd2668910b253721060')
    version('4.1.0', sha256='92b8ee13dfc11a67d5136227ee985622685790fd3f0f0e1ec6db411d4e9a3419')
    version('4.0.0', sha256='cf105ce8c3e352d19713b3bf8bda77f25c1a692c4f2ca82d631ba15523ecc1cd')
    version('3.10.0', sha256='8d5b50aadfa56a9195e4c387b8eb351c9b9b7671b136b624e07fe28db24bd330')
    version('3.9.0', sha256='17a011f8c3433d4f8c2dddabd5854cf96c406d24592b3942deb51672c570882e')
    version('3.8.0', sha256='c78a11db85fdf54bfd26533ee6fa98f6a6e789fa423537993061497ac5f22ed6')
    version('3.7.0', sha256='488a7f76ea42a7601d0557f53068ec4832a2c7c06bb1b511470a4e35599a5a4d')
    version('3.5.0', sha256='71eb3eed6625b08a4cedb539dd9b596e3d4cc82a1a8063d37d94c0765b6f8257')

    tensile_architecture = ('all', 'gfx803', 'gfx900', 'gfx906', 'gfx908')

    variant('tensile_architecture', default='all', values=tensile_architecture, multi=False)
    variant('openmp', default=True, description='Enable OpenMP')

    depends_on('cmake@3:', type='build')
    # This is the default library format since 3.7.0
    depends_on('msgpack-c@3:', when='@3.7:')
    depends_on('boost', type=('build', 'link'))

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1']:
        depends_on('rocm-cmake@' + ver, type='build',  when='@' + ver)
        depends_on('hip@' + ver,                       when='@' + ver)
        depends_on('comgr@' + ver,                     when='@' + ver)
        depends_on('llvm-amdgpu@' + ver,               when='@' + ver + '+openmp')
        depends_on('llvm-amdgpu@' + ver + '~openmp',   when='@' + ver + '~openmp')
        depends_on('rocminfo@' + ver,    type='build', when='@' + ver)

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0']:
        depends_on('rocm-smi@' + ver, type='build', when='@' + ver)

    for ver in ['4.0.0', '4.1.0', '4.2.0', '4.3.0', '4.3.1']:
        depends_on('rocm-smi-lib@' + ver, type='build', when='@' + ver)

    root_cmakelists_dir = 'Tensile/Source'
    # Status: https://github.com/ROCmSoftwarePlatform/Tensile/commit/a488f7dadba34f84b9658ba92ce9ec5a0615a087
    # Not yet landed in 3.7.0, nor 3.8.0.
    patch('0001-fix-compile-error.patch', when='@3.7.0:3.8.0')
    patch('0002-require-openmp-when-tensile-use-openmp-is-on.patch', when='@3.9.0:4.0.0')

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        arch = self.spec.variants['tensile_architecture'].value
        args = [
            self.define('amd_comgr_DIR', self.spec['comgr'].prefix),
            self.define('Tensile_COMPILER', 'hipcc'),
            self.define('Tensile_LOGIC', 'asm_full'),
            self.define('Tensile_CODE_OBJECT_VERSION', 'V3'),
            self.define('Boost_USE_STATIC_LIBS', 'OFF'),
            self.define('TENSILE_USE_OPENMP', 'ON'),
            self.define(
                'BUILD_WITH_TENSILE_HOST',
                'ON' if '@3.7.0:' in self.spec else 'OFF'
            )
        ]

        if '@3.7.0:' in self.spec:
            args.append(self.define('Tensile_LIBRARY_FORMAT', 'msgpack'))

        if self.spec.satisfies('@4.1.0:'):
            if arch == 'gfx906' or arch == 'gfx908':
                arch = arch + ':xnack-'
        args.append(self.define('Tensile_ARCHITECTURE', arch))

        if self.spec.satisfies('^cmake@3.21:'):
            args.append(self.define('__skip_rocmclang', 'ON'))

        return args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            install_tree('./client', prefix.client)
            install_tree('./lib', prefix.lib)
