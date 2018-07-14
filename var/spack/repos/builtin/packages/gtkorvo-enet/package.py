##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class GtkorvoEnet(AutotoolsPackage):
    """ENet reliable UDP networking library.
    This is a downstream branch of lsalzman's ENet.
    This version has expanded the client ID to handle more clients.
    The original is at http://github.com/lsalzman/enet.
    """

    homepage = "http://www.github.com/GTkorvo/enet"
    url = "https://github.com/GTkorvo/enet/archive/v1.3.13.tar.gz"

    version('1.3.14', '05272cac1a8cb0500995eeca310e7fac')
    version('1.3.13', '3490f924a4d421e4832e45850e6ec142')
