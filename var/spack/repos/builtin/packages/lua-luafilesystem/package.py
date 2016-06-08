##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
    """
    LuaFileSystem is a Lua library developed to complement the set of functions related to file
    systems offered by the standard Lua distribution.

    LuaFileSystem offers a portable way to access the underlying directory structure and file attributes. LuaFileSystem
    is free software and uses the same license as Lua 5.1
    """
    homepage = 'http://keplerproject.github.io/luafilesystem'
    url = 'https://github.com/keplerproject/luafilesystem/archive/v_1_6_3.tar.gz'

    version('1_6_3', 'd0552c7e5a082f5bb2865af63fb9dc95')

    extends('lua')

    def install(self, spec, prefix):
        version = self.spec.version
        rockspec_format = join_path(self.stage.path, 'luafilesystem-v_{version.underscored}', 'rockspecs', 'luafilesystem-{version.dotted}-1.rockspec')
        luarocks('--tree=' + prefix, 'install', rockspec_format.format(version=self.spec.version))