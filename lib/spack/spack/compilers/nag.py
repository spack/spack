##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
