# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Clingo(CMakePackage):
    """Clingo: A grounder and solver for logic programs

       Clingo is part of the Potassco project for Answer Set
       Programming (ASP). ASP offers a simple and powerful modeling
       language to describe combinatorial problems as logic
       programs. The clingo system then takes such a logic program and
       computes answer sets representing solutions to the given
       problem."""

    homepage = "https://potassco.org/clingo/"
    url      = "https://github.com/potassco/clingo/archive/v5.2.2.tar.gz"

    version('5.4.0', sha256='e2de331ee0a6d254193aab5995338a621372517adcf91568092be8ac511c18f3')
    version('5.3.0', sha256='b0d406d2809352caef7fccf69e8864d55e81ee84f4888b0744894977f703f976')
    version('5.2.2', sha256='da1ef8142e75c5a6f23c9403b90d4f40b9f862969ba71e2aaee9a257d058bfcf')

    depends_on('doxygen', type=('build'))
    depends_on('python')

    def cmake_args(self):
        try:
            self.compiler.cxx14_flag
        except UnsupportedCompilerFlag:
            InstallError('clingo requires a C++14-compliant C++ compiler')

        args = ['-DCLINGO_BUILD_WITH_PYTHON=ON',
                '-DCLING_BUILD_PY_SHARED=ON',
                '-DPYCLINGO_USE_INSTALL_PREFIX=ON',
                '-DCLINGO_BUILD_WITH_LUA=OFF']
        return args
