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


class Proxymngr(AutotoolsPackage):
    """The proxy manager (proxymngr) is responsible for resolving requests from
    xfindproxy (and other similar clients), starting new proxies when
    appropriate, and keeping track of all of the available proxy services.
    The proxy manager strives to reuse existing proxies whenever possible."""

    homepage = "http://cgit.freedesktop.org/xorg/app/proxymngr"
    url      = "https://www.x.org/archive/individual/app/proxymngr-1.0.4.tar.gz"

    version('1.0.4', 'a165cf704f6a413f0bacf65ea470331f')

    depends_on('libice')
    depends_on('libxt')
    depends_on('lbxproxy')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('xproxymanagementprotocol', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
