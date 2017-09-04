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

import spack.environment
import llnl.util.tty as tty


class Ldc(CMakePackage):
    """The LDC project aims to provide a portable D programming language
    compiler with modern optimization and code generation capabilities.

    LDC is fully Open Source; the parts of the code not taken/adapted from
    other projects are BSD-licensed (see the LICENSE file for details).

    Consult the D wiki for further information: http://wiki.dlang.org/LDC
    """

    homepage = "https://dlang.org/"
    url = "https://github.com/ldc-developers/ldc/releases/download/v0.17.4/ldc-0.17.4-src.tar.gz"

    version('1.3.0', '537d992a361b0fd0440b24a5145c9107')
    # This is the last version that does not require a D compiler to bootstrap
    version('0.17.4', '000e006426d6094fabd2a2bdab0ff0b7')

    depends_on('llvm@3.7:')
    depends_on('zlib')
    depends_on('libconfig')
    depends_on('curl')
    depends_on('libedit')
    depends_on('binutils')

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS:BOOL=ON'
        ]

        if self.spec.satisfies('@1.0:'):
            bootstrap = Spec('ldc@0.17.4')
            bootstrap.concretize()

            if not bootstrap.package.installed:
                # ldc greater than 0.17.X needs a D compiler to be
                # bootstrapped. There's no way currently to express
                # this in Spack with directives, hence this logic.
                tty.warn('ldc requires a D compiler to build.')
                msg = 'Bootstrapping "{0}" right now'.format(
                    bootstrap.cshort_spec
                )
                tty.warn(msg)
                bootstrap.package.do_install()

            # We need libphobos in LD_LIBRARY_PATH
            env = spack.environment.EnvironmentModifications()
            env.prepend_path('LD_LIBRARY_PATH', bootstrap.prefix.lib)
            env.apply_modifications()

            ldmd2 = join_path(bootstrap.prefix.bin, 'ldmd2')

            args.append('-DD_COMPILER:STRING={0}'.format(ldmd2))

        return args
