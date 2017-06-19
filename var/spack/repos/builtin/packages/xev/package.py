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


class Xev(AutotoolsPackage):
    """xev creates a window and then asks the X server to send it X11 events
    whenever anything happens to the window (such as it being moved,
    resized, typed in, clicked in, etc.).  You can also attach it to an
    existing window.  It is useful for seeing what causes events to occur
    and to display the information that they contain; it is essentially a
    debugging and development tool, and should not be needed in normal
    usage."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xev"
    url      = "https://www.x.org/archive/individual/app/xev-1.2.2.tar.gz"

    version('1.2.2', 'fdb374f77cdad8e104b989a0148c4c1f')

    depends_on('libxrandr@1.2:')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
