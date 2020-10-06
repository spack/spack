# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.compiler
from spack.compiler import Compiler, UnsupportedCompilerFlag
from spack.version import ver

import re


class Nvidia(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['nvc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['nvc++', 'nvCC']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['nvfortran']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['nvfortran']

    # Named wrapper links within build_env_path
    link_paths = {'cc': 'nvidia/nvc',
                  'cxx': 'nvidia/nvc++',
                  'f77': 'nvidia/nvfortran',
                  'fc': 'nvidia/nvfortran'}

    PrgEnv = 'PrgEnv-nvidia'
    PrgEnv_compiler = 'nvidia'

    version_argument = '--version'
    version_regex = r'nv[^ ]* ([0-9.]+)-[0-9]+ (LLVM )?[^ ]+ target on '

    @property
    def verbose_flag(self):
        return "-v"

    @property
    def debug_flags(self):
        return ['-g', '-gopt']

    @property
    def opt_flags(self):
        return ['-O', '-O0', '-O1', '-O2', '-O3', '-O4']

    @property
    def openmp_flag(self):
        return "-mp"

    @property
    def cxx11_flag(self):
        return "-std=c++11"

    @property
    def cxx14_flag(self):
        return "-std=c++14"

    @property
    def cxx17_flag(self):
        return "-std=c++17"

    @property
    def c99_flag(self):
        return "-std=c99"

    @property
    def c11_flag(self):
        return "-std=c11"

    @property
    def cc_pic_flag(self):
        return "-fpic"

    @property
    def cxx_pic_flag(self):
        return "-fpic"

    @property
    def f77_pic_flag(self):
        return "-fpic"

    @property
    def fc_pic_flag(self):
        return "-fpic"

    required_libs = ['libnvc', 'libnvf']
