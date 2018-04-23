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


class Libxxf86vm(AutotoolsPackage):
    """libXxf86vm - Extension library for the XFree86-VidMode X extension."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXxf86vm"
    url      = "https://www.x.org/archive/individual/lib/libXxf86vm-1.1.4.tar.gz"

    version('1.1.4', '675bd0c521472628d5796602f625ef51')

    depends_on('libx11@1.6:')
    depends_on('libxext')

    depends_on('xproto', type='build')
    depends_on('xextproto', type='build')
    depends_on('xf86vidmodeproto@2.2.99.1:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
