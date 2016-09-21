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


class Compiz(Package):
    """compiz - OpenGL window and compositing manager.

    Compiz is an OpenGL compositing manager that use
    GLX_EXT_texture_from_pixmap for binding redirected top-level
    windows to texture objects. It has a flexible plug-in system
    and it is designed to run well on most graphics hardware."""

    homepage = "http://www.compiz.org/"
    url      = "https://www.x.org/archive/individual/app/compiz-0.7.8.tar.gz"

    version('0.7.8', 'e99977d9170a7bd5d571004eed038428')

    # FIXME: add dependencies
    # x11-xcb
    # xcomposite
    # xfixes
    # xdamage
    # xrandr
    # xinerama
    # ice
    # sm
    # libxml-2.0
    # libxslt
    # libstartup-notification-1.0 >= 0.7
    # xrender
    # libpng
    # glib-2.0
    # gconf-2.0

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make('install')
