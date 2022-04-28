# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from llnl.util.filesystem import find, join_path
import llnl.util.tty as tty

from spack.directives import depends_on, extends
from spack.package import PackageBase
from spack.util.executable import Executable


class LuaPackage(PackageBase):
    """Specialized class for lua packages"""

    phases = ['unpack', 'preprocess', 'install']
    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'LuaPackage'

    list_depth = 1  # LuaRocks requires at least one level of spidering to find versions
    depends_on('lua-lang')
    extends('lua', when='^lua')
    extends('lua-luajit', when='^lua-luajit')
    depends_on('lua-luajit+lualinks', when='^lua-luajit')
    extends('lua-luajit-openresty', when='^lua-luajit-openresty')
    depends_on('lua-luajit-openresty+lualinks', when='^lua-luajit-openresty')

    def unpack(self, spec, prefix):
        if os.path.splitext(self.stage.archive_file)[1] == '.rock':
            directory = self.luarocks('unpack', self.stage.archive_file, output=str)
            tty.debug(directory)
            dirlines = directory.split('\n')
            tty.debug(dirlines)
            os.chdir(dirlines[2])

    def preprocess(self, spec, prefix):
        """Override this to preprocess source before building with luarocks"""
        pass

    @property
    def lua(self):
        return Executable(self.spec['lua-lang'].prefix.bin.lua)

    @property
    def luarocks(self):
        return Executable(self.spec['lua-lang'].prefix.bin.luarocks)

    def luarocks_args(self):
        return []

    def install(self, spec, prefix):
        rock = '.'
        specs = find('.', '*.rockspec', recursive=False)
        cmd = 'make'
        if specs:
            rock = specs[0]
        rocks_args = self.luarocks_args()
        rocks_args.append(rock)
        self.luarocks('--tree=' + prefix, cmd, *rocks_args)
