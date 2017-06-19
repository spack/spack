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


class Libxxf86dga(AutotoolsPackage):
    """libXxf86dga - Client library for the XFree86-DGA extension."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXxf86dga"
    url      = "https://www.x.org/archive/individual/lib/libXxf86dga-1.1.4.tar.gz"

    version('1.1.4', '8ed1c8674e730e8d333dfe4b9f2097d9')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xproto', type='build')
    depends_on('xextproto', type='build')
    depends_on('xf86dgaproto@2.0.99.2:', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
