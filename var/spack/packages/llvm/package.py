##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by David Beckingsale, david@llnl.gov, All rights reserved.
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

class Llvm(Package):
    """The LLVM Project is a collection of modular and reusable compiler and
       toolchain technologies. Despite its name, LLVM has little to do with
       traditional virtual machines, though it does provide helpful libraries
       that can be used to build them. The name "LLVM" itself is not an acronym;
       it is the full name of the project.
    """
    homepage = "http://llvm.org/"
    list_url = "http://llvm.org/releases/download.html"

    version('3.5.1', '2d3d8004f38852aa679e5945b8ce0b14', url='http://llvm.org/releases/3.5.1/llvm-3.5.1.src.tar.xz')
    version('3.4.2', 'a20669f75967440de949ac3b1bad439c', url='http://llvm.org/releases/3.4.2/llvm-3.4.2.src.tar.gz')
    version('3.0',   'a8e5f5f1c1adebae7b4a654c376a6005', url='http://llvm.org/releases/3.0/llvm-3.0.tar.gz')
    version('2.9',   '793138412d2af2c7c7f54615f8943771', url='http://llvm.org/releases/2.9/llvm-2.9.tgz')
    version('2.8',   '220d361b4d17051ff4bb21c64abe05ba', url='http://llvm.org/releases/2.8/llvm-2.8.tgz')

    def install(self, spec, prefix):
        env['CXXFLAGS'] = self.compiler.cxx11_flag

        with working_dir('spack-build', create=True):
            cmake('..',
                  '-DLLVM_REQUIRES_RTTI=1',
                  '-DPYTHON_EXECUTABLE=/usr/bin/python',
                  '-DPYTHON_INCLUDE_DIR=/usr/include/python2.6',
                  '-DPYTHON_LIBRARY=/usr/lib64/libpython2.6.so',
                  *std_cmake_args)
            make()
            make("install")
