##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
