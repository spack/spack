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
import os


class Ghc(Package):
    """The Glasgow Haskell Compiler is a state-of-the-art, open source
       compiler and interactive environment for the functional language
       Haskell."""
    homepage = "https://www.haskell.org/ghc/"
    url      = "http://downloads.haskell.org/~ghc/8.0.1/ghc-8.0.1-src.tar.xz"

    version('8.0.1', 'c185b8a1f3e67e43533ec590b751c2ff')

    depends_on('gmp')
    depends_on('ncurses')
    depends_on('libffi')
    depends_on('libedit')       # docs say, but I can't see where.
    depends_on('perl')
    depends_on('python')
    depends_on('py-sphinx')

    def install(self, spec, prefix):
        bootstrap_ghc = which('ghc')
        configure_args = [
            "--prefix=%s" % prefix,
            "--with-ghc=%s" % bootstrap_ghc,
            "--with-gmp-includes=%s" % spec['gmp'].prefix.include,
            "--with-gmp-libraries=%s" % spec['gmp'].prefix.lib,
            "--with-curses-includes=%s" % spec['ncurses'].prefix.include,
            "--with-curses-libraries=%s" % spec['ncurses'].prefix.lib,
            "--with-ffi-includes=%s" % spec['libffi'].prefix.include,
            "--with-ffi-libraries=%s" % spec['libffi'].prefix.lib,
        ]
        configure(*configure_args)
        make()
        make('install')
