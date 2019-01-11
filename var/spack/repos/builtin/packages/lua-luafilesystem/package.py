# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LuaLuafilesystem(Package):
    """LuaFileSystem is a Lua library developed to complement the set of
    functions related to file systems offered by the standard Lua distribution.

    LuaFileSystem offers a portable way to access the underlying directory
    structure and file attributes.

    LuaFileSystem is free software and uses the same license as Lua 5.1
    """

    homepage = 'http://keplerproject.github.io/luafilesystem'
    url = 'https://github.com/keplerproject/luafilesystem/archive/v1_6_3.tar.gz'

    version('1_6_3', 'bed11874cfded8b4beed7dd054127b24')

    # The version constraint here comes from this post:
    #
    # https://www.perforce.com/blog/git-beyond-basics-using-shallow-clones
    #
    # where it is claimed that full shallow clone support was added @1.9
    depends_on('git@1.9.0:', type='build')
    extends('lua')

    def install(self, spec, prefix):
        rockspec_fmt = join_path(self.stage.path,
                                 'luafilesystem-{version.underscored}',
                                 'rockspecs',
                                 'luafilesystem-{version.dotted}-1.rockspec')
        luarocks('--tree=' + prefix, 'install',
                 rockspec_fmt.format(version=self.spec.version))
