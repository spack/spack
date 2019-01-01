# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.compiler import Compiler, _version_cache
from spack.util.executable import Executable


class Arm(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['armclang']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['armclang++']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['armflang']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['armflang']

    # Named wrapper links within lib/spack/env
    link_paths = {'cc': 'clang/clang',
                  'cxx': 'clang/clang++',
                  'f77': 'clang/flang',
                  'fc': 'clang/flang'}

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
        return "-std=c++1z"

    @property
    def pic_flag(self):
        return "-fPIC"

    @classmethod
    def default_version(cls, comp):
        if comp not in _version_cache:
            compiler = Executable(comp)
            output = compiler('--version', output=str, error=str)

            ver = 'unknown'
            match = re.search(r'Arm C/C++/Fortran Compiler version ([^ )]+)',
                              output)
            if match:
                ver = match.group(1)

            _version_cache[comp] = ver

        return _version_cache[comp]

    @classmethod
    def fc_version(cls, fc):
        return cls.default_version(fc)

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)
