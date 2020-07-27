# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.compiler
from spack.version import ver


class Gcc(spack.compiler.Compiler):
    # Named wrapper links within build_env_path
    link_paths = {'cc': 'gcc/gcc',
                  'cxx': 'gcc/g++',
                  'f77': 'gcc/gfortran',
                  'fc': 'gcc/gfortran'}

    PrgEnv = 'PrgEnv-gnu'
    PrgEnv_compiler = 'gcc'

    @property
    def verbose_flag(self):
        return "-v"

    @property
    def debug_flags(self):
        return ['-g', '-gstabs+', '-gstabs', '-gxcoff+', '-gxcoff', '-gvms']

    @property
    def opt_flags(self):
        return ['-O', '-O0', '-O1', '-O2', '-O3', '-Os', '-Ofast', '-Og']

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
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++11 standard", "cxx11_flag", " < 4.3")
        elif self.version < ver('4.7'):
            return "-std=c++0x"
        else:
            return "-std=c++11"

    @property
    def cxx14_flag(self):
        if self.version < ver('4.8'):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++14 standard", "cxx14_flag", "< 4.8")
        elif self.version < ver('4.9'):
            return "-std=c++1y"
        elif self.version < ver('6.0'):
            return "-std=c++14"
        else:
            return ""

    @property
    def cxx17_flag(self):
        if self.version < ver('5.0'):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++17 standard", "cxx17_flag", "< 5.0")
        elif self.version < ver('6.0'):
            return "-std=c++1z"
        else:
            return "-std=c++17"

    @property
    def c99_flag(self):
        if self.version < ver('4.5'):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C99 standard", "c99_flag", "< 4.5")
        return "-std=c99"

    @property
    def c11_flag(self):
        if self.version < ver('4.7'):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C11 standard", "c11_flag", "< 4.7")
        return "-std=c11"

    @property
    def cc_pic_flag(self):
        return "-fPIC"

    @property
    def cxx_pic_flag(self):
        return "-fPIC"

    @property
    def f77_pic_flag(self):
        return "-fPIC"

    @property
    def fc_pic_flag(self):
        return "-fPIC"

    required_libs = ['libgcc', 'libgfortran']

    @property
    def stdcxx_libs(self):
        return ('-lstdc++', )
