# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack import *


class CBlosc(CMakePackage):
    """Blosc, an extremely fast, multi-threaded, meta-compressor library"""
    homepage = "http://www.blosc.org"
    url      = "https://github.com/Blosc/c-blosc/archive/v1.11.1.tar.gz"

    version('1.12.1', '6fa4ecb7ef70803a190dd386bf4a2e93')
    version('1.11.1', 'e236550640afa50155f3881f2d300206')
    version('1.9.2',  'dd2d83069d74b36b8093f1c6b49defc5')
    version('1.9.1',  '7d708d3daadfacf984a87b71b1734ce2')
    version('1.9.0',  'e4c1dc8e2c468e5cfa2bf05eeee5357a')
    version('1.8.1',  'd73d5be01359cf271e9386c90dcf5b05')
    version('1.8.0',  '5b92ecb287695ba20cc33d30bf221c4f')

    variant('avx2', default=True, description='Enable AVX2 support')

    depends_on('cmake@2.8.10:', type='build')
    depends_on('snappy')
    depends_on('zlib')
    depends_on('zstd')
    depends_on('lz4')

    def cmake_args(self):
        args = []

        if '+avx2' in self.spec:
            args.append('-DDEACTIVATE_AVX2=OFF')
        else:
            args.append('-DDEACTIVATE_AVX2=ON')

        if self.spec.satisfies('@1.12.0:'):
            args.append('-DPREFER_EXTERNAL_SNAPPY=ON')
            args.append('-DPREFER_EXTERNAL_ZLIB=ON')
            args.append('-DPREFER_EXTERNAL_ZSTD=ON')
            args.append('-DPREFER_EXTERNAL_LZ4=ON')

        return args

    @run_after('install')
    def darwin_fix(self):
        if sys.platform == 'darwin':
            fix_darwin_install_name(self.prefix.lib)
