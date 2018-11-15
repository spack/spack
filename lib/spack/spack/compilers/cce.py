# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.compiler import Compiler, get_compiler_version


class Cce(Compiler):
    """Cray compiler environment compiler."""
    # Subclasses use possible names of C compiler
    cc_names = ['cc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['CC']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['ftn']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['ftn']

    # MacPorts builds gcc versions with prefixes and -mp-X.Y suffixes.
    suffixes = [r'-mp-\d\.\d']

    PrgEnv = 'PrgEnv-cray'
    PrgEnv_compiler = 'cce'

    link_paths = {'cc': 'cc',
                  'cxx': 'c++',
                  'f77': 'f77',
                  'fc': 'fc'}

    @classmethod
    def default_version(cls, comp):
        return get_compiler_version(comp, '-V', r'[Vv]ersion.*?(\d+(\.\d+)+)')

    @property
    def openmp_flag(self):
        return "-h omp"

    @property
    def cxx11_flag(self):
        return "-h std=c++11"

    @property
    def pic_flag(self):
        return "-h PIC"
