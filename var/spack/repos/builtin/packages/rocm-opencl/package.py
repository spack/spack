# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RocmOpencl(CMakePackage):
    """OpenCL: Open Computing Language on ROCclr"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime"
    url      = "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/roc-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='511b617d5192f2d4893603c1a02402b2ac9556e9806ff09dd2a91d398abf39a0')
    depends_on('cmake@3.5.2', type='build')
    depends_on('rocclr@3.5.0:', type='build', when='@3.5.0:')
    depends_on('comgr@3.5.0:', type='build', when='@3.5.0:')
    depends_on('mesa~llvm@18.3:', type='link', when='@3.5:')

    resource(name='rocclr',
             url='https://github.com/ROCm-Developer-Tools/ROCclr/archive/roc-3.5.0.tar.gz',
             sha256='87c1ee9f02b8aa487b628c543f058198767c474cec3d21700596a73c028959e1',
             expand=True,
             destination='',
             placement='rocclr-src')

    def cmake_args(self):
        args = ['-DLIBROCclr_STATIC_DIR={}/../rocclr_build'.format(self.stage.path),
                '-DUSE_COMGR_LIBRARY=yes',
                '-DCMAKE_BUILD_WITH_INSTALL_RPATH=TRUE',
                '-DCMAKE_SKIP_BUILD_RPATH=TRUE',
                '-DROCclr_DIR={}/rocclr-src'.format(self.stage.source_path)
               ]
        return args
