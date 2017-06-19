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
    # depends_on('gl@9.2.0:')

    depends_on('dri2proto@2.8:', type='build')
    depends_on('dri3proto@1.0:', type='build')
    depends_on('glproto@1.4.17:', type='build')

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')

    # TODO: add missing dependencies
    # $LIBSELINUX $REQUIRED_MODULES $REQUIRED_LIBS
    # $LIBPCIACCESS $DGAPROTO $XORG_MODULES epoxy xdmcp xau xfixes x11-xcb
    # xcb-aux xcb-image xcb-ewmh xcb-icccm $WINDOWSWMPROTO windowsdriproto
    # khronos-opengl-registry
    # $APPLEWMPROTO $LIBAPPLEWM xfixes $LIBDMX $LIBXEXT $LIBDMX xmu $LIBXEXT
    # $LIBDMX $LIBXI $LIBXEXT $LIBXTST $LIBXEXT xres $LIBXEXT $LIBXEXT
    # $XEPHYR_REQUIRED_LIBS

    # VIDEOPROTO="videoproto"
    # COMPOSITEPROTO="compositeproto >= 0.4"
    # RECORDPROTO="recordproto >= 1.13.99.1"
    # SCRNSAVERPROTO="scrnsaverproto >= 1.1"
    # RESOURCEPROTO="resourceproto >= 1.2.0"
    # DRIPROTO="xf86driproto >= 2.1.0"
    # XINERAMAPROTO="xineramaproto"
    # BIGFONTPROTO="xf86bigfontproto >= 1.2.0"
    # DGAPROTO="xf86dgaproto >= 2.0.99.1"
    # DMXPROTO="dmxproto >= 2.2.99.1"
    # VIDMODEPROTO="xf86vidmodeproto >= 2.2.99.1"
    # WINDOWSWMPROTO="windowswmproto"
    # APPLEWMPROTO="applewmproto >= 1.4"

    # XPROTO="xproto >= 7.0.28"
    # RANDRPROTO="randrproto >= 1.5.0"
    # RENDERPROTO="renderproto >= 0.11"
    # XEXTPROTO="xextproto >= 7.2.99.901"
    # INPUTPROTO="inputproto >= 2.3"
    # KBPROTO="kbproto >= 1.0.3"
    # FONTSPROTO="fontsproto >= 2.1.3"
    # FIXESPROTO="fixesproto >= 5.0"
    # DAMAGEPROTO="damageproto >= 1.1"
    # XCMISCPROTO="xcmiscproto >= 1.2.0"
    # BIGREQSPROTO="bigreqsproto >= 1.1.0"
    # XTRANS="xtrans >= 1.3.5"
    # PRESENTPROTO="presentproto >= 1.0"

    # LIBAPPLEWM="applewm >= 1.4"
    # LIBDMX="dmx >= 1.0.99.1"
    # LIBDRI="dri >= 7.8.0"
    # LIBEGL="egl"
    # LIBGBM="gbm >= 10.2.0"
    # LIBXEXT="xext >= 1.0.99.4"
    # LIBXFONT="xfont2 >= 2.0.0"
    # LIBXI="xi >= 1.2.99.1"
    # LIBXTST="xtst >= 1.0.99.2"
    # LIBPCIACCESS="pciaccess >= 0.12.901"
    # LIBUDEV="libudev >= 143"
    # LIBSELINUX="libselinux >= 2.0.86"
    # LIBDBUS="dbus-1 >= 1.0"
