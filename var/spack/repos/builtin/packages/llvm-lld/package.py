##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class LlvmLld(Package):
    """lld - The LLVM Linker
       lld is a new set of modular code for creating linker tools."""
    homepage = "http://lld.llvm.org"
    url      = "http://llvm.org/releases/3.4/lld-3.4.src.tar.gz"

    depends_on('llvm')

    version('3.4', '3b6a17e58c8416c869c14dd37682f78e')

    depends_on('cmake', type='build')

    def install(self, spec, prefix):
        env['CXXFLAGS'] = self.compiler.cxx11_flag

        with working_dir('spack-build', create=True):
            cmake('..',
                  '-DLLD_PATH_TO_LLVM_BUILD=%s' % spec['llvm'].prefix,
                  '-DLLVM_MAIN_SRC_DIR=%s' % spec['llvm'].prefix,
                  *std_cmake_args)
            make()
            make("install")
