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


class Xfindproxy(AutotoolsPackage):
    """xfindproxy is used to locate available X11 proxy services.

    It utilizes the Proxy Management Protocol to communicate with a proxy
    manager.  The proxy manager keeps track of all available proxy
    services, starts new proxies when necessary, and makes sure that
    proxies are shared whenever possible."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xfindproxy"
    url      = "https://www.x.org/archive/individual/app/xfindproxy-1.0.4.tar.gz"

    version('1.0.4', 'd0a7b53ae5827b342bccd3ebc7ec672f')

    depends_on('libice')
    depends_on('libxt')

    depends_on('xproto', type='build')
    depends_on('xproxymanagementprotocol', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
