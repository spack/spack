# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxinerama(AutotoolsPackage):
    """libXinerama - API for Xinerama extension to X11 Protocol."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXinerama"
    url      = "https://www.x.org/archive/individual/lib/libXinerama-1.1.3.tar.gz"

    version('1.1.3', '7224a1baa9733a54053550a3fb4be118')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xextproto', type='build')
    depends_on('xineramaproto@1.1.99.1:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
