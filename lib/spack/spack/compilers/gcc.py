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
import spack.compilers.clang
from spack.compiler import \
    Compiler, get_compiler_version, UnsupportedCompilerFlag
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

    # Named wrapper links within build_env_path
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
    def cxx98_flag(self):
        if self.version < ver('6.0'):
            return ""
        else:
            return "-std=c++98"

    @property
    def cxx11_flag(self):
        if self.version < ver('4.3'):
            raise UnsupportedCompilerFlag(self,
                                          "the C++11 standard",
                                          "cxx11_flag",
                                          " < 4.3")
        elif self.version < ver('4.7'):
            return "-std=c++0x"
        else:
            return "-std=c++11"

    @property
    def cxx14_flag(self):
        if self.version < ver('4.8'):
            raise UnsupportedCompilerFlag(self,
                                          "the C++14 standard",
                                          "cxx14_flag",
                                          "< 4.8")
        elif self.version < ver('4.9'):
            return "-std=c++1y"
        elif self.version < ver('6.0'):
            return "-std=c++14"
        else:
            return ""

    @property
    def cxx17_flag(self):
        if self.version < ver('5.0'):
            raise UnsupportedCompilerFlag(self,
                                          "the C++17 standard",
                                          "cxx17_flag",
                                          "< 5.0")
        elif self.version < ver('6.0'):
            return "-std=c++1z"
        else:
            return "-std=c++17"

    @property
    def pic_flag(self):
        return "-fPIC"

    @classmethod
    def default_version(cls, cc):
        """Older versions of gcc use the ``-dumpversion`` option.
        Output looks like this::

            4.4.7

        In GCC 7, this option was changed to only return the major
        version of the compiler::

            7

        A new ``-dumpfullversion`` option was added that gives us
        what we want::

            7.2.0
        """
        # Skip any gcc versions that are actually clang, like Apple's gcc.
        # Returning "unknown" makes them not detected by default.
        # Users can add these manually to compilers.yaml at their own risk.
        if spack.compilers.clang.Clang.default_version(cc) != 'unknown':
            return 'unknown'

        version = super(Gcc, cls).default_version(cc)
        if ver(version) >= ver('7'):
            version = get_compiler_version(cc, '-dumpfullversion')
        return version

    @classmethod
    def fc_version(cls, fc):
        """Older versions of gfortran use the ``-dumpversion`` option.
        Output looks like this::

            GNU Fortran (GCC) 4.4.7 20120313 (Red Hat 4.4.7-18)
            Copyright (C) 2010 Free Software Foundation, Inc.

        or::

            4.8.5

        In GCC 7, this option was changed to only return the major
        version of the compiler::

            7

        A new ``-dumpfullversion`` option was added that gives us
        what we want::

            7.2.0
        """
        version = get_compiler_version(
            fc, '-dumpversion',
            r'(?:GNU Fortran \(GCC\) )?([\d.]+)')
        if ver(version) >= ver('7'):
            version = get_compiler_version(fc, '-dumpfullversion')
        return version

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)

    @property
    def stdcxx_libs(self):
        return ('-lstdc++', )
