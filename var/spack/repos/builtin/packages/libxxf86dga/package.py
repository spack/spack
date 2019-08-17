# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxxf86dga(AutotoolsPackage):
    """libXxf86dga - Client library for the XFree86-DGA extension."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXxf86dga"
    url      = "https://www.x.org/archive/individual/lib/libXxf86dga-1.1.4.tar.gz"

    version('1.1.4', '8ed1c8674e730e8d333dfe4b9f2097d9')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xproto', type='build')
    depends_on('xextproto', type='build')
    depends_on('xf86dgaproto@2.0.99.2:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
