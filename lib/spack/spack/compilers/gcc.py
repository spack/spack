# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import os
import spack.compilers.clang

from spack.compiler import Compiler, UnsupportedCompilerFlag
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

    @classmethod
    def verbose_flag(cls):
        return "-v"

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
    def c99_flag(self):
        if self.version < ver('4.5'):
            raise UnsupportedCompilerFlag(self,
                                          "the C99 standard",
                                          "c99_flag",
                                          "< 4.5")
        return "-std=c99"

    @property
    def c11_flag(self):
        if self.version < ver('4.7'):
            raise UnsupportedCompilerFlag(self,
                                          "the C11 standard",
                                          "c11_flag",
                                          "< 4.7")
        return "-std=c11"

    @property
    def pic_flag(self):
        return "-fPIC"

    required_libs = ['libgcc', 'libgfortran']

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
            output = spack.compiler.get_compiler_version_output(
                cc, '-dumpfullversion'
            )
            version = cls.extract_version_from_output(output)
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
        output = spack.compiler.get_compiler_version_output(fc, '-dumpversion')
        match = re.search(r'(?:GNU Fortran \(GCC\) )?([\d.]+)', output)
        version = match.group(match.lastindex) if match else 'unknown'
        if ver(version) >= ver('7'):
            output = spack.compiler.get_compiler_version_output(
                fc, '-dumpfullversion'
            )
            version = cls.extract_version_from_output(output)
        return version

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)

    @property
    def stdcxx_libs(self):
        return ('-lstdc++', )

    def remap_debugsrc(self, from_dir, to_dir):
        option = "-ffile-prefix-map" if self.spec.satisfies('gcc@8:') \
                 else "-fdebug-prefix-map"
        real_from_dir = os.path.realpath(from_dir)
        return "%s=%s=%s" % (option, real_from_dir, to_dir)
