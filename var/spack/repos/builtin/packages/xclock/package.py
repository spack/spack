# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xclock(AutotoolsPackage, XorgPackage):
    """xclock is the classic X Window System clock utility.  It displays
    the time in analog or digital form, continuously updated at a
    frequency which may be specified by the user."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xclock"
    xorg_mirror_path = "app/xclock-1.0.7.tar.gz"

    version('1.0.9', sha256='4f0dd4d7d969b55c64f6e58242bca201d19e49eb8c9736dc099330bb0c5385b1')
    version('1.0.8', sha256='bb6f2439e6037759dc1682d80a3fe0232e7b55aa9b38548203e746d290b246bd')
    version('1.0.7', sha256='e730bd575938d5628ef47003a9d4d41b882621798227f5d0c12f4a26365ed1b5')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libx11')
    depends_on('libxrender')
    depends_on('libxft')
    depends_on('libxkbfile')
    depends_on('libxt')

    depends_on('xproto@7.0.17:')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
