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


class LdcBootstrap(CMakePackage):
    """The LDC project aims to provide a portable D programming language
    compiler with modern optimization and code generation capabilities.

    LDC is fully Open Source; the parts of the code not taken/adapted from
    other projects are BSD-licensed (see the LICENSE file for details).

    Consult the D wiki for further information: http://wiki.dlang.org/LDC

    This old version of the compiler is needed to bootstrap newer ones.
    """

    homepage = "https://dlang.org/"
    url = "https://github.com/ldc-developers/ldc/releases/download/v0.17.4/ldc-0.17.4-src.tar.gz"

    # This is the last version that does not require a D compiler to bootstrap
    version('0.17.4', '000e006426d6094fabd2a2bdab0ff0b7')

    depends_on('llvm@3.7:')
    depends_on('zlib')
    depends_on('libconfig')
    depends_on('curl')
    depends_on('libedit')
    depends_on('binutils')

    def setup_dependent_environment(self, build_env, run_env, dep_spec):

        # The code below relies on this function being executed after the
        # environment has been sanitized (because LD_LIBRARY_PATH is among
        # the variables that get unset)

        # We need libphobos in LD_LIBRARY_PATH
        build_env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)

    def cmake_args(self):
        return [
            '-DBUILD_SHARED_LIBS:BOOL=ON'
        ]
