# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.compiler import Compiler, get_compiler_version


class Nag(Compiler):
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

    @classmethod
    def default_version(cls, comp):
        """The ``-V`` option works for nag compilers.
        Output looks like this::

            NAG Fortran Compiler Release 6.0(Hibiya) Build 1037
            Product NPL6A60NA for x86-64 Linux
        """
        return get_compiler_version(
            comp, '-V', r'NAG Fortran Compiler Release ([0-9.]+)')
