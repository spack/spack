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


class XorgServer(AutotoolsPackage):
    """X.Org Server is the free and open source implementation of the display
    server for the X Window System stewarded by the X.Org Foundation."""

    homepage = "http://cgit.freedesktop.org/xorg/xserver"
    url      = "https://www.x.org/archive/individual/xserver/xorg-server-1.18.99.901.tar.gz"

    version('1.18.99.901', 'd0242b95991c221c4fcc0d283aba7a42')

    depends_on('pixman@0.27.2:')
    depends_on('font-util')
    depends_on('libxshmfence@1.1:')
    depends_on('libdrm@2.3.0:')
    depends_on('libx11')
    depends_on('mesa+hwrender', type='build')

    depends_on('dri2proto@2.8:', type='build')
    depends_on('dri3proto@1.0:', type='build')
    depends_on('glproto@1.4.17:', type='build')

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
    depends_on('fixesproto@5.0:')
    depends_on('damageproto@1.1:')
    depends_on('xcmiscproto@1.2.0:')
    depends_on('xtrans@1.3.5:')
    depends_on('bigreqsproto@1.1.0:')
    depends_on('xproto@7.0.28:')
    depends_on('randrproto@1.5.0:')
    depends_on('renderproto@0.11:')
    depends_on('xextproto@7.2.99.901:')
    depends_on('inputproto@2.3:')
    depends_on('kbproto@1.0.3:')
    depends_on('fontsproto@2.1.3:')
    depends_on('pixman@0.27.2:')
    depends_on('videoproto')
    depends_on('compositeproto@0.4:')
    depends_on('recordproto@1.13.99.1:')
    depends_on('scrnsaverproto@1.1:')
    depends_on('resourceproto@1.2.0:')
    depends_on('xf86driproto@2.1.0:')
    depends_on('glproto@1.4.17:')
    depends_on('presentproto@1.0:')
    depends_on('xineramaproto')
    depends_on('libxkbfile')
    depends_on('libxfont2')
    depends_on('libxext')
    depends_on('libxdamage')
    depends_on('libxfixes')
    depends_on('libepoxy')
