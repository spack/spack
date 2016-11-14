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


class Gtkplus(Package):
    """The GTK+ 2 package contains libraries used for creating graphical user
       interfaces for applications."""
    homepage = "http://www.gtk.org"

    version(
        '2.24.25', '612350704dd3aacb95355a4981930c6f',
        url="http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-2.24.25.tar.xz")

    depends_on("atk")
    depends_on("gdk-pixbuf")
    depends_on("pango")
    depends_on("glib")

    def patch(self):
        # remove disable deprecated flag.
        filter_file(r'CFLAGS="-DGDK_PIXBUF_DISABLE_DEPRECATED $CFLAGS"',
                    '', 'configure', string=True)

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
