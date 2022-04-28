# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from llnl.util.filesystem import find, join_path

from spack.directives import depends_on, extends
from spack.package import PackageBase, run_before
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
    depends_on('luajit', when='^lua-luajit')
    depends_on('luajit', when='^lua-luajit-openresty')
    depends_on('lua-luajit+lualinks', when='^lua-luajit')
    extends('lua-luajit-openresty', when='^lua-luajit-openresty')
    depends_on('lua-luajit-openresty+lualinks', when='^lua-luajit-openresty')

    def unpack(self, spec, prefix):
        if os.path.splitext(self.stage.archive_file)[1] == '.rock':
            directory = self.luarocks('unpack', self.stage.archive_file, output=str)
            dirlines = directory.split('\n')
            os.chdir(dirlines[2])

    def _generate_tree_line(self, name, prefix):
        return """{{ name = "{name}", root = "{prefix}" }};""".format(
            name=name,
            prefix=prefix,
        )

    def _luarocks_config_path(self):
        return os.path.join(self.stage.source_path, 'spack_luarocks.lua')

    @run_before("preprocess")
    def _generate_luarocks_config(self):
        spec = self.spec
        prefix = self.prefix
        table_entries = []
        for d in spec.traverse(
                deptypes=("build", "run"), deptype_query="run"
        ):
            if d.package.extends(self.extendee_spec):
                table_entries.append(self._generate_tree_line(d.name, d.prefix))

        path = self._luarocks_config_path()
        with open(path, 'w') as config:
            config.write(
                """
                deps_mode="all"
                rocks_trees={{
                {}
                }}
                """.format(
                    "\n".join(table_entries)
                )
            )
        return path

    def setup_build_environment(self, env):
        env.set('LUAROCKS_CONFIG', self._luarocks_config_path())

    def preprocess(self, spec, prefix):
        """Override this to preprocess source before building with luarocks"""
        pass

    @property
    def lua(self):
        return Executable(self.spec['lua-lang'].prefix.bin.lua)

    @property
    def luarocks(self):
        lr = Executable(self.spec['lua-lang'].prefix.bin.luarocks)
        return lr

    def luarocks_args(self):
        return []

    def install(self, spec, prefix):
        rock = '.'
        specs = find('.', '*.rockspec', recursive=False)
        if specs:
            rock = specs[0]
        rocks_args = self.luarocks_args()
        rocks_args.append(rock)
        self.luarocks('--tree=' + prefix, 'make', *rocks_args)
