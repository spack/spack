##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import llnl.util.tty as tty
from spack.compiler import *
from spack.version import ver

class Gcc(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['gcc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['g++']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['gfortran']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['gfortran']

    # MacPorts builds gcc versions with prefixes and -mp-X.Y suffixes.
    suffixes = [r'-mp-\d\.\d']

    # Named wrapper links within spack.build_env_path
    link_paths = {'cc'  : 'gcc/gcc',
                  'cxx' : 'gcc/g++',
                  'f77' : 'gcc/gfortran',
                  'fc'  : 'gcc/gfortran' }

    @property
    def cxx11_flag(self):
        if self.version < ver('4.3'):
            tty.die("Only gcc 4.3 and above support c++11.")
        elif self.version < ver('4.7'):
            return "-std=gnu++0x"
        else:
            return "-std=gnu++11"

    @classmethod
    def fc_version(cls, fc):
        return get_compiler_version(
            fc, '-dumpversion',
            # older gfortran versions don't have simple dumpversion output.
            r'(?:GNU Fortran \(GCC\))?(\d+\.\d+(?:\.\d+)?)')


    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)
