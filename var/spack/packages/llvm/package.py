##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by David Beckingsale, david@llnl.gov, All rights reserved.
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


class Llvm(Package):
    """The LLVM Project is a collection of modular and reusable compiler and
       toolchain technologies. Despite its name, LLVM has little to do with
       traditional virtual machines, though it does provide helpful libraries
       that can be used to build them. The name "LLVM" itself is not an acronym;
       it is the full name of the project.
    """
    homepage = 'http://llvm.org/'
    url = 'http://llvm.org/releases/3.7.0/llvm-3.7.0.src.tar.xz'

    version('3.7.0', 'b98b9495e5655a672d6cb83e1a180f8e', url='http://llvm.org/releases/3.7.0/llvm-3.7.0.src.tar.xz')
    version('3.6.2', '0c1ee3597d75280dee603bae9cbf5cc2', url='http://llvm.org/releases/3.6.2/llvm-3.6.2.src.tar.xz')
    version('3.5.1', '2d3d8004f38852aa679e5945b8ce0b14', url='http://llvm.org/releases/3.5.1/llvm-3.5.1.src.tar.xz')
    version('3.0', 'a8e5f5f1c1adebae7b4a654c376a6005', url='http://llvm.org/releases/3.0/llvm-3.0.tar.gz') # currently required by mesa package

    depends_on('python@2.7:')

    variant('libcxx', default=False, description="Builds the LLVM Standard C++ library targeting C++11")

    ##########
    # @3.7.0
    resource(name='compiler-rt',
             url='http://llvm.org/releases/3.7.0/compiler-rt-3.7.0.src.tar.xz', md5='383c10affd513026f08936b5525523f5',
             destination='projects', when='@3.7.0')
    resource(name='openmp',
             url='http://llvm.org/releases/3.7.0/openmp-3.7.0.src.tar.xz', md5='f482c86fdead50ba246a1a2b0bbf206f',
             destination='projects', when='@3.7.0')
    resource(name='libcxx',
             url='http://llvm.org/releases/3.7.0/libcxx-3.7.0.src.tar.xz', md5='46aa5175cbe1ad42d6e9c995968e56dd',
             destination='projects', placement='libcxx', when='+libcxx@3.7.0')
    resource(name='libcxxabi',
             url='http://llvm.org/releases/3.7.0/libcxxabi-3.7.0.src.tar.xz', md5='5aa769e2fca79fa5335cfae8f6258772',
             destination='projects', placement='libcxxabi', when='+libcxx@3.7.0')
    ##########

    def install(self, spec, prefix):
        env['CXXFLAGS'] = self.compiler.cxx11_flag

        with working_dir('spack-build', create=True):
            cmake('..',
                  '-DLLVM_REQUIRES_RTTI:BOOL=ON',
                  '-DPYTHON_EXECUTABLE:PATH=%s/bin/python' % spec['python'].prefix,
                  *std_cmake_args)
            make()
            make("install")
