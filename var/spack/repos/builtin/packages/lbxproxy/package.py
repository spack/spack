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


class Lbxproxy(AutotoolsPackage):
    """lbxproxy accepts client connections, multiplexes them over a single
    connection to the X server, and performs various optimizations on the
    X protocol to make it faster over low bandwidth and/or high latency
    connections.

    Note that the X server source from X.Org no longer supports the LBX
    extension, so this program is only useful in connecting to older
    X servers."""

    homepage = "http://cgit.freedesktop.org/xorg/app/lbxproxy"
    url      = "https://www.x.org/archive/individual/app/lbxproxy-1.0.3.tar.gz"

    version('1.0.3', '50a2a1ae15e8edf7582f76bcdf6b8197')

    depends_on('libxext')
    depends_on('liblbxutil')
    depends_on('libx11')
    depends_on('libice')

    depends_on('xtrans', type='build')
    depends_on('xproxymanagementprotocol', type='build')
    depends_on('bigreqsproto', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
