# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxxf86vm(AutotoolsPackage):
    """libXxf86vm - Extension library for the XFree86-VidMode X extension."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXxf86vm"
    url      = "https://www.x.org/archive/individual/lib/libXxf86vm-1.1.4.tar.gz"

    version('1.1.4', '675bd0c521472628d5796602f625ef51')

    depends_on('libx11@1.6:')
    depends_on('libxext')

    depends_on('xproto', type='build')
    depends_on('xextproto', type='build')
    depends_on('xf86vidmodeproto@2.2.99.1:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
