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
import llnl.util.tty as tty


class Emacs(Package):
    """The Emacs programmable text editor."""

    homepage = "https://www.gnu.org/software/emacs"
    url      = "http://ftp.gnu.org/gnu/emacs/emacs-24.5.tar.gz"

    version('24.5', 'd74b597503a68105e61b5b9f6d065b44')

    variant('X', default=True, description="Enable a X toolkit (GTK+)")
    variant('gtkplus', default=False, description="Enable a GTK+ as X toolkit (this variant is ignored if ~X)")

    depends_on('ncurses')
    depends_on('libtiff', when='+X')
    depends_on('libpng', when='+X')
    depends_on('libxpm', when='+X')
    depends_on('giflib', when='+X')
    depends_on('gtkplus', when='+X+gtkplus')

    def install(self, spec, prefix):
        args = []
        if '+X' in spec:
            if '+gtkplus' in spec:
                toolkit = 'gtk{0}'.format(spec['gtkplus'].version.up_to(1))
            else:
                toolkit = 'no'
            args = [
                '--with-x',
                '--with-x-toolkit={0}'.format(toolkit)
            ]
        else:
            args = ['--without-x']
            if '+gtkplus' in spec:
                tty.warn('The variant +gtkplus is ignored if ~X is selected.')

        configure('--prefix={0}'.format(prefix), *args)

        make()
        make("install")
