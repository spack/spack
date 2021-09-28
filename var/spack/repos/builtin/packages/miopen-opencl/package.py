# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class MiopenOpencl(CMakePackage):
    """AMD's library for high performance machine learning primitives."""

    homepage = "https://github.com/ROCmSoftwarePlatform/MIOpen"
    git = "https://github.com/ROCmSoftwarePlatform/MIOpen.git"
    url = "https://github.com/ROCmSoftwarePlatform/MIOpen/archive/rocm-4.3.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('4.3.1', sha256='1fb2fd8b24f984174ec5338a58b7964e128b74dafb101373a41c8ed33955251a')
    version('4.3.0', sha256='034445470cfd44480a1d9854f9fdfe92cfb8efa3f002dee508eb9585e338486d')
    version('4.2.0', sha256='8ab02e784c8b3471159794766ed6303c333b33c69dc5186c0930e56504373b7c')
    version('4.1.0', sha256='068b1bc33f90fe21d3aab5697d2b3b7b930e613c54d6c5ee820768579b2b41ee')
    version('4.0.0', sha256='84c6c17be9c1a9cd0d3a2af283433f64b07a4b9941349f498e40fed82fb205a6')
    version('3.10.0', sha256='926e43c5583cf70d6b247f9fe45971b8b1cc9668f9c8490c142c7e8b6e268f1a')
    version('3.9.0', sha256='f57d75a220c1094395cc1dccab2185c759d779751ddbb5369a6f041ec77b2156')
    version('3.8.0', sha256='612b30d4a967bf18c7fa7aa3ef12ed558314ed04cee2775b842bf6a96cd7276f')
    version('3.7.0', sha256='f6a6ddd8d39bb76b7f7d91e68ade3b45e0201181145658c43b967065a354b103')
    version('3.5.0', sha256='aa362e69c4dce7f5751f0ee04c745735ea5454c8101050e9b92cc60fa3c0fb82')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('boost@1.67.0:1.73.0', type='link')
    depends_on('pkgconfig', type='build')
    depends_on('bzip2', type='link')
    depends_on('sqlite', type='link')
    depends_on('half', type='build')

    depends_on('miopengemm@1.1.6', type='link', when='@3.5.0')
    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1']:
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)
        depends_on('hip@' + ver,                      when='@' + ver)
        depends_on('rocm-opencl@' + ver,              when='@' + ver)

    for ver in ['3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1']:
        depends_on('miopengemm@' + ver, when='@' + ver)

    def cmake_args(self):
        args = [
            self.define('MIOPEN_BACKEND', 'OpenCL'),
            self.define(
                'MIOPEN_HIP_COMPILER',
                '{0}/bin/clang++'.format(self.spec['llvm-amdgpu'].prefix)
            ),
            self.define(
                'HIP_CXX_COMPILER',
                '{0}/bin/clang++'.format(self.spec['llvm-amdgpu'].prefix)
            ),
            self.define(
                'MIOPEN_AMDGCN_ASSEMBLER',
                '{0}/bin/clang'.format(self.spec['llvm-amdgpu'].prefix)
            ),
            self.define('Boost_USE_STATIC_LIBS', 'Off')
        ]
        return args
