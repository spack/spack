# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xwud(AutotoolsPackage):
    """xwud allows X users to display in a window an image saved in a
    specially formatted dump file, such as produced by xwd."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xwud"
    url      = "https://www.x.org/archive/individual/app/xwud-1.0.4.tar.gz"

    version('1.0.4', 'bb44485a37496f0121e5843bcf5bb01b')

    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
