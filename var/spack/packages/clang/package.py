##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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

import os
import os.path

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

    ##########
    # @3.7.0
    resource(name='clang-tools-extra',
             url='http://llvm.org/releases/3.7.0/clang-tools-extra-3.7.0.src.tar.xz',
             md5='d5a87dacb65d981a427a536f6964642e', destination='tools', when='@3.7.0')
    ##########

    def install(self, spec, prefix):
        env['CXXFLAGS'] = self.compiler.cxx11_flag

        with working_dir('spack-build', create=True):

            options = []
            if '@3.7.0:' in spec:
                options.append('-DCLANG_DEFAULT_OPENMP_RUNTIME:STRING=libomp')
            options.extend(std_cmake_args)

            cmake('..',
                  '-DCLANG_PATH_TO_LLVM_BUILD:PATH=%s' % spec['llvm'].prefix,
                  '-DLLVM_MAIN_SRC_DIR:PATH=%s' % spec['llvm'].prefix,
                  *options)
            make()
            make("install")
            # CLang doesn't look in llvm folders for system headers...
            self.link_llvm_directories(spec)

    def link_llvm_directories(self, spec):

        def clang_include_dir_at(root):
            return join_path(root, 'include')

        def clang_lib_dir_at(root):
            return join_path(root, 'lib/clang/', str(self.version), 'include')

        def do_link(source_dir, destination_dir):
            if os.path.exists(source_dir):
                for name in os.listdir(source_dir):
                    source = join_path(source_dir, name)
                    link = join_path(destination_dir, name)
                    os.symlink(source, link)

        # Link folder and files in include
        llvm_dir = clang_include_dir_at(spec['llvm'].prefix)
        clang_dir = clang_include_dir_at(self.prefix)
        do_link(llvm_dir, clang_dir)
        # Link folder and files in lib
        llvm_dir = clang_lib_dir_at(spec['llvm'].prefix)
        clang_dir = clang_lib_dir_at(self.prefix)
        do_link(llvm_dir, clang_dir)