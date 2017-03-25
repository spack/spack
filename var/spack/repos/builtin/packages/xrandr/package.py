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


class Xrandr(AutotoolsPackage):
    """xrandr - primitive command line interface to X11 Resize, Rotate, and
    Reflect (RandR) extension."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xrandr"
    url      = "https://www.x.org/archive/individual/app/xrandr-1.5.0.tar.gz"

    version('1.5.0', 'fe9cf76033fe5d973131eac67b6a3118')

    depends_on('libxrandr@1.5:')
    depends_on('libxrender')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
