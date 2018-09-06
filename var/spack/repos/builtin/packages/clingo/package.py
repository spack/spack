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
