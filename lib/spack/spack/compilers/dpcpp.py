# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.compilers.oneapi


class Dpcpp(spack.compilers.oneapi.Oneapi):
    """This is the same as the oneAPI compiler but uses dpcpp instead of
    icpx (for DPC++ source files). It explicitly refers to dpcpp, so that
    CMake test files which check the compiler name (e.g. CMAKE_CXX_COMPILER)
    detect it as dpcpp.

    Ideally we could switch out icpx for dpcpp where needed in the oneAPI
    compiler definition, but two things are needed for that: (a) a way to
    tell the compiler that it should be using dpcpp and (b) a way to
    customize the link_paths

    See also: https://www.intel.com/content/www/us/en/develop/documentation/oneapi-dpcpp-cpp-compiler-dev-guide-and-reference/top/compiler-setup/using-the-command-line/invoking-the-compiler.html
    """

    # Subclasses use possible names of C++ compiler
    cxx_names = ["dpcpp"]

    # Named wrapper links within build_env_path
    link_paths = {
        "cc": os.path.join("oneapi", "icx"),
        "cxx": os.path.join("oneapi", "dpcpp"),
        "f77": os.path.join("oneapi", "ifx"),
        "fc": os.path.join("oneapi", "ifx"),
    }
