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


class GdkPixbuf(AutotoolsPackage):
    """The Gdk Pixbuf is a toolkit for image loading and pixel buffer
       manipulation. It is used by GTK+ 2 and GTK+ 3 to load and
       manipulate images. In the past it was distributed as part of
       GTK+ 2 but it was split off into a separate package in
       preparation for the change to GTK+ 3."""
    homepage = "https://developer.gnome.org/gdk-pixbuf/"
    url      = "http://ftp.gnome.org/pub/gnome/sources/gdk-pixbuf/2.31/gdk-pixbuf-2.31.1.tar.xz"

    version('2.31.2', '6be6bbc4f356d4b79ab4226860ab8523')

    depends_on("pkg-config", type="build")
    depends_on("gettext")
    depends_on("glib")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("libtiff")
