# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xinput(AutotoolsPackage):
    """xinput is a utility to configure and test XInput devices."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xinput"
    url      = "https://www.x.org/archive/individual/app/xinput-1.6.2.tar.gz"

    version('1.6.2', '6684f6015298d22936438173be3b7ef5')

    depends_on('libx11')
    depends_on('libxext')
    depends_on('libxi@1.5.99.1:')
    depends_on('libxrandr')
    depends_on('libxinerama')

    depends_on('inputproto@2.1.99.1:', type='build')
    depends_on('fixesproto', type='build')
    depends_on('randrproto', type='build')
    depends_on('xineramaproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
