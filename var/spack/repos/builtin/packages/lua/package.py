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
import os


class Lua(Package):
    """The Lua programming language interpreter and library."""

    homepage = "http://www.lua.org"
    url = "http://www.lua.org/ftp/lua-5.3.4.tar.gz"

    version('5.3.4', '53a9c68bcc0eda58bdc2095ad5cdfc63')
    version('5.3.2', '33278c2ab5ee3c1a875be8d55c1ca2a1')
    version('5.3.1', '797adacada8d85761c079390ff1d9961')
    version('5.3.0', 'a1b0a7e92d0c85bbff7a8d27bf29f8af')
    version('5.2.4', '913fdb32207046b273fdb17aad70be13')
    version('5.2.3', 'dc7f94ec6ff15c985d2d6ad0f1b35654')
    version('5.2.2', 'efbb645e897eae37cad4344ce8b0a614')
    version('5.2.1', 'ae08f641b45d737d12d30291a5e5f6e3')
    version('5.2.0', 'f1ea831f397214bae8a265995ab1a93e')
    version('5.1.5', '2e115fe26e435e33b0d5c022e4490567')
    version('5.1.4', 'd0870f2de55d59c1c8419f36e8fac150')
    version('5.1.3', 'a70a8dfaa150e047866dc01a46272599')

    extendable = True

    depends_on('ncurses')
    depends_on('readline')
    # luarocks needs unzip for some packages (e.g. lua-luaposix)
    depends_on('unzip', type='run')

    resource(
        name="luarocks",
        url="https://keplerproject.github.io/luarocks/releases/"
        "luarocks-2.3.0.tar.gz",
        md5="a38126684cf42b7d0e7a3c7cf485defb",
        destination="luarocks",
        placement='luarocks')

    def install(self, spec, prefix):
        if spec.satisfies("platform=darwin"):
            target = 'macosx'
        else:
            target = 'linux'
        make('INSTALL_TOP=%s' % prefix,
             'MYLDFLAGS=-L%s -L%s' % (
                 spec['readline'].prefix.lib,
                 spec['ncurses'].prefix.lib),
             'MYLIBS=-lncursesw',
             'CC=%s -std=gnu99 %s' % (spack_cc,
                                      self.compiler.pic_flag),
             target)
        make('INSTALL_TOP=%s' % prefix,
             'install')

        static_to_shared_library(join_path(prefix.lib, 'liblua.a'),
                                 arguments=['-lm'], version=self.version,
                                 compat_version=self.version.up_to(2))

        # compatibility with ax_lua.m4 from autoconf-archive
        # https://www.gnu.org/software/autoconf-archive/ax_lua.html
        with working_dir(prefix.lib):
            # e.g., liblua.so.5.1.5
            src_path = 'liblua.{0}.{1}'.format(dso_suffix,
                                               str(self.version.up_to(3)))

            # For lua version 5.1.X, the symlinks should be:
            # liblua5.1.so
            # liblua51.so
            # liblua-5.1.so
            # liblua-51.so
            version_formats = [str(self.version.up_to(2)),
                               Version(str(self.version.up_to(2))).joined]
            for version_str in version_formats:
                for joiner in ['', '-']:
                    dest_path = 'liblua{0}{1}.{2}'.format(joiner,
                                                          version_str,
                                                          dso_suffix)
                    os.symlink(src_path, dest_path)

        with working_dir(os.path.join('luarocks', 'luarocks')):
            configure('--prefix=' + prefix, '--with-lua=' + prefix)
            make('build')
            make('install')

    def append_paths(self, paths, cpaths, path):
        paths.append(os.path.join(path, '?.lua'))
        paths.append(os.path.join(path, '?', 'init.lua'))
        cpaths.append(os.path.join(path, '?.so'))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        lua_paths = []
        for d in dependent_spec.traverse(
                deptypes=('build', 'run'), deptype_query='run'):
            if d.package.extends(self.spec):
                lua_paths.append(os.path.join(d.prefix, self.lua_lib_dir))
                lua_paths.append(os.path.join(d.prefix, self.lua_lib64_dir))
                lua_paths.append(os.path.join(d.prefix, self.lua_share_dir))

        lua_patterns = []
        lua_cpatterns = []
        for p in lua_paths:
            if os.path.isdir(p):
                self.append_paths(lua_patterns, lua_cpatterns, p)

        # Always add this package's paths
        for p in (os.path.join(self.spec.prefix, self.lua_lib_dir),
                  os.path.join(self.spec.prefix, self.lua_lib64_dir),
                  os.path.join(self.spec.prefix, self.lua_share_dir)):
            self.append_paths(lua_patterns, lua_cpatterns, p)

        spack_env.set('LUA_PATH', ';'.join(lua_patterns), separator=';')
        spack_env.set('LUA_CPATH', ';'.join(lua_cpatterns), separator=';')

        # Add LUA to PATH for dependent packages
        spack_env.prepend_path('PATH', self.prefix.bin)

        # For run time environment set only the path for dependent_spec and
        # prepend it to LUAPATH
        if dependent_spec.package.extends(self.spec):
            run_env.prepend_path('LUA_PATH', ';'.join(lua_patterns),
                                 separator=';')
            run_env.prepend_path('LUA_CPATH', ';'.join(lua_cpatterns),
                                 separator=';')

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path(
            'LUA_PATH',
            os.path.join(self.spec.prefix, self.lua_share_dir, '?.lua'),
            separator=';')
        run_env.prepend_path(
            'LUA_PATH', os.path.join(self.spec.prefix, self.lua_share_dir, '?',
                                     'init.lua'),
            separator=';')
        run_env.prepend_path(
            'LUA_PATH',
            os.path.join(self.spec.prefix, self.lua_lib_dir, '?.lua'),
            separator=';')
        run_env.prepend_path(
            'LUA_PATH',
            os.path.join(self.spec.prefix, self.lua_lib_dir, '?', 'init.lua'),
            separator=';')
        run_env.prepend_path(
            'LUA_CPATH',
            os.path.join(self.spec.prefix, self.lua_lib_dir, '?.so'),
            separator=';')

    @property
    def lua_lib_dir(self):
        return os.path.join('lib', 'lua', str(self.version.up_to(2)))

    @property
    def lua_lib64_dir(self):
        return os.path.join('lib64', 'lua', str(self.version.up_to(2)))

    @property
    def lua_share_dir(self):
        return os.path.join('share', 'lua', str(self.version.up_to(2)))

    def setup_dependent_package(self, module, dependent_spec):
        """
        Called before lua modules's install() methods.

        In most cases, extensions will only need to have two lines::

        luarocks('--tree=' + prefix, 'install', rock_spec_path)
        """
        # Lua extension builds can have lua and luarocks executable functions
        module.lua = Executable(join_path(self.spec.prefix.bin, 'lua'))
        module.luarocks = Executable(
            join_path(self.spec.prefix.bin, 'luarocks'))
