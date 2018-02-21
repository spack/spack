##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class LlvmLld(CMakePackage):
    """lld - The LLVM Linker
       lld is a new set of modular code for creating linker tools."""
    homepage = "http://lld.llvm.org"
    url      = "http://llvm.org/releases/3.4/lld-3.4.src.tar.xz"

    version('5.0.1', 'a873c7fdaac647613d8eed2cb03d82de')
    version('5.0.0', 'a39cbecced3263feab9139b47118e062')
    version('4.0.1', '39cd3512cddcfd7d37ef12066c961660')
    version('4.0.0', 'e5784656e0f38e3578f10ff7551d3896')
    version('3.9.1', '6254dd138e23b098df4ef7840c11e2c8')
    version('3.9.0', 'c23c895c0d855a0dc426af686538a95e')
    version('3.8.1', '68cd069bf99c71ebcfbe01d557c0e14d')
    version('3.8.0', 'de33b5c6c77698ee2f8d024fbffb8df1')
    version('3.7.1', '6c3794e30fbe118a601fb694627f34f8')
    version('3.7.0', '91bd593a67293d84dad0bf11845546c2')
    version('3.6.2', '7143cc4fa88851a9f9b9a03621fbb387')
    version('3.5.1', '173be02b7ff4e5e31fbb0a591a03d7a3')

    # The llvm-lld and llvm versions must match
    depends_on('llvm@5.0.1', when='@5.0.1')
    depends_on('llvm@5.0.0', when='@5.0.0')
    depends_on('llvm@4.0.1', when='@4.0.1')
    depends_on('llvm@4.0.0', when='@4.0.0')
    depends_on('llvm@3.9.1', when='@3.9.1')
    depends_on('llvm@3.9.0', when='@3.9.0')
    depends_on('llvm@3.8.1', when='@3.8.1')
    depends_on('llvm@3.8.0', when='@3.8.0')
    depends_on('llvm@3.7.1', when='@3.7.1')
    depends_on('llvm@3.7.0', when='@3.7.0')
    depends_on('llvm@3.6.2', when='@3.6.2')
    depends_on('llvm@3.5.1', when='@3.5.1')

    depends_on('cmake@2.8:', type='build')

    def cmake_args(self):
        if 'CXXFLAGS' in env and env['CXXFLAGS']:
            env['CXXFLAGS'] += ' ' + self.compiler.cxx11_flag
        else:
            env['CXXFLAGS'] = self.compiler.cxx11_flag

        return [
            '-DLLD_PATH_TO_LLVM_BUILD=%s' % self.spec['llvm'].prefix,
            '-DLLVM_MAIN_SRC_DIR=%s' % self.spec['llvm'].prefix,
        ]
