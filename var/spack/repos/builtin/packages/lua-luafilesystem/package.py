# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LuaLuafilesystem(LuaPackage):
    """LuaFileSystem is a Lua library developed to complement the set of
    functions related to file systems offered by the standard Lua distribution.

    LuaFileSystem offers a portable way to access the underlying directory
    structure and file attributes.

    LuaFileSystem is free software and uses the same license as Lua 5.1
    """

    homepage = 'http://keplerproject.github.io/luafilesystem'
    url = 'https://github.com/keplerproject/luafilesystem/archive/v1_6_3.tar.gz'

    version('1_8_0', sha256='16d17c788b8093f2047325343f5e9b74cccb1ea96001e45914a58bbae8932495')
    version('1_7_0_2', sha256='23b4883aeb4fb90b2d0f338659f33a631f9df7a7e67c54115775a77d4ac3cc59')
    version('1_6_3', sha256='11c7b1fc2e560c0a521246b84e6257138d97dddde5a19e405714dbabcb9436ca')
