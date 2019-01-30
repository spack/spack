# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bitmap(AutotoolsPackage):
    """bitmap, bmtoa, atobm - X bitmap (XBM) editor and converter utilities."""

    homepage = "http://cgit.freedesktop.org/xorg/app/bitmap"
    url      = "https://www.x.org/archive/individual/app/bitmap-1.0.8.tar.gz"

    version('1.0.8', '0ca600041bb0836ae7c9f5db5ce09091')

    depends_on('libx11')
    depends_on('libxmu')
    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt')

    depends_on('xbitmaps', type='build')
    depends_on('xproto@7.0.25:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
