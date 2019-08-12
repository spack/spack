# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
