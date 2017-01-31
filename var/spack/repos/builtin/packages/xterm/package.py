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


class Xterm(AutotoolsPackage):
    """The xterm program is a terminal emulator for the X Window System. It
    provides DEC VT102 and Tektronix 4014 compatible terminals for programs
    that can't use the window system directly."""

    homepage = "http://invisible-island.net/xterm/"
    url      = "http://invisible-island.net/xterm/xterm-327.tgz"

    version('327', '3c32e931adcad44e64e57892e75d9e02')

    depends_on('libxft')
    depends_on('fontconfig')
    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt')
    depends_on('libx11')
    depends_on('libxinerama')
    depends_on('libxpm')
    depends_on('libice')
    depends_on('freetype')
    depends_on('libxrender')
    depends_on('libxext')
    depends_on('libsm')
    depends_on('libxcb')
    depends_on('libxau')
    depends_on('bzip2')

    depends_on('pkg-config', type='build')
