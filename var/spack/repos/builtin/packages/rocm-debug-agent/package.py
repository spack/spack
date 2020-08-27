# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocmDebugAgent(CMakePackage):
    """Radeon Open Compute (ROCm) debug agent"""

    homepage = "https://github.com/ROCm-Developer-Tools/rocr_debug_agent"
    url      = "https://github.com/ROCm-Developer-Tools/rocr_debug_agent/archive/roc-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='203ccb18d2ac508aae40bf364923f67375a08798b20057e574a0c5be8039f133')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    for ver in ['3.5.0']:
        depends_on('hsa-rocr-dev@' + ver, type='link', when='@' + ver)
        depends_on('hsakmt-roct@' + ver, type='link', when='@' + ver)
        depends_on("elfutils", type='link', when='@' + ver)

    root_cmakelists_dir = 'src'

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DCMAKE_PREFIX_PATH={0}/include/hsa;{1}/include,'.
            format(spec['hsa-rocr-dev'].prefix, spec['hsakmt-roct'].prefix)
        ]
        return args
