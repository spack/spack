# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
