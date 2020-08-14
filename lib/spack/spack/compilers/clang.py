# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.compiler import Compiler, UnsupportedCompilerFlag
from spack.version import ver


#: compiler symlink mappings for mixed f77 compilers
f77_mapping = [
    ('gfortran', 'clang/gfortran'),
    ('xlf_r', 'xl_r/xlf_r'),
    ('xlf', 'xl/xlf'),
    ('pgfortran', 'pgi/pgfortran'),
    ('ifort', 'intel/ifort')
]

#: compiler symlink mappings for mixed f90/fc compilers
fc_mapping = [
    ('gfortran', 'clang/gfortran'),
    ('xlf90_r', 'xl_r/xlf90_r'),
    ('xlf90', 'xl/xlf90'),
    ('pgfortran', 'pgi/pgfortran'),
    ('ifort', 'intel/ifort')
]


class Clang(Compiler):
    version_argument = '--version'

    @property
    def debug_flags(self):
        return ['-gcodeview', '-gdwarf-2', '-gdwarf-3', '-gdwarf-4',
                '-gdwarf-5', '-gline-tables-only', '-gmodules', '-gz', '-g']

    @property
    def opt_flags(self):
        return ['-O0', '-O1', '-O2', '-O3', '-Ofast', '-Os', '-Oz', '-Og',
                '-O', '-O4']

    # Clang has support for using different fortran compilers with the
    # clang executable.
    @property
    def link_paths(self):
        # clang links are always the same
        link_paths = {'cc': 'clang/clang',
                      'cxx': 'clang/clang++'}

        # fortran links need to look at the actual compiler names from
        # compilers.yaml to figure out which named symlink to use
        for compiler_name, link_path in f77_mapping:
            if self.f77 and compiler_name in self.f77:
                link_paths['f77'] = link_path
                break
        else:
            link_paths['f77'] = 'clang/flang'

        for compiler_name, link_path in fc_mapping:
            if self.fc and compiler_name in self.fc:
                link_paths['fc'] = link_path
                break
        else:
            link_paths['fc'] = 'clang/flang'

        return link_paths

    @property
    def verbose_flag(self):
        return "-v"

    openmp_flag = "-fopenmp"

    @property
    def cxx11_flag(self):
        if self.version < ver('3.3'):
            raise UnsupportedCompilerFlag(
                self, "the C++11 standard", "cxx11_flag", "< 3.3"
            )
        return "-std=c++11"

    @property
    def cxx14_flag(self):
        if self.version < ver('3.4'):
            raise UnsupportedCompilerFlag(
                self, "the C++14 standard", "cxx14_flag", "< 3.5"
            )
        elif self.version < ver('3.5'):
            return "-std=c++1y"

        return "-std=c++14"

    @property
    def cxx17_flag(self):
        if self.version < ver('3.5'):
            raise UnsupportedCompilerFlag(
                self, "the C++17 standard", "cxx17_flag", "< 3.5"
            )
        elif self.version < ver('5.0'):
            return "-std=c++1z"

        return "-std=c++17"

    @property
    def c99_flag(self):
        return '-std=c99'

    @property
    def c11_flag(self):
        if self.version < ver('6.1.0'):
            raise UnsupportedCompilerFlag(self,
                                          "the C11 standard",
                                          "c11_flag",
                                          "< 6.1.0")
        else:
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

    required_libs = ['libclang']
