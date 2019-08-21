# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Zstd(MakefilePackage):
    """Zstandard, or zstd as short version, is a fast lossless compression
    algorithm, targeting real-time compression scenarios at zlib-level and
    better compression ratios."""

    homepage = "http://facebook.github.io/zstd/"
    url      = "https://github.com/facebook/zstd/archive/v1.4.2.tar.gz"

    version('1.4.2', sha256='7a6e1dad34054b35e2e847eb3289be8820a5d378228802239852f913c6dcf6a7')
    version('1.4.0', sha256='63be339137d2b683c6d19a9e34f4fb684790e864fee13c7dd40e197a64c705c1')
    version('1.3.8', sha256='90d902a1282cc4e197a8023b6d6e8d331c1fd1dfe60f7f8e4ee9da40da886dc3')
    version('1.3.0', '888660a850e33c2dcc7c4f9d0b04d347')
    version('1.1.2', '4c57a080d194bdaac83f2d3251fc7ffc')

    variant('pic', default=True, description='Build position independent code')

    def setup_environment(self, spack_env, run_env):
        if '+pic' in self.spec:
            spack_env.append_flags('CFLAGS', self.compiler.pic_flag)

    def build(self, spec, prefix):
        make('PREFIX={0}'.format(prefix))

    def install(self, spec, prefix):
        make('install', 'PREFIX={0}'.format(prefix))
