# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class I3(AutotoolsPackage):
    """i3, improved tiling wm. i3 is a tiling window manager, completely
    written from scratch. The target platforms are GNU/Linux and BSD operating
    systems, our code is Free and Open Source Software (FOSS) under the BSD
    license. i3 is primarily targeted at advanced users and developers."""

    homepage = "https://i3wm.org/"
    url      = "https://github.com/i3/i3/archive/4.14.1.tar.gz"

    version('4.14.1', 'bdbb6d7bb5a647c8b7b53ed10de84cc5')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('pkgconfig', type='build')

    depends_on('libev')
    depends_on('startup-notification')
    depends_on('xcb-util-cursor')
    depends_on('xcb-util-keysyms')
    depends_on('xcb-util-wm')
    depends_on('xcb-util-xrm')
    depends_on('libxkbcommon')
    depends_on('yajl')
    depends_on('cairo+X')
    depends_on('pango+X')
