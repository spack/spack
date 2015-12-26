##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *

import os

class Gnuplot(Package):
    """
    Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other
    platforms. The source code is copyrighted but freely distributed (i.e., you don't have to pay for it). It was
    originally created to allow scientists and students to visualize mathematical functions and data interactively,
    but has grown to support many non-interactive uses such as web scripting. It is also used as a plotting engine by
    third-party applications like Octave. Gnuplot has been supported and under active development since 1986
    """
    homepage = "http://www.gnuplot.info"
    url      = "http://downloads.sourceforge.net/project/gnuplot/gnuplot/5.0.1/gnuplot-5.0.1.tar.gz"

    version('5.0.1', '79b4f9e203728f76b60b28bcd402d3c7')

    depends_on('readline')
    depends_on('libcerf')
    depends_on('libgd')
    depends_on('cairo')
    depends_on('pango')
    depends_on('wx', when='+wx')

    variant('wx', default=False, description='Activates wxWidgets terminal')

    def install(self, spec, prefix):
        # It seems there's an open bug for wxWidgets support
        # See : http://sourceforge.net/p/gnuplot/bugs/1694/
        os.environ['TERMLIBS'] = '-lX11'

        options = ['--prefix=%s' % prefix]

        configure(*options)
        make()
        make("install")
