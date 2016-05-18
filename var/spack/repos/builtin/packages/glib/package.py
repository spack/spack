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
import sys

class Glib(Package):
    """The GLib package contains a low-level libraries useful for
       providing data structure handling for C, portability wrappers
       and interfaces for such runtime functionality as an event loop,
       threads, dynamic loading and an object system."""
    homepage = "https://developer.gnome.org/glib/"
    url      = "http://ftp.gnome.org/pub/gnome/sources/glib/2.42/glib-2.42.1.tar.xz"

    version('2.42.1', '89c4119e50e767d3532158605ee9121a')

    depends_on("libffi")
    depends_on("zlib")
    depends_on("pkg-config")
    depends_on('gettext', sys.platform=='darwin')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install", parallel=False)
