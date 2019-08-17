# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rstart(AutotoolsPackage):
    """This package includes both the client and server sides implementing
    the protocol described in the "A Flexible Remote Execution Protocol
    Based on rsh" paper found in the specs/ subdirectory.

    This software has been deprecated in favor of the X11 forwarding
    provided in common ssh implementations."""

    homepage = "http://cgit.freedesktop.org/xorg/app/rstart"
    url      = "https://www.x.org/archive/individual/app/rstart-1.0.5.tar.gz"

    version('1.0.5', '32db3625cb5e841e17d6bc696f21edfb')

    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
