# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xconsole(AutotoolsPackage):
    """xconsole displays in a X11 window the messages which are usually sent
    to /dev/console."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xconsole"
    url      = "https://www.x.org/archive/individual/app/xconsole-1.0.6.tar.gz"

    version('1.0.6', '46cb988e31a0cf9a02c2bbc4a82bd572')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt@1.0:')
    depends_on('libx11')

    depends_on('xproto@7.0.17:')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
