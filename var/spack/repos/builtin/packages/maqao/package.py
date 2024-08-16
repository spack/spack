# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util.filesystem import find_system_libraries

from spack.package import *
from spack.util.executable import *


class Maqao(CMakePackage):
    """MAQAO (Modular Assembly Quality Analyzer and Optimizer) is a performance
    analysis and optimization framework operating at binary level with a focus
    on core performance. Its main goal is to guide application developers
    along the optimization process through synthetic reports and hints."""

    homepage = "https://maqao.exascale-computing.eu/"
    git = "https://gitlab.exascale-computing.eu/MAQAO/MAQAO.git"
    url = "https://gitlab.exascale-computing.eu/MAQAO/MAQAO/repository/archive.tar.bz2?ref=master"

    maintainers = ["cvalensi", "yaspr"]
    executables = ["maqao"]

    version("master", branch="master")

    # From 'profiles' subdirectory
    supported_profiles = ("default", "release", "release.intel64-xeonphi")

    # Currently supported architectures
    supported_arches = ("x86_64", "k1om")

    # Function to map Spack-detected system architecture to a supported MAQAO arch code
    def detect_arch(self):
        if self.spec.satisfies(target=mic_knl):
            return "k1om"
        elif self.spec.satisfies(target=x86_64):
            return "x86_64"
        else:
            return None

    variant(
        "profile",
        multi=False,
        default="default",
        values=supported_profiles,
        description="What profile to build",
    )

    default_arch = self.detect_arch()
    variant(
        "arch",
        multi=True,
        default=default_arch,
        values=supported_arches,
        description="What architectures to build",
    )

    variant(
        "exclude_uarch",
        multi=True,
        default=None,
        values=supported_arches,
        description="Microarchitectures to exclude from build",
    )

    variant("strip", default=False, description="Strip the MAQAO binary")

    variant(
        "lua",
        multi=False,
        default="luajit",
        values=("lua", "luajit"),
        description="Lua compiler to use",
    )

    variant("xlsx", default=False, description="Enable .xlsx output for ONE-View")

    variant("docs", default=False, description="Generate documentation")

    depends_on("cmake@2.8.12:", type="build")
    depends_on('gcc@4.8.1: languages="c,c++"', when="%gcc")
    depends_on("lua", type=("build", "run"), when="lua=lua")
    depends_on("lua-luajit", type=("build", "run"), when="lua=luajit")
    depends_on("zip", type=("build", "run"), when="+xlsx")
    depends_on("doxygen", type="build", when="+docs")

    # Workaround for glibc-static dependency
    def find_glibc_static(self):
        glibc_static_libs = ["c", "m", "rt", "dl", "pthread"]
        glibc_static_files = ["lib" + x for x in glibc_static_libs]
        return find_system_libraries(glibc_static_files, shared=False)

    # Workaround for libstdc++-static dependency
    def find_libstdcxx_static(self):
        compiler = Executable(self.compiler.cxx)
        return compiler("--print-file-name=libstdc++.a", output=str, error=str)

    # Find luadoc and install it using luarocks when not found
    def find_luadoc(self):
        luadoc = which("luadoc")
        if luadoc is None:
            luarocks = self.spec["lua"].luarocks
            if luarocks is None:
                raise RuntimeError(
                    "Spack cannot find both luarocks and luadoc"
                    " on your system. Please install luarocks first,"
                    " then install luadoc with `luarocks install luadoc`"
                )
            luarocks("install", "luadoc")
            luadoc = which("luadoc")
        return luadoc.command.path

    def cmake_args(self):

        spec = self.spec
        define = self.define
        from_variant = self.define_from_variant

        args = []

        args.append(from_variant("PROFILE", "profile"))
        args.append(from_variant("ARCHS", "arch"))
        args.append(from_variant("EXCLUDE_UARCHS", "exclude_uarch"))

        if spec.platform.beginswith("linux"):

            # Workaround for glibc-static dependency
            liblist = self.find_glibc_static()
            for name, lib in zip(liblist.names, liblist.libraries):
                var = "LIB" + name.upper() + "_PATH"
                args.append(define(var, lib))

            # Workaround for libstdc++-static dependency
            stdcxx = self.find_libstdcxx_static()
            args.append(define("STDCXX_PATH", stdcxx))

        args.append(from_variant("LUA", "lua"))

        if "+xlsx" in spec:
            zip_bin = which("zip")
            args.append(define("ZIP_BIN", zip_bin))

        if "+docs" in spec:
            doxygen = spec["doxygen"].command.path
            luadoc = self.find_luadoc()
            args.append(define("DOXYGEN_BIN", doxygen))
            args.append(define("LUADOC_BIN", luadoc))

        return args
