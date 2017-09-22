##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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
import os


class Flang(CMakePackage):
    """Flang is a Fortran compiler targeting LLVM."""
    homepage = "https://github.com/flang-compiler/flang"
    url      = "https://github.com/flang-compiler/flang/flecsi/tarball/v1.0"

    version('develop', git='https://github.com/flang-compiler/flang', branch='master')

    depends_on(
        "llvm+clang",
        patches=patch('https://github.com/llvm-mirror/clang/pull/33.diff',
                      sha256='e46d7ab305e5e95c51f4656d9b52058143cd85d859b312b3c80e93a02d54b4a5',
                      when='@4.0.1', level=1, working_dir='tools/clang'))

    def patch(self):
        # Don't use -Werror
        # https://github.com/flang-compiler/flang/pull/85
        filter_file(r'-Werror', '', 'CMakeLists.txt')

    def cmake_args(self):
        options = [
            '-DCMAKE_C_COMPILER=%s' % os.path.join(
                self.spec['llvm'].prefix.bin, 'clang'),
            '-DCMAKE_CXX_COMPILER=%s' % os.path.join(
                self.spec['llvm'].prefix.bin, 'clang++'),
            '-DCMAKE_Fortran_COMPILER=%s' % os.path.join(
                self.spec['llvm'].prefix.bin, 'flang'),
            '-DFLANG_LIBOMP=%s' % find_libraries(
                'libomp', root=self.spec['llvm'].prefix.lib)
        ]

        return options
