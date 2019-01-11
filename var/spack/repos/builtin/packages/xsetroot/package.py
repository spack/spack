# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xsetroot(AutotoolsPackage):
    """xsetroot - root window parameter setting utility for X."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xsetroot"
    url      = "https://www.x.org/archive/individual/app/xsetroot-1.1.1.tar.gz"

    version('1.1.1', '8c794914a2d0456317288c41451dbee3')

    depends_on('libxmu')
    depends_on('libx11')
    depends_on('libxcursor')

    depends_on('xbitmaps', type='build')
    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
