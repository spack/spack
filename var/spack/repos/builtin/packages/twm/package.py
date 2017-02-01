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


class Twm(AutotoolsPackage):
    """twm is a window manager for the X Window System.  It provides
    titlebars, shaped windows, several forms of icon management,
    user-defined macro functions, click-to-type and pointer-driven
    keyboard focus, and user-specified key and pointer button bindings."""

    homepage = "http://cgit.freedesktop.org/xorg/app/twm"
    url      = "https://www.x.org/archive/individual/app/twm-1.0.9.tar.gz"

    version('1.0.9', 'e98fcb32f774ac1ff7bf82101b79f61e')

    depends_on('libx11')
    depends_on('libxext')
    depends_on('libxt')
    depends_on('libxmu')
    depends_on('libice')
    depends_on('libsm')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
