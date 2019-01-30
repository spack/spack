# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Twm(AutotoolsPackage):
    """twm is a window manager for the X Window System.  It provides
    titlebars, shaped windows, several forms of icon management,
    user-defined macro functions, click-to-type and pointer-driven
    keyboard focus, and user-specified key and pointer button bindings."""

    homepage = "http://cgit.freedesktop.org/xorg/app/twm"
    url      = "https://www.x.org/archive/individual/app/twm-1.0.9.tar.gz"

    version('1.0.9', 'e98fcb32f774ac1ff7bf82101b79f61e')

    depends_on('libx11')
    depends_on('libxext')
    depends_on('libxt')
    depends_on('libxmu')
    depends_on('libice')
    depends_on('libsm')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
