# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xmh(AutotoolsPackage):
    """The xmh program provides a graphical user interface to the
    MH Message Handling System.  To actually do things with your
    mail, it makes calls to the MH package."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xmh"
    url      = "https://www.x.org/archive/individual/app/xmh-1.0.3.tar.gz"

    version('1.0.3', '7547c5a5ab7309a1b10e8ecf48e60105')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt')
    depends_on('libx11')

    depends_on('xbitmaps@1.1.0:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
