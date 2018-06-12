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


class Gtkplus3(AutotoolsPackage):
    """The GTK+ package contains libraries used for creating graphical user
       interfaces for applications."""
    homepage = "http://www.gtk.org"
    url      = "http://ftp.gnome.org/pub/gnome/sources/gtk+/3.22/gtk+-3.22.26.tar.xz"
    list_url = "http://ftp.gnome.org/pub/gnome/sources/gtk+/"
    list_depth = 2

    version('3.22.26', 'eeeb8038fe0d386c7516fa46cd4fff6b')

    depends_on('pkgconfig', type='build')
    depends_on('at-spi2-atk@2.26:')
    depends_on('gdk-pixbuf@2.36:')
    depends_on('glib@2.54:')
    depends_on('gobject-introspection@1.54:')
    # Hardcode X11 support (former +X variant),
    # see #6940 for rationale:
    depends_on('pango+X@1.40:')
    depends_on('libepoxy')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path("XDG_DATA_DIRS",
                               self.prefix.share)
        run_env.prepend_path("XDG_DATA_DIRS",
                             self.prefix.share)
