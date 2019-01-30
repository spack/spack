# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xcalc(AutotoolsPackage):
    """xcalc is a scientific calculator X11 client that can emulate a TI-30
    or an HP-10C."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xcalc"
    url      = "https://www.x.org/archive/individual/app/xcalc-1.0.6.tar.gz"

    version('1.0.6', 'a192ebb5e5f33925c71713501173d8e0')

    depends_on('libxaw')
    depends_on('libxt')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
