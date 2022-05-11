# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.util.package import *


class LuaLuajit(MakefilePackage):
    """Flast flexible JITed lua"""
    homepage = "https://www.luajit.org"
    url      = "https://luajit.org/download/LuaJIT-2.0.5.tar.gz"

    version('2.1.0-beta3', sha256='1ad2e34b111c802f9d0cdf019e986909123237a28c746b21295b63c9e785d9c3')
    version('2.0.5', sha256='874b1f8297c697821f561f9b73b57ffd419ed8f4278c82e05b48806d30c1e979', preferred=True)
    version('2.0.4', sha256='620fa4eb12375021bef6e4f237cbd2dd5d49e56beb414bee052c746beef1807d')

    conflicts('@:2.0.5', when='target=aarch64:')

    variant('lualinks', default=False, description="add symlinks to make lua-luajit a drop-in lua replacement")

    provides("lua-lang", when="+lualinks")

    @run_after("install")
    def install_links(self):
        if not self.spec.satisfies("+lualinks"):
            return

        with working_dir(self.prefix.bin):
            luajit = os.readlink(self.prefix.bin.luajit)
            symlink(luajit, "lua")

        with working_dir(self.prefix.include):
            luajit_include_subdirs = glob.glob(
                os.path.join(self.prefix.include, "luajit*"))
            assert len(luajit_include_subdirs) == 1
            symlink(luajit_include_subdirs[0], "lua")

        with working_dir(self.prefix.lib):
            luajit_libnames = glob.glob(
                os.path.join(self.prefix.lib, "libluajit*.so*"))
            real_lib = next(
                lib for lib in luajit_libnames
                if os.path.isfile(lib) and not os.path.islink(lib)
            )
            symlink(real_lib, "liblua.so")

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
        # Linking with the C++ compiler is a dirty hack to deal with the fact
        # that unwinding symbols are not included by libc, this is necessary
        # on some platforms for the final link stage to work
        src_makefile.filter(
            '^TARGET_LD = .*',
            'TARGET_LD = {0}'.format(spack_cxx))
