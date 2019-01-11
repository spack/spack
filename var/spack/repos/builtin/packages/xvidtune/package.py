# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xvidtune(AutotoolsPackage):
    """xvidtune is a client interface to the X server video mode
    extension (XFree86-VidModeExtension)."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xvidtune"
    url      = "https://www.x.org/archive/individual/app/xvidtune-1.0.3.tar.gz"

    version('1.0.3', 'e0c31d78741ae4aab2f4bfcc2abd4a3d')

    depends_on('libxxf86vm')
    depends_on('libxt')
    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
