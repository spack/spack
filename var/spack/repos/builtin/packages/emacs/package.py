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

import sys


class Emacs(AutotoolsPackage):
    """The Emacs programmable text editor."""

    homepage = "https://www.gnu.org/software/emacs"
    url      = "https://ftpmirror.gnu.org/emacs/emacs-24.5.tar.gz"

    version('26.1', '544d2ab5eb142e9ca69adb023d17bf4b')
    version('25.3', '74ddd373dc52ac05ca7a8c63b1ddbf58')
    version('25.2', '0a36d1cdbba6024d4dbbac027f87995f')
    version('25.1', '95c12e6a9afdf0dcbdd7d2efa26ca42c')
    version('24.5', 'd74b597503a68105e61b5b9f6d065b44')

    variant('X', default=False, description="Enable an X toolkit")
    variant(
        'toolkit',
        default='gtk',
        values=('gtk', 'athena'),
        description="Select an X toolkit (gtk, athena)"
    )
    variant('tls', default=False, description="Build Emacs with gnutls")

    depends_on('pkgconfig', type='build')

    depends_on('ncurses')
    depends_on('pcre')
    depends_on('zlib')
    depends_on('libtiff', when='+X')
    depends_on('libpng', when='+X')
    depends_on('libxpm', when='+X')
    depends_on('giflib', when='+X')
    depends_on('libx11', when='+X')
    depends_on('libxaw', when='+X toolkit=athena')
    depends_on('gtkplus', when='+X toolkit=gtk')
    depends_on('gnutls', when='+tls')

    def configure_args(self):
        spec = self.spec

        toolkit = spec.variants['toolkit'].value
        if '+X' in spec:
            args = [
                '--with-x',
                '--with-x-toolkit={0}'.format(toolkit)
            ]
        else:
            args = ['--without-x']

        # On OS X/macOS, do not build "nextstep/Emacs.app", because
        # doing so throws an error at build-time
        if sys.platform == 'darwin':
            args.append('--without-ns')

        if '+tls' in spec:
            args.append('--with-gnutls')
        else:
            args.append('--without-gnutls')

        return args
