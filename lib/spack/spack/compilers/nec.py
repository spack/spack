# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.compiler


class Nec(spack.compiler.Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ["ncc"]

    # Subclasses use possible names of C++ compiler
    cxx_names = ["nc++"]

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ["nfort"]

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ["nfort"]

    # Named wrapper links within build_env_path
    link_paths = {
        "cc": os.path.join("nec", "ncc"),
        "cxx": os.path.join("nec", "nc++"),
        "f77": os.path.join("nec", "nfort"),
        "fc": os.path.join("nec", "nfort"),
    }

    version_argument = "--version"
    #: Regex used to extract version from compiler's output
    version_regex = r"([0-9]*\.[0-9]*\.[0-9]*)"

    @property
    def verbose_flag(self):
        return "-v"

    @property
    def debug_flags(self):
        return "-g"

    @property
    def opt_flags(self):
        return ["-O0", "-O1", "-O2", "-O3", "-O4"]

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
        return "-std=c++17"

    @property
    def cxx20_flag(self):
        return "-std=c++20"

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
