# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.compiler


class Arm(spack.compiler.Compiler):
    # Named wrapper links within lib/spack/env
    link_paths = {'cc': 'arm/armclang',
                  'cxx': 'arm/armclang++',
                  'f77': 'arm/armflang',
                  'fc': 'arm/armflang'}

    @property
    def verbose_flag(self):
        return "-v"

    @property
    def opt_flags(self):
        return ['-O', '-O0', '-O1', '-O2', '-O3', '-Ofast']

    @property
    def openmp_flag(self):
        return "-fopenmp"

    @property
    def cxx11_flag(self):
        return "-std=c++11"

    @property
    def cxx14_flag(self):
        return "-std=c++14"

    @property
    def cxx17_flag(self):
        return "-std=c++1z"

    @property
    def c99_flag(self):
        return "-std=c99"

    @property
    def c11_flag(self):
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

    required_libs = ['libclang', 'libflang']
