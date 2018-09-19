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


class Applewmproto(AutotoolsPackage):
    """Apple Rootless Window Management Extension.

    This extension defines a protcol that allows X window managers
    to better interact with the Mac OS X Aqua user interface when
    running X11 in a rootless mode."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/applewmproto"
    url      = "https://www.x.org/archive/individual/proto/applewmproto-1.4.2.tar.gz"

    version('1.4.2', 'ecc8a4424a893ce120f5652dba62e9e6')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
