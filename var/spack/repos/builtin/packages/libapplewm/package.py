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


class Libapplewm(AutotoolsPackage):
    """AppleWM is a simple library designed to interface with the Apple-WM
    extension. This extension allows X window managers to better interact with
    the Mac OS X Aqua user interface when running X11 in a rootless mode."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libAppleWM"
    url      = "https://www.x.org/archive/individual/lib/libAppleWM-1.4.1.tar.gz"

    version('1.4.1', '52c587641eb57f00978d28d98d487af8')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xextproto', type='build')
    depends_on('applewmproto@1.4:', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')

    # Crashes with this error message on Linux:
    # HIServices/Processes.h: No such file or directory
    # May only build properly on macOS?
