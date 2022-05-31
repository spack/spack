# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class MiopenTensile(CMakePackage):
    """MIOpenTensile provides host-callable interfaces to Tensile library.
       MIOpenTensile supports one programming model: HIP"""

    homepage = "https://github.com/ROCmSoftwarePlatform/MIOpenTensile"
    git = "https://github.com/ROCmSoftwarePlatform/MIOpenTensile.git"
    url      = "https://github.com/ROCmSoftwarePlatform/MIOpentensile/archive/rocm-5.0.0.tar.gz"

    maintainers = ['srekolam']

    version('5.1.0', sha256='f1ae57bd4df8c154357b3f17caf0cfd5f80ba16ffff67bf6219a56f1eb5f897d')
    version('5.0.2', sha256='7b85a6a37d0905b0a3baa8361fd71a5a32ad90f3a562fd5e1af7e2ba68099fa6')
    version('5.0.0', sha256='276ada52e2e8431851296a60df538e0171f8a1c4e9894de8954ffa9306cda2d8')
    version('4.5.2', sha256='eae14b20aec5ad57815c85d0571b7aecc3704696147f3cdbe34287e88da0c9e9')
    version('4.5.0', sha256='5f181f536040c0612bf889600f75951e7ec031ae5c4cb9c2c44f6ac3b15b004b')

    tensile_architecture = ('all', 'gfx906', 'gfx908', 'gfx803', 'gfx900')

    variant('tensile_architecture', default='all', values=tensile_architecture, multi=True)
    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    patch('0002-Improve-compilation-by-using-local-tensile-path.patch', when='@4.5.0:')

    depends_on('cmake@3.5:', type='build')
    depends_on('msgpack-c@3:')
    depends_on('python@3.6:', type='build')
    depends_on('py-virtualenv', type='build')
    depends_on('perl-file-which', type='build')
    depends_on('py-pyyaml', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-msgpack', type='build')
    depends_on('py-pip', type='build')

    resource(name='Tensile',
             git='https://github.com/ROCmSoftwarePlatform/Tensile.git',
             commit='9cbabb07f81e932b9c98bf5ae48fbd7fcef615cf',
             when='@4.5.0:')

    for ver in ['4.5.0', '4.5.2', '5.0.0', '5.0.2', '5.1.0']:
        depends_on('rocm-cmake@%s:' % ver, type='build', when='@' + ver)
        depends_on('hip@' + ver,                      when='@' + ver)
        depends_on('llvm-amdgpu@' + ver,              when='@' + ver)
        depends_on('rocminfo@' + ver,                 when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        arch = self.spec.variants['tensile_architecture'].value
        tensile_path = join_path(self.stage.source_path, 'Tensile')
        args = [
            self.define('TENSILE_USE_MSGPACK', 'ON'),
            self.define('COMPILER', 'hipcc'),
            self.define('TENSILE_USE_LLVM', 'OFF'),
            self.define('CODE_OBJECT_VERSION', 'V3'),
            self.define('TENSILE_LIBRARY_FORMAT', 'msgpack'),
            self.define('MIOPEN_TENSILE_SRC', 'asm_full'),
            self.define('Tensile_TEST_LOCAL_PATH', tensile_path)
        ]
        args.append(self.define('Tensile_ARCHITECTURE', arch))

        return args
