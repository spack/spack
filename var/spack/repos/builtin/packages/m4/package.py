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

class M4(Package):
    """GNU M4 is an implementation of the traditional Unix macro processor."""
    homepage = "https://www.gnu.org/software/m4/m4.html"
    url      = "ftp://ftp.gnu.org/gnu/m4/m4-1.4.17.tar.gz"

    version('1.4.17', 'a5e9954b1dae036762f7b13673a2cf76')

    patch('pgi.patch', when='@1.4.17')

    variant('sigsegv', default=True, description="Build the libsigsegv dependency")

    depends_on('libsigsegv', when='+sigsegv')

    def install(self, spec, prefix):
        configure_args = []
        if 'libsigsegv' in spec:
            configure_args.append('--with-libsigsegv-prefix=%s' % spec['libsigsegv'].prefix)
        else:
            configure_args.append('--without-libsigsegv-prefix')

        configure("--prefix=%s" % prefix, *configure_args)
        make()
        make("install")
