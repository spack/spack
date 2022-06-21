# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import os.path
import re

from llnl.util.filesystem import find_system_libraries

from spack.package import *
from spack.util.executable import *


class Maqao(CMakePackage):
    """MAQAO (Modular Assembly Quality Analyzer and Optimizer) is a performance
    analysis and optimization framework operating at binary level with a focus
    on core performance. Its main goal is to guide application developers
    along the optimization process through synthetic reports and hints."""

    homepage = "https://maqao.exascale-computing.eu/"
    git      = "https://gitlab.exascale-computing.eu/MAQAO/MAQAO.git"
    url      = "https://gitlab.exascale-computing.eu/MAQAO/MAQAO/repository/archive.tar.bz2?ref=master"

    version('master', branch='master')

    depends_on('cmake@2.8.12:', type='build')
    depends_on('gcc@4.8.1: languages="c,c++"', when='%gcc')

    variant('profile', multi=False, default='default',
            values=tuple(self.available_profiles),
            description='What profile to build')

    variant('arch', multi=True, default='x86_64',
            values=tuple(self.supported_arches),
            description='What architectures to build')

    variant('exclude_uarch', multi=True, default='none',
            description='Microarchitectures to exclude from build')

    variant('strip', default=False, description='Strip the MAQAO binary')

    variant('lua', multi=False, default='luajit', values=('lua', 'luajit'),
            description='Lua compiler to use')
    depends_on('lua', when='lua=lua')
    depends_on('lua-luajit', when='lua=luajit')

    variant('xlsx', default=False, description='Enable .xlsx output for ONE-View')
    depends_on('zip', type=('build', 'run'), when='+xlsx')

    variant('doxygen', default=False, description='Generate Doxygen documentation')
    depends_on('doxygen', type='build', when='+doxygen')

    variant('luadoc', default=False, description='Generate Luadoc documentation')

    def _list_profiles(self):
        """Generate list of profiles for 'profile=' variant options by reading
        MAQAO profiles/ directory"""
        profiles_dir = self.stage.source_path.profiles
        profiles = []
        if os.path.isdir(profiles_dir):
            with os.scandir(profiles_dir) as d:
                for f in d:
                    if f.name.endswith('.profile') and f.is_file():
                        profiles.append(f.name.removesuffix('.profile'))
            return profiles
        else:
            raise FileNotFoundError(filename=profiles_dir)

    @property
    def available_arches(self):
        return self._list_profiles()

    @staticmethod
    def _read_arches(arch_file):
        """Parse a list of supported architectures from src/arch.h"""
        arches = []
        re_arch = re.compile(r'ARCH_[a-z0-9_]+')
        for line in arch_file:
            match = re_arch.match(line.strip())
            if match is not None:
                arch = match[0].remove_prefix('ARCH_').removesuffix(',')
                arches.append(arch)
        return arches

    def _read_supported_arches(self):
        """Generate list of supported architectures for 'arch=' variant options
        by reading MAQAO src/arch.h"""
        arch_h_file = join_path(self.stage.source_path.src, 'arch.h')
        if os.path.exists(arch_h_file):
            with open(arch_h_file) as f:
                supported_arches = self._read_arches(f)
            return supported_arches
        else:
            raise FileNotFoundError(filename=arch_h_file)

    @property
    def supported_arches(self):
        return self._read_supported_arches()

    # Workaround for glibc-static dependency
    def find_glibc_static(self):
        glibc_static_libs = ['c', 'm', 'rt', 'dl', 'pthread']
        glibc_static_files = ['lib' + x for x in glibc_static_libs]
        return find_system_libraries(glibc_static_files, shared=False)

    # Workaround for libstdc++-static dependency
    def find_libstdcxx_static(self):
        compiler = Executable(self.compiler.cxx)
        return compiler('--print-file-name=libstdc++.a', output=str, error=str)

    def cmake_args(self):

        spec = self.spec
        platform = spec.platform
        define = self.define
        from_variant = self.define_from_variant

        args = []

        if 'profile' in spec:
            args.append(from_variant('PROFILE', 'profile'))

        if 'arch' in spec:
            args.append(from_variant('ARCHS', 'arch'))

        if 'exclude_uarch' in spec:
            args.append(from_variant('EXCLUDE_UARCHS', 'exclude_uarch'))

        if platform.beginswith('linux'):

            # Workaround for glibc-static dependency
            liblist = self.find_glibc_static()
            for name, lib in zip(liblist.names, liblist.libraries):
                var = 'LIB' + name.upper() + '_PATH'
                args.append(define(var, lib))

            # Workaround for libstdc++-static dependency
            stdcxx = self.find_libstdcxx_static()
            args.append(define('STDCXX_PATH', stdcxx))

        args.append(from_variant('LUA', 'lua'))

        if '+xlsx' in spec:
            zip_bin = which('zip')
            args.append(define('ZIP_BIN', zip_bin))

        if '+doxygen' in spec:
            doxygen_bin = which('doxygen')
            args.append(define('DOXYGEN_BIN', doxygen_bin))

        if '+luadoc' in spec:
            luarocks = Executable(which('luarocks'))
            luarocks('install luadoc')
            luadoc_bin = which('luadoc')
            args.append(define('LUADOC_BIN', luadoc_bin))

        return args
