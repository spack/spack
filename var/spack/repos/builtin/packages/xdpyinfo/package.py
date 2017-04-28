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


class Xdpyinfo(AutotoolsPackage):
    """xdpyinfo is a utility for displaying information about an X server.

    It is used to examine the capabilities of a server, the predefined
    values for various parameters used in communicating between clients
    and the server, and the different types of screens, visuals, and X11
    protocol extensions that are available."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xdpyinfo"
    url      = "https://www.x.org/archive/individual/app/xdpyinfo-1.3.2.tar.gz"

    version('1.3.2', 'dab410719d36c9df690cf3a8cd7d117e')

    depends_on('libxext')
    depends_on('libx11')
    depends_on('libxtst')
    depends_on('libxcb')

    depends_on('xproto@7.0.22:', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
