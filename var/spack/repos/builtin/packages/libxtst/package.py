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


class Libxtst(AutotoolsPackage):
    """libXtst provides the Xlib-based client API for the XTEST & RECORD
    extensions.

    The XTEST extension is a minimal set of client and server extensions
    required to completely test the X11 server with no user intervention.
    This extension is not intended to support general journaling and
    playback of user actions.

    The RECORD extension supports the recording and reporting of all
    core X protocol and arbitrary X extension protocol."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXtst"
    url      = "https://www.x.org/archive/individual/lib/libXtst-1.2.2.tar.gz"

    version('1.2.2', 'efef3b1e44bd8074a601c0c5ce0788f4')

    depends_on('libx11')
    depends_on('libxext@1.0.99.4:')
    depends_on('libxi')

    depends_on('recordproto@1.13.99.1:', type='build')
    depends_on('xextproto@7.0.99.3:', type='build')
    depends_on('inputproto', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
