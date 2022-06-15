# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from os.path import dirname

from spack.compiler import Compiler


class Oneapi(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['icx']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['icpx']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['ifx']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['ifx']

    # Named wrapper links within build_env_path
    link_paths = {'cc': os.path.join('oneapi', 'icx'),
                  'cxx': os.path.join('oneapi', 'icpx'),
                  'f77': os.path.join('oneapi', 'ifx'),
                  'fc': os.path.join('oneapi', 'ifx')}

    PrgEnv = 'PrgEnv-oneapi'
    PrgEnv_compiler = 'oneapi'

    version_argument = '--version'
    version_regex = r'(?:(?:oneAPI DPC\+\+(?:\/C\+\+)? Compiler)|(?:\(IFORT\))) (\S+)'

    @property
    def verbose_flag(self):
        return "-v"

    required_libs = ['libirc', 'libifcore', 'libifcoremt', 'libirng',
                     'libsvml', 'libintlc', 'libimf', 'libsycl',
                     'libOpenCL']

    @property
    def debug_flags(self):
        return ['-debug', '-g', '-g0', '-g1', '-g2', '-g3']

    @property
    def opt_flags(self):
        return ['-O', '-O0', '-O1', '-O2', '-O3', '-Ofast', '-Os']

    @property
    def openmp_flag(self):
        return "-fiopenmp"
    # There may be some additional options here for offload, e.g. :
    #  -fopenmp-simd           Emit OpenMP code only for SIMD-based constructs.
    #  -fopenmp-targets=<value>
    #  -fopenmp-version=<value>
    #  -fopenmp                Parse OpenMP pragmas and generate parallel code.
    #  -qno-openmp             Disable OpenMP support
    #  -qopenmp-link=<value>   Choose whether to link with the static or
    #                          dynamic OpenMP libraries. Default is dynamic.
    #  -qopenmp-simd           Emit OpenMP code only for SIMD-based constructs.
    #  -qopenmp-stubs          enables the user to compile OpenMP programs in
    #                          sequential mode. The OpenMP directives are
    #                          ignored and a stub OpenMP library is linked.
    #  -qopenmp-threadprivate=<value>
    #  -qopenmp                Parse OpenMP pragmas and generate parallel code.
    #  -static-openmp          Use the static host OpenMP runtime while
    #                          linking.
    #  -Xopenmp-target=<triple> <arg>
    #  -Xopenmp-target <arg>   Pass <arg> to the target offloading toolchain.
    # Source: icx --help output

    @property
    def cxx11_flag(self):
        return "-std=c++11"

    @property
    def cxx14_flag(self):
        return "-std=c++14"

    @property
    def c99_flag(self):
        return "-std=c99"

    @property
    def c11_flag(self):
        return "-std=c1x"

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

    @property
    def stdcxx_libs(self):
        return ('-cxxlib', )

    def setup_custom_environment(self, pkg, env):
        # workaround bug in icpx driver where it requires sycl-post-link is on the PATH
        # It is located in the same directory as the driver. Error message:
        #   clang++: error: unable to execute command:
        #   Executable "sycl-post-link" doesn't exist!
        if self.cxx:
            env.prepend_path('PATH', dirname(self.cxx))
