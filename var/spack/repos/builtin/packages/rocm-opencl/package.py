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
    depends_on('cmake@3:', type='build')
    depends_on('rocclr@3.5.0', type='build', when='@3.5.0')
    depends_on('comgr@3.5.0', type='build', when='@3.5.0')
    depends_on('mesa~llvm@18.3:', type='link')

    def flag_handler(self, name, flags):
        # The includes are messed up in ROCm 3.5.0:
        # ROCM-OpenCL-Runtime uses flat includes
        # and the find_package(ROCclr) bit it
        # commented out. So instead we provide
        # all the includes...

        if self.spec.satisfies('@3.5.0') and name in ('cflags', 'cxxflags'):
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
