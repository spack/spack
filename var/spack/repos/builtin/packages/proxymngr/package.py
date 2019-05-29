# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
