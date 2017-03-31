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


class Ncurses(AutotoolsPackage):
    """The ncurses (new curses) library is a free software emulation of
    curses in System V Release 4.0, and more. It uses terminfo format,
    supports pads and color and multiple highlights and forms
    characters and function-key mapping, and has all the other
    SYSV-curses enhancements over BSD curses."""

    homepage = "http://invisible-island.net/ncurses/ncurses.html"
    url      = "http://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.0.tar.gz"

    version('6.0', 'ee13d052e1ead260d7c28071f46eefb1')
    version('5.9', '8cb9c412e5f2d96bc6f459aa8c6282a1')

    variant('symlinks', default=False,
            description='Enables symlinks. Needed on AFS filesystem.')

    # Use mawk instead of gawk to prevent a circular dependency
    depends_on('mawk',       type='build')
    depends_on('pkg-config', type='build')

    patch('patch_gcc_5.txt', when='@6.0%gcc@5.0:')
    patch('sed_pgi.patch',   when='@:6.0')

    def configure_args(self):
        opts = [
            'AWK=mawk',
            'CFLAGS={0}'.format(self.compiler.pic_flag),
            'CXXFLAGS={0}'.format(self.compiler.pic_flag),
            '--with-shared',
            '--with-cxx-shared',
            '--enable-widec',
            '--enable-overwrite',
            '--disable-lib-suffixes',
            '--without-ada',
            '--enable-pc-files',
            '--with-pkg-config-libdir={0}/lib/pkgconfig'.format(self.prefix)
        ]

        if '+symlinks' in self.spec:
            opts.append('--enable-symlinks')

        return opts
