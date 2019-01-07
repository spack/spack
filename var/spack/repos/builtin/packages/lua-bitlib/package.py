# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class LuaBitlib(Package):
    """Lua-jit-like bitwise operations for lua"""

    homepage = "http://luaforge.net/projects/bitlib"
    url      = "https://luarocks.org/bitlib-23-2.src.rock"

    version('23', '9fee36a6e512c54bf6364dfe97d1d871',
            url="https://luarocks.org/bitlib-23-2.src.rock",
            expand=False)

    extends('lua')

    def install(self, spec, prefix):
        luarocks('unpack', "bitlib-23-2.src.rock")
        os.chdir(os.path.join('bitlib-23-2', 'bitlib-23'))
        sed = which('sed')
        sed('-ie', 's/luaL_reg/luaL_Reg/', 'lbitlib.c')
        luarocks('--tree=' + prefix, 'make')
