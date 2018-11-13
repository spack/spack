# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxxf86misc(AutotoolsPackage):
    """libXxf86misc - Extension library for the XFree86-Misc X extension."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXxf86misc"
    url      = "https://www.x.org/archive/individual/lib/libXxf86misc-1.0.3.tar.gz"

    version('1.0.3', 'c8d8743e146bcd2aa9856117ac5ef6c0')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xproto', type='build')
    depends_on('xextproto', type='build')
    depends_on('xf86miscproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
