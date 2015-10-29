##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

class Clang(Package):
    """The goal of the Clang project is to create a new C, C++,
       Objective C and Objective C++ front-end for the LLVM compiler.
    """
    homepage = 'http://clang.llvm.org'
    url = 'http://llvm.org/releases/3.7.0/cfe-3.7.0.src.tar.xz'

    depends_on('llvm@3.7.0', when='@3.7.0')
    depends_on('llvm@3.6.2', when='@3.6.2')
    depends_on('llvm@3.5.1', when='@3.5.1')

    version('3.7.0', '8f9d27335e7331cf0a4711e952f21f01', url='http://llvm.org/releases/3.7.0/cfe-3.7.0.src.tar.xz')
    version('3.6.2', 'ff862793682f714bb7862325b9c06e20', url='http://llvm.org/releases/3.6.2/cfe-3.6.2.src.tar.xz')
    version('3.5.1', '93f9532f8f7e6f1d8e5c1116907051cb', url='http://llvm.org/releases/3.5.1/cfe-3.5.1.src.tar.xz')

    def install(self, spec, prefix):
        env['CXXFLAGS'] = self.compiler.cxx11_flag

        with working_dir('spack-build', create=True):
            cmake('..',
                  '-DCLANG_PATH_TO_LLVM_BUILD=%s' % spec['llvm'].prefix,
                  '-DLLVM_MAIN_SRC_DIR=%s' % spec['llvm'].prefix,
                  *std_cmake_args)
            make()
            make("install")
