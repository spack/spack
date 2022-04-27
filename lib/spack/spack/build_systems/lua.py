# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
from typing import List, Text

from llnl.util.filesystem import find, join_path

from spack.directives import *
from spack.package import PackageBase
from spack.util.executable import Executable


class LuaPackage(PackageBase):
    """Specialized class for lua packages

    Note that there is also a LuaRocksPackage for the common case where luarocks is the
    build system"""

    phases = ['preprocess', 'install']
    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'LuaPackage'

    depends_on('lua-lang')
    extends('lua', when='^lua')
    extends('lua-luajit', when='^lua-luajit')
    depends_on('lua-luajit+lualinks', when='^lua-luajit')
    extends('lua-luajit-openresty', when='^lua-luajit-openresty')
    depends_on('lua-luajit-openresty+lualinks', when='^lua-luajit-openresty')

    rocks_build_flags = []  # type: List[Text]

    def preprocess(self, spec, prefix):
        """Extend this to preprocess source before building with luarocks"""
        pass

    @property
    def lua(self):
        return Executable(join_path(self.spec['lua-lang'].prefix.bin, 'lua'))

    @property
    def luarocks(self):
        return Executable(join_path(self.spec['lua-lang'].prefix.bin, 'luarocks'))

    def install(self, spec, prefix):
        rock = '.'
        if os.path.splitext(self.stage.archive_file)[1] == 'rock':
            rock = self.stage.archive_file
        else:
            specs = find('.', '*.rockspec', recursive=False)
            if specs:
                rock = specs[0]
        rocks_args = list(self.rocks_build_flags)
        rocks_args.append(rock)
        self.luarocks('--tree=' + prefix, 'build', *rocks_args)
