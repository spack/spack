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

    depends_on('cmake@3.5.2', type='build')
    depends_on('hsa-rocr-dev@3.5:', type='link', when='@3.5:')
    depends_on('hsakmt-roct@3.5:', type='link', when='@3.5:')
    depends_on("elfutils", type='link', when='@3.5:')
    root_cmakelists_dir= 'src'

    def cmake_args(self):
        spec=self.spec
        args = [
                '-DCMAKE_VERBOSE_MAKEFILE=1',
                '-DROCM_DIR={}'.format(spec['hsa-rocr-dev'].prefix),
                '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE',
                '-DCMAKE_PREFIX_PATH={}/include/hsa;{}/hsa/lib;{}/include;{}/lib,'.format(spec['hsa-rocr-dev'].prefix, spec['hsa-rocr-dev'].prefix, spec['hsakmt-roct'].prefix, spec['hsakmt-roct'].prefix)
               ]
        return args
