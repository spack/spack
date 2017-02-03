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


class Emacs(AutotoolsPackage):
    """The Emacs programmable text editor."""

    homepage = "https://www.gnu.org/software/emacs"
    url      = "http://ftp.gnu.org/gnu/emacs/emacs-24.5.tar.gz"

    version('25.1', '95c12e6a9afdf0dcbdd7d2efa26ca42c')
    version('24.5', 'd74b597503a68105e61b5b9f6d065b44')

    variant('X', default=False, description="Enable an X toolkit")
    variant('toolkit', default='gtk',
            description="Select an X toolkit (gtk, athena)")

    depends_on('ncurses')
    depends_on('libtiff', when='+X')
    depends_on('libpng', when='+X')
    depends_on('libxpm', when='+X')
    depends_on('giflib', when='+X')
    depends_on('libx11', when='+X')
    depends_on('libxaw', when='+X toolkit=athena')
    depends_on('gtkplus+X', when='+X toolkit=gtk')

    def configure_args(self):
        spec = self.spec
        args = []
        toolkit = spec.variants['toolkit'].value
        if '+X' in spec:
            if toolkit not in ('gtk', 'athena'):
                raise InstallError("toolkit must be in (gtk, athena), not %s" %
                                   toolkit)
            args = [
                '--with-x',
                '--with-x-toolkit={0}'.format(toolkit)
            ]
        else:
            args = ['--without-x']

        return args
