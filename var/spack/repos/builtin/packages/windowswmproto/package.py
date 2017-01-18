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


class Windowswmproto(AutotoolsPackage):
    """This module provides the definition of the WindowsWM extension to the
    X11 protocol, used for coordination between an X11 server and the
    Microsoft Windows native window manager.

    WindowsWM is only intended to be used on Cygwin when running a
    rootless XWin server."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/windowswmproto"
    url      = "https://www.x.org/archive/individual/proto/windowswmproto-1.0.4.tar.gz"

    version('1.0.4', '558db92a8e4e1b07e9c62eca3f04dd8d')
