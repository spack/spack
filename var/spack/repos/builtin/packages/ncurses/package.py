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

class Ncurses(Package):
    """The ncurses (new curses) library is a free software emulation of curses
       in System V Release 4.0, and more. It uses terminfo format, supports pads and
       color and multiple highlights and forms characters and function-key mapping,
       and has all the other SYSV-curses enhancements over BSD curses.
    """

    homepage = "http://invisible-island.net/ncurses/ncurses.html"
    url      = "http://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.0.tar.gz"

    version('6.0', 'ee13d052e1ead260d7c28071f46eefb1')
    version('5.9', '8cb9c412e5f2d96bc6f459aa8c6282a1')

    patch('patch_gcc_5.txt', when='%gcc@5.0:')

    def install(self, spec, prefix):
        opts = [
            "--prefix=%s" % prefix,
            "--with-shared",
            "--with-cxx-shared",
            "--enable-widec",
            "--enable-overwrite",
            "--disable-lib-suffixes",
            "--without-ada"]
        configure(*opts)
        make()
        make("install")
