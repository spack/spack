# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xrx(AutotoolsPackage):
    """The remote execution (RX) service specifies a MIME format for invoking
    applications remotely, for example via a World Wide Web browser.  This
    RX format specifies a syntax for listing network services required by
    the application, for example an X display server.  The requesting Web
    browser must identify specific instances of the services in the request
    to invoke the application."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xrx"
    url      = "https://www.x.org/archive/individual/app/xrx-1.0.4.tar.gz"

    version('1.0.4', 'dd4b8bf6eca5fc5be5df30c14050074c')

    depends_on('libx11')
    depends_on('libxt')
    depends_on('libxext')
    depends_on('libxau')
    depends_on('libice')
    depends_on('libxaw')

    depends_on('xtrans', type='build')
    depends_on('xproxymanagementprotocol', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
