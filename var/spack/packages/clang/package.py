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
    homepage = "http://clang.llvm.org"
    list_url = "http://llvm.org/releases/download.html"

    depends_on("llvm")
    version('3.4.2', '87945973b7c73038871c5f849a818588', url='http://llvm.org/releases/3.4.2/cfe-3.4.2.src.tar.xz')

    def install(self, spec, prefix):
        env['CXXFLAGS'] = self.compiler.cxx11_flag

        with working_dir('spack-build', create=True):
            cmake('..',
                  '-DCLANG_PATH_TO_LLVM_BUILD=%s' % spec['llvm'].prefix,
                  '-DLLVM_MAIN_SRC_DIR=%s' % spec['llvm'].prefix,
                  *std_cmake_args)
            make()
            make("install")
