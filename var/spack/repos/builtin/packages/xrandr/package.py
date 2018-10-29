# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xrandr(AutotoolsPackage):
    """xrandr - primitive command line interface to X11 Resize, Rotate, and
    Reflect (RandR) extension."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xrandr"
    url      = "https://www.x.org/archive/individual/app/xrandr-1.5.0.tar.gz"

    version('1.5.0', 'fe9cf76033fe5d973131eac67b6a3118')

    depends_on('libxrandr@1.5:')
    depends_on('libxrender')
    depends_on('libx11')
    depends_on('randrproto')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
