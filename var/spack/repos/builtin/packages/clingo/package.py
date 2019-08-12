# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    version('5.2.2', 'd46a1567f772eebad85c6300d55d2cc3')

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
