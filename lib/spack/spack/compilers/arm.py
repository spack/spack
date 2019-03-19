# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.compiler


class Arm(spack.compiler.Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['armclang']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['armclang++']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['armflang']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['armflang']

    # Named wrapper links within lib/spack/env
    link_paths = {'cc': 'arm/armclang',
                  'cxx': 'arm/armclang++',
                  'f77': 'arm/armflang',
                  'fc': 'arm/armflang'}

    version_argument = '--version'
    version_regex = r'Arm C\/C\+\+\/Fortran Compiler version ([^ )]+)'

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
    def fc_version(cls, fc):
        return cls.default_version(fc)

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)
