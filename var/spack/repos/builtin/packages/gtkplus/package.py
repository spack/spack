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


class Gtkplus(AutotoolsPackage):
    """The GTK+ 2 package contains libraries used for creating graphical user
       interfaces for applications."""
    homepage = "http://www.gtk.org"
    url = "http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-2.24.31.tar.xz"

    version('2.24.31', '68c1922732c7efc08df4656a5366dcc3afdc8791513400dac276009b40954658')
    version('2.24.25', '38af1020cb8ff3d10dda2c8807f11e92af9d2fa4045de61c62eedb7fbc7ea5b3')

    variant('X', default=False, description="Enable an X toolkit")

    depends_on('pkg-config', type='build')

    depends_on("atk")
    depends_on("gdk-pixbuf")
    depends_on("glib")
    depends_on("pango")
    depends_on("pango~X", when='~X')
    depends_on("pango+X", when='+X')
    depends_on('gobject-introspection', when='+X')

    def patch(self):
        # remove disable deprecated flag.
        filter_file(r'CFLAGS="-DGDK_PIXBUF_DISABLE_DEPRECATED $CFLAGS"',
                    '', 'configure', string=True)
