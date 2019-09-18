# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob


class LuaLuaposix(Package):
    """Lua posix bindings, including ncurses"""
    homepage = "https://github.com/luaposix/luaposix/"
    url      = "https://github.com/luaposix/luaposix/archive/release-v33.4.0.tar.gz"

    version('33.4.0', 'b36ff049095f28752caeb0b46144516c')

    extends("lua")

    def install(self, spec, prefix):
        rockspec = glob.glob('luaposix-*.rockspec')
        luarocks('--tree=' + prefix, 'make', rockspec[0])
