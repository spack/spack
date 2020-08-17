# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class LuaJit(MakefilePackage):
    """LuaJIT is a Just-In-Time Compiler (JIT) for the Lua programming
    language. Lua is a powerful, dynamic and light-weight programming
    language. It may be embedded or used as a general-purpose,
    stand-alone language. """

    homepage = "http://luajit.org/luajit.html"
    url      = "http://luajit.org/download/LuaJIT-2.1.0-beta3.tar.gz"

    version('2.1.0-beta3', sha256='1ad2e34b111c802f9d0cdf019e986909123237a28c746b21295b63c9e785d9c3')
    version('2.0.5', sha256='874b1f8297c697821f561f9b73b57ffd419ed8f4278c82e05b48806d30c1e979', preferred=True)

    conflicts('@:2.0.5', when='target=aarch64:')
    depends_on('lua', type='link')

    @property
    def headers(self):
        hdrs = find_headers('luajit', self.prefix.include, recursive=True)
        hdrs.directories = os.path.dirname(hdrs[0])
        return hdrs or None

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('PREFIX= .*', 'PREFIX = {0}'.format(prefix))
        src_makefile = FileFilter(join_path('src', 'Makefile'))
        src_makefile.filter(
            '^DEFAULT_CC = .*',
            'DEFAULT_CC = {0}'.format(spack_cc))
        src_makefile.filter(
            '^DYNAMIC_CC = .*',
            'DYNAMIC_CC = $(CC) {0}'.format(self.compiler.cc_pic_flag))
