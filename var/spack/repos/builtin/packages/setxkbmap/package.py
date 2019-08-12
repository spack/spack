# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Setxkbmap(AutotoolsPackage):
    """setxkbmap is an X11 client to change the keymaps in the X server for a
    specified keyboard to use the layout determined by the options listed
    on the command line."""

    homepage = "http://cgit.freedesktop.org/xorg/app/setxkbmap"
    url      = "https://www.x.org/archive/individual/app/setxkbmap-1.3.1.tar.gz"

    version('1.3.1', 'fdfc0fc643a50fb0b5fa7546e4d28868')

    depends_on('libxkbfile')
    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
