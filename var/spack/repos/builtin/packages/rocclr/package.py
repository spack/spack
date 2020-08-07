# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rocclr(CMakePackage):
    """ROCclr is a virtual device interface that compute runtimes interact
       with to different backends such as ROCr or PAL This abstraction allows
       runtimes to work on Windows as well as on Linux without much effort."""

    homepage = "https://github.com/ROCm-Developer-Tools/ROCclr"
    url      = "https://github.com/ROCm-Developer-Tools/ROCclr/archive/roc-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='87c1ee9f02b8aa487b628c543f058198767c474cec3d21700596a73c028959e1')

    depends_on('cmake@3:', type='build')
    for ver in ['3.5.0']:
        depends_on('hsakmt-roct@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('mesa~llvm@18.3:', type='link', when='@' + ver)

    patch('opengl.patch', when='@3.5.0')

    resource(name='opencl-on-vdi',
             url='https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/roc-3.5.0.tar.gz',
             sha256='511b617d5192f2d4893603c1a02402b2ac9556e9806ff09dd2a91d398abf39a0',
             expand=True,
             destination='',
             placement='opencl-on-vdi')

    @run_after('install')
    def deploy_missing_files(self):
        # the amdrocclr_staticTargets.cmake file is generated but not installed
        # and when we install it by hand, we have to fix the path to the static
        # library libamdrocclr_static.a from build dir to prefix lib dir.
        cmakefile = join_path(self.build_directory,
                              'amdrocclr_staticTargets.cmake')
        filter_file(self.build_directory, self.prefix.lib, cmakefile)
        install(cmakefile, self.prefix.lib)

    def cmake_args(self):
        args = [
            '-DUSE_COMGR_LIBRARY=yes',
            '-DOPENCL_DIR={0}/opencl-on-vdi'.format(self.stage.source_path)
        ]
        return args
