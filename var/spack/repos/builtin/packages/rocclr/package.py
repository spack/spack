# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os
import shutil

class Rocclr(CMakePackage):
    """ROCclr is a virtual device interface that compute runtimes interact with to different backends such as ROCr or PAL This abstraction allows runtimes to work on Windows as well as on Linux without much effort."""

    homepage = "https://github.com/ROCm-Developer-Tools/ROCclr"
    url      = "https://github.com/ROCm-Developer-Tools/ROCclr/archive/roc-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='87c1ee9f02b8aa487b628c543f058198767c474cec3d21700596a73c028959e1')

    depends_on('cmake@3.5.2', type='build')
    depends_on('hsakmt-roct@3.5.0:', type='build', when='@3.5:')
    depends_on('hsa-rocr-dev@3.5.0:', type='build', when='@3.5:')
    depends_on('comgr@3.5.0:', type='build', when='@3.5:')
    depends_on('mesa~llvm@18.3:', type='link', when='@3.5:')

    resource(name='opencl-on-vdi',
             url='https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/roc-3.5.0.tar.gz',
             sha256='511b617d5192f2d4893603c1a02402b2ac9556e9806ff09dd2a91d398abf39a0',
             expand=True,
             destination='',
             placement='opencl-on-vdi')
    build_directory = '../../rocclr_build'

    @run_before('cmake')
    def buildcleanup(self):
        build_path=os.path.join(self.stage.path, '../rocclr_build')
        shutil.rmtree(build_path, ignore_errors=True)

    def cmake_args(self):
        args = ['-DUSE_COMGR_LIBRARY=yes',
                '-DOPENCL_DIR={}/opencl-on-vdi'.format(self.stage.source_path)]
        return args

