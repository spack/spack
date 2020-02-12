# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.compiler


class Nag(spack.compiler.Compiler):
    # Subclasses use possible names of C compiler
    cc_names = []

    # Subclasses use possible names of C++ compiler
    cxx_names = []

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['nagfor']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['nagfor']

    # Named wrapper links within build_env_path
    # Use default wrappers for C and C++, in case provided in compilers.yaml
    link_paths = {
        'cc': 'cc',
        'cxx': 'c++',
        'f77': 'nag/nagfor',
        'fc': 'nag/nagfor'}

    version_argument = '-V'
    version_regex = r'NAG Fortran Compiler Release ([0-9.]+)'

    @property
    def openmp_flag(self):
        return "-openmp"

    @property
    def cxx11_flag(self):
        # NAG does not have a C++ compiler
        # However, it can be mixed with a compiler that does support it
        return "-std=c++11"

    @property
    def pic_flag(self):
        return "-PIC"

    # Unlike other compilers, the NAG compiler passes options to GCC, which
    # then passes them to the linker. Therefore, we need to doubly wrap the
    # options with '-Wl,-Wl,,'
    @property
    def f77_rpath_arg(self):
        return '-Wl,-Wl,,-rpath,,'

    @property
    def fc_rpath_arg(self):
        return '-Wl,-Wl,,-rpath,,'

    @property
    def linker_arg(self):
        return '-Wl,-Wl,,'
