# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import List  # novm
from spack.compiler import Compiler


class Msvc(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['cl.exe']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['cl.exe']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = []  # type: List[str]

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = []  # type: List[str]

    # Named wrapper links within build_env_path
    link_paths = {'cc': 'msvc/cl.exe',
                  'cxx': 'msvc/cl.exe',
                  'f77': '',
                  'fc': ''}

    @property
    def verbose_flag(self):
        return ""

    @property
    def pic_flag(self):
        return ""
