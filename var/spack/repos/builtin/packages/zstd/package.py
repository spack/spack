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
    url      = "https://github.com/facebook/zstd/archive/v1.1.2.tar.gz"

    version('1.3.8', '90d902a1282cc4e197a8023b6d6e8d331c1fd1dfe60f7f8e4ee9da40da886dc3')
    version('1.3.0', '888660a850e33c2dcc7c4f9d0b04d347')
    version('1.1.2', '4c57a080d194bdaac83f2d3251fc7ffc')

    variant('pic', default=True, description='Build position independent code')

    def setup_environment(self, spack_env, run_env):
        if '+pic' in self.spec:
            spack_env.append_flags('CFLAGS', self.compiler.pic_flag)

    def install(self, spec, prefix):
        make('install', 'PREFIX={0}'.format(prefix))
