# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

import llnl.util.lang

from spack.compiler import Compiler


class Rocmcc(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['amdclang']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['amdclang++']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['amdflang']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['amdflang']

    PrgEnv = 'PrgEnv-rocmcc'
    PrgEnv_compiler = 'rocmcc'

    version_argument = '--version'

    @property
    def debug_flags(self):
        return ['-gcodeview', '-gdwarf-2', '-gdwarf-3', '-gdwarf-4',
                '-gdwarf-5', '-gline-tables-only', '-gmodules', '-gz', '-g']

    @property
    def opt_flags(self):
        return ['-O0', '-O1', '-O2', '-O3', '-Ofast', '-Os', '-Oz', '-Og',
                '-O', '-O4']

    @property
    def link_paths(self):
        link_paths = {'cc': 'rocmcc/amdclang',
                      'cxx': 'rocmcc/amdclang++',
                      'f77': 'rocmcc/amdflang',
                      'fc': 'rocmcc/amdflang'}

        return link_paths

    @property
    def verbose_flag(self):
        return "-v"

    @property
    def openmp_flag(self):
        return "-fopenmp"

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
        return '-std=c99'

    @property
    def c11_flag(self):
        return "-std=c11"

    @property
    def cc_pic_flag(self):
        return "-fPIC"

    @property
    def cxx_pic_flag(self):
        return "-fPIC"

    @property
    def f77_pic_flag(self):
        return "-fPIC"

    @property
    def fc_pic_flag(self):
        return "-fPIC"

    required_libs = ['libclang']

    @classmethod
    @llnl.util.lang.memoized
    def extract_version_from_output(cls, output):
        ver = 'unknown'
        match = re.search(
            # clang compiler versions are displayed as clang version 13.0.0
            r'clang version ([^ )\n]+?)-[~.\w\d-]*|'
            r'clang version ([^ )\n]+)',
            output
        )
        if match:
            ver = match.group(match.lastindex)
        return ver

    @classmethod
    def fc_version(cls, fortran_compiler):
        if sys.platform == 'darwin':
            return cls.default_version('clang')

        return cls.default_version(fortran_compiler)

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)

    @property
    def stdcxx_libs(self):
        return ('-lstdc++', )
