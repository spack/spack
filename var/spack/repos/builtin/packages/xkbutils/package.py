# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xkbutils(AutotoolsPackage):
    """xkbutils is a collection of small utilities utilizing the XKeyboard
    (XKB) extension to the X11 protocol."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xkbutils"
    url      = "https://www.x.org/archive/individual/app/xkbutils-1.0.4.tar.gz"

    version('1.0.4', '6b898346b84e07c2f13b097193ca0413')

    depends_on('libxaw')
    depends_on('libxt')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('inputproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
