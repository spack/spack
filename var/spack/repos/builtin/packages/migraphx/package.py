# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Migraphx(CMakePackage):
    """ AMD's graph optimization engine."""

    homepage = "https://github.com/ROCmSoftwarePlatform/AMDMIGraphX"
    url = "https://github.com/ROCmSoftwarePlatform/AMDMIGraphX/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    def url_for_version(self, version):
        url = "https://github.com/ROCmSoftwarePlatform/AMDMIGraphX/archive/{0}.tar.gz"
        if version > Version('3.5'):
            return url.format(version)
        else:
            return url.format('rocm-' + version)

    version('3.8.0', sha256='08fa991349a2b95364b0a69be7960580c3e3fde2fda0f0c67bc41429ea2d67a0')
    version('3.7.0', sha256='697c3c7babaa025eaabec630dbd8a87d10dc4fe35fafa3b0d3463aaf1fc46399')
    version('3.5.0', sha256='5766f3b262468c500be5051a056811a8edfa741734a5c08c4ecb0337b7906377')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('protobuf', type='link')
    depends_on('blaze', type='build')
    depends_on('nlohmann-json', type='link')
    depends_on('py-pybind11', type='build')
    depends_on('msgpack-c', type='link')
    depends_on('half@1.12.0', type='link')
    for ver in ['3.5.0', '3.7.0', '3.8.0']:
        depends_on('hip@' + ver, type='build', when='@' + ver)
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)
        depends_on('llvm-amdgpu@' + ver, type='build', when='@' + ver)
        depends_on('rocblas@' + ver, type='link', when='@' + ver)
        depends_on('miopen-hip@' + ver, type='link', when='@' + ver)

    def cmake_args(self):
        args = [
            '-DCMAKE_CXX_COMPILER={0}/bin/clang++'
            .format(self.spec['llvm-amdgpu'].prefix)
        ]
        return args
