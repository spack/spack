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


class Gnuplot(AutotoolsPackage):
    """Gnuplot is a portable command-line driven graphing utility for Linux,
       OS/2, MS Windows, OSX, VMS, and many other platforms. The source
       code is copyrighted but freely distributed (i.e., you don't have
       to pay for it). It was originally created to allow scientists and
       students to visualize mathematical functions and data
       interactively, but has grown to support many non-interactive uses
       such as web scripting. It is also used as a plotting engine by
       third-party applications like Octave. Gnuplot has been supported
       and under active development since 1986

    """
    homepage = "http://www.gnuplot.info"
    url      = "http://downloads.sourceforge.net/project/gnuplot/gnuplot/5.0.1/gnuplot-5.0.1.tar.gz"

    # There is a conflict in term.h between gnuplot and ncurses, which is a
    # dependency of readline. Fix it with a small patch
    patch('term_include.patch')

    version('5.0.5', 'c5e96fca73afbee4f57cbc1bfce6b3b8')
    version('5.0.1', '79b4f9e203728f76b60b28bcd402d3c7')

    variant('wx',      default=False,
            description='Activates wxWidgets terminal')
    variant('gd',      default=True,
            description='Activates gd based terminal')
    variant('cairo',   default=True,
            description='Activates cairo based terminal')
    variant('X',       default=False,
            description='Build with X11')
    variant('libcerf', default=True,
            description='Build with libcerf support')
    variant('pbm',     default=False,
            description='Enable PBM (Portable Bit Map) and other older bitmap terminals')  # NOQA: ignore=E501

    # required dependencies
    depends_on('readline')
    depends_on('pkg-config', type='build')
    depends_on('libxpm')
    depends_on('libiconv')

    # optional dependencies:
    depends_on('libcerf', when='+libcerf')
    depends_on('libgd', when='+gd')
    depends_on('cairo@1.2:', when='+cairo')
    depends_on('wx', when='+wx')
    depends_on('pango@1.10:', when='+wx')
    depends_on('pango@1.10:', when='+cairo')

    def configure_args(self):
        # see https://github.com/Homebrew/homebrew-core/blob/master/Formula/gnuplot.rb
        # and https://github.com/macports/macports-ports/blob/master/math/gnuplot/Portfile
        spec = self.spec
        options = [
            '--disable-dependency-tracking',
            '--disable-silent-rules',
            # Per upstream: "--with-tutorial is horribly out of date."
            '--without-tutorial',
            '--with-readline=%s' % spec['readline'].prefix
        ]

        if '+pbm' in spec:
            options.append('--with-bitmap-terminals')
        else:
            options.append('--without-bitmap-terminals')

        if '+X' in spec:
            # It seems there's an open bug for wxWidgets support
            # See : http://sourceforge.net/p/gnuplot/bugs/1694/
            os.environ['TERMLIBS'] = '-lX11'
            options.append('--with-x')
        else:
            options.append('--without-x')

        if '+wx' in spec:
            options.append('--with-wx=%s' % spec['wx'].prefix)
        else:
            options.append('--disable-wxwidgets')

        if '+gd' in spec:
            options.append('--with-gd=%s' % spec['libgd'].prefix)
        else:
            options.append('--without-gd')

        if '+cairo' in spec:
            options.append('--with-cairo')
        else:
            options.append('--without-cairo')

        if '+libcerf' in spec:
            options.append('--with-libcerf')
        else:
            options.append('--without-libcerf')

        # TODO: Enable pdflib-based pdf terminal
        # '--with-pdf=%s' % spec['pdflib-lite'].prefix  (or pdflib)
        options.append('--without-pdf')

        # TODO: Enable qt terminal qt@5.7
        options.append('--with-qt=no')

        # TODO: Enable lua-based terminals
        options.append('--without-lua')

        # TODO: --with-latex
        options.append('--without-latex')

        # TODO: --with-aquaterm  depends_on('aquaterm')
        options.append('--without-aquaterm')

        return options
