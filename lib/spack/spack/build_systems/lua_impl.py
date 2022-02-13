# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import glob
import inspect
import os
import platform
import re
from typing import List  # novm

from llnl.util.filesystem import find, find_libraries, join_path, working_dir

import spack.build_environment
from spack.build_systems.makefile import MakefilePackage
from spack.directives import *
from spack.package import InstallError, PackageBase, run_after
from spack.util.executable import Executable

__SUPPORTED_IMPLS = ("Lua", "LuaLuajit", "LuaLuajitOpenresty")


class LuaImplPackage(MakefilePackage):
    """Specialized class for lua *implementations*

    This exists to ensure that lua, luajit and luajit-openresty all initialize extension
    packages the same way and provide luarocks the same way."""

    extendable = True

    variant(
        "fetcher",
        default="curl",
        values=("curl", "wget"),
        description="Fetcher to use in the LuaRocks package manager",
    )

    phases = MakefilePackage.phases + ["add_luarocks"]
    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "LuaImplPackage"

    lua_version_override = None

    def __init__(self, *args, **kwargs):
        super(LuaImplPackage, self).__init__(*args, **kwargs)
        self.lua_dir_name = "lua"
        pass

    def __verdir(self):
        return (
            str(self.version.up_to(2))
            if self.lua_version_override is None
            else self.lua_version_override
        )

    @property
    def lua_lib_dir(self):
        return os.path.join("lib", self.lua_dir_name, self.__verdir())

    @property
    def lua_lib64_dir(self):
        return os.path.join("lib64", self.lua_dir_name, self.__verdir())

    @property
    def lua_share_dir(self):
        return os.path.join("share", self.lua_dir_name, self.__verdir())

    # luarocks needs unzip for some packages (e.g. lua-luaposix)
    depends_on("unzip", type="run")

    # luarocks needs a fetcher (curl/wget), unfortunately I have not found
    # how to force a choice for curl or wget, but curl seems the default.
    depends_on("curl", when="fetcher=curl", type="run")
    depends_on("wget", when="fetcher=wget", type="run")

    resource(
        name="luarocks",
        url="https://luarocks.github.io/luarocks/releases/" "luarocks-3.8.0.tar.gz",
        sha256="56ab9b90f5acbc42eb7a94cf482e6c058a63e8a1effdf572b8b2a6323a06d923",
        destination="luarocks",
        placement="luarocks",
    )

    def symlink_luajit(self):
        """helper for luajit-like packages that need symlinks"""
        if not self.spec.satisfies("+lualinks"):
            return

        with working_dir(self.prefix.bin):
            if not os.path.exists(self.prefix.bin.lua):
                luajits = find(self.prefix.bin, "luajit*")
                assert len(luajits) == 1
                luajit = luajits[0]
                if os.path.islink(luajit):
                    luajit = os.readlink(luajit)
                symlink(luajit, "lua")

        with working_dir(self.prefix.include):
            if not os.path.exists(self.prefix.include.lua):
                luajit_include_subdirs = glob.glob(
                    os.path.join(self.prefix.include, "luajit*")
                )
                assert len(luajit_include_subdirs) == 1
                symlink(luajit_include_subdirs[0], "lua")

        with working_dir(self.prefix.lib):
            for ext in ("." + spack.build_environment.dso_suffix, ".a"):
                luajit_libnames = glob.glob(
                    os.path.join(self.prefix.lib, "libluajit") + "*" + ext + "*"
                )
                real_lib = next(
                    lib
                    for lib in luajit_libnames
                    if os.path.isfile(lib) and not os.path.islink(lib)
                )
                symlink(real_lib, "liblua" + ext)

    def add_luarocks(self, spec, prefix):
        with working_dir(os.path.join("luarocks", "luarocks")):
            configure("--prefix=" + prefix, "--with-lua=" + prefix)
            make("build")
            make("install")

    def append_paths(self, paths, cpaths, path):
        paths.append(os.path.join(path, "?.lua"))
        paths.append(os.path.join(path, "?", "init.lua"))
        cpaths.append(os.path.join(path, "?.so"))

    def _setup_dependent_env_helper(self, env, dependent_spec):
        lua_paths = []
        for d in dependent_spec.traverse(
            deptypes=("build", "run"), deptype_query="run"
        ):
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
        for p in (
            os.path.join(self.spec.prefix, self.lua_lib_dir),
            os.path.join(self.spec.prefix, self.lua_lib64_dir),
            os.path.join(self.spec.prefix, self.lua_share_dir),
        ):
            self.append_paths(lua_patterns, lua_cpatterns, p)

        return lua_patterns, lua_cpatterns

    def setup_dependent_build_environment(self, env, dependent_spec):
        lua_patterns, lua_cpatterns = self._setup_dependent_env_helper(
            env, dependent_spec
        )

        env.prepend_path("LUA_PATH", ";".join(lua_patterns), separator=";")
        env.prepend_path("LUA_CPATH", ";".join(lua_cpatterns), separator=";")

    def setup_dependent_run_environment(self, env, dependent_spec):
        # For run time environment set only the path for dependent_spec and
        # prepend it to LUAPATH
        lua_patterns, lua_cpatterns = self._setup_dependent_env_helper(
            env, dependent_spec
        )

        if dependent_spec.package.extends(self.spec):
            env.prepend_path("LUA_PATH", ";".join(lua_patterns), separator=";")
            env.prepend_path("LUA_CPATH", ";".join(lua_cpatterns), separator=";")

    def setup_run_environment(self, env):
        env.prepend_path(
            "LUA_PATH",
            os.path.join(self.spec.prefix, self.lua_share_dir, "?.lua"),
            separator=";",
        )
        env.prepend_path(
            "LUA_PATH",
            os.path.join(self.spec.prefix, self.lua_share_dir, "?", "init.lua"),
            separator=";",
        )
        env.prepend_path(
            "LUA_PATH",
            os.path.join(self.spec.prefix, self.lua_lib_dir, "?.lua"),
            separator=";",
        )
        env.prepend_path(
            "LUA_PATH",
            os.path.join(self.spec.prefix, self.lua_lib_dir, "?", "init.lua"),
            separator=";",
        )
        env.prepend_path(
            "LUA_CPATH",
            os.path.join(self.spec.prefix, self.lua_lib_dir, "?.so"),
            separator=";",
        )

    def setup_dependent_package(self, module, dependent_spec):
        """
        Called before lua modules's install() methods.

        In most cases, extensions will only need to have two lines::

        luarocks('--tree=' + prefix, 'install', rock_spec_path)
        """
        # Lua extension builds can have lua and luarocks executable functions
        module.lua = Executable(join_path(self.spec.prefix.bin, "lua"))
        module.luarocks = Executable(join_path(self.spec.prefix.bin, "luarocks"))
