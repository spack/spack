# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RocmOpencl(CMakePackage):
    """OpenCL: Open Computing Language on ROCclr"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    def url_for_version(self, version):
        if version == Version('3.5.0'):
            return "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/roc-3.5.0.tar.gz"

        url = "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/rocm-{0}.tar.gz"
        return url.format(version)

    version('3.7.0', sha256='283e1dfe4c3d2e8af4d677ed3c20e975393cdb0856e3ccd77b9c7ed2a151650b')
    version('3.5.0', sha256='511b617d5192f2d4893603c1a02402b2ac9556e9806ff09dd2a91d398abf39a0')

    depends_on('cmake@3:', type='build')
    depends_on('mesa~llvm@18.3:', type='link')
    for ver in ['3.5.0', '3.7.0']:
        depends_on('rocclr@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='build', when='@' + ver)

    def flag_handler(self, name, flags):
        # The includes are messed up in ROCm 3.5.0:
        # ROCM-OpenCL-Runtime uses flat includes
        # and the find_package(ROCclr) bit it
        # commented out. So instead we provide
        # all the includes...

        if name in ('cflags', 'cxxflags'):
            rocclr = self.spec['rocclr'].prefix.include
            extra_includes = [
                'include',
                'compiler/lib',
                'compiler/lib/include',
                'elf/utils/libelf',
                'elf/utils/common'
            ]

            for p in extra_includes:
                flag = '-I {0}'.format(join_path(rocclr, p))
                flags.append(flag)

        return (flags, None, None)

    def cmake_args(self):

        args = [
            '-DUSE_COMGR_LIBRARY=yes',
            '-DROCclr_DIR={0}'.format(self.spec['rocclr'].prefix),
            '-DLIBROCclr_STATIC_DIR={0}/lib'.format(self.spec['rocclr'].prefix)
        ]
        return args
