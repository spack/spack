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


class Xfwp(AutotoolsPackage):
    """xfwp proxies X11 protocol connections, such as through a firewall."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xfwp"
    url      = "https://www.x.org/archive/individual/app/xfwp-1.0.3.tar.gz"

    version('1.0.3', 'e23cc01894ae57e5959ca6a56d0f4f94')

    depends_on('libice')

    depends_on('xproto', type='build')
    depends_on('xproxymanagementprotocol', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')

    # FIXME: fails with the error message:
    # io.c:1039:7: error: implicit declaration of function 'swab'
