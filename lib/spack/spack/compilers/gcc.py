##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
    # Homebrew and Linuxbrew may build gcc with -X, -X.Y suffixes.
    # Old compatibility versions may contain XY suffixes.
    suffixes = [r'-mp-\d\.\d', r'-\d\.\d', r'-\d', r'\d\d']

    # Named wrapper links within spack.build_env_path
    link_paths = {'cc': 'gcc/gcc',
                  'cxx': 'gcc/g++',
                  'f77': 'gcc/gfortran',
                  'fc': 'gcc/gfortran'}

    PrgEnv = 'PrgEnv-gnu'
    PrgEnv_compiler = 'gcc'

    @property
    def openmp_flag(self):
        return "-fopenmp"

    @property
    def cxx11_flag(self):
        if self.version < ver('4.3'):
            tty.die("Only gcc 4.3 and above support c++11.")
        elif self.version < ver('4.7'):
            return "-std=c++0x"
        else:
            return "-std=c++11"

    @property
    def cxx14_flag(self):
        if self.version < ver('4.8'):
            tty.die("Only gcc 4.8 and above support c++14.")
        elif self.version < ver('4.9'):
            return "-std=c++1y"
        else:
            return "-std=c++14"

    @property
    def cxx17_flag(self):
        if self.version < ver('5.0'):
            tty.die("Only gcc 5.0 and above support c++17.")
        else:
            return "-std=c++1z"

    @property
    def pic_flag(self):
        return "-fPIC"

    @classmethod
    def fc_version(cls, fc):
        return get_compiler_version(
            fc, '-dumpversion',
            # older gfortran versions don't have simple dumpversion output.
            r'(?:GNU Fortran \(GCC\))?(\d+\.\d+(?:\.\d+)?)')

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)

    @property
    def stdcxx_libs(self):
        return ('-lstdc++', )
