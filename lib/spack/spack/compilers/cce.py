# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.compiler


class Cce(spack.compiler.Compiler):
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

    link_paths = {'cc': 'cce/cc',
                  'cxx': 'cce/case-insensitive/CC',
                  'f77': 'cce/ftn',
                  'fc': 'cce/ftn'}

    version_argument = '-V'
    version_regex = r'[Vv]ersion.*?(\d+(\.\d+)+)'

    @property
    def openmp_flag(self):
        return "-h omp"

    @property
    def cxx11_flag(self):
        return "-h std=c++11"

    @property
    def pic_flag(self):
        return "-h PIC"
