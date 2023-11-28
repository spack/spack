# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.builtin.lua import LuaImplPackage


class LuaLuajitOpenresty(LuaImplPackage):
    """Flast flexible JITed lua - OpenResty maintained fork"""

    homepage = "https://openresty.org/en/luajit.html"
    url = "https://github.com/openresty/luajit2/archive/refs/tags/v2.1-20230410.tar.gz"

    version(
        "2.1-20220111", sha256="1ad2e34b111c802f9d0cdf019e986909123237a28c746b21295b63c9e785d9c3"
    )
    version(
        "2.1-20230410", sha256="77bbcbb24c3c78f51560017288f3118d995fe71240aa379f5818ff6b166712ff"
    )

    variant(
        "lualinks",
        default=True,
        description="add symlinks to make lua-luajit a drop-in lua replacement",
    )

    provides("luajit", "lua-lang@5.1", when="+lualinks")
    lua_version_override = "5.1"

    @run_after("install")
    def install_links(self):
        self.symlink_luajit()

    @property
    def headers(self):
        hdrs = find_headers("luajit", self.prefix.include, recursive=True)
        hdrs.directories = os.path.dirname(hdrs[0])
        return hdrs or None

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("PREFIX= .*", "PREFIX = {0}".format(prefix))
        src_makefile = FileFilter(join_path("src", "Makefile"))
        src_makefile.filter("^DEFAULT_CC = .*", "DEFAULT_CC = {0}".format(spack_cc))
        src_makefile.filter(
            "^DYNAMIC_CC = .*", "DYNAMIC_CC = $(CC) {0}".format(self.compiler.cc_pic_flag)
        )
        # Catalina and higher produce a non-functional luajit unless this is set
        if spec.satisfies("platform=darwin"):
            src_makefile.filter(
                "^.XCFLAGS.= -DLUAJIT_ENABLE_GC64", "XCFLAGS+= -DLUAJIT_ENABLE_GC64"
            )
        # Linking with the C++ compiler is a dirty hack to deal with the fact
        # that unwinding symbols are not included by libc, this is necessary
        # on some platforms for the final link stage to work
        src_makefile.filter("^TARGET_LD = .*", "TARGET_LD = {0}".format(spack_cxx))
