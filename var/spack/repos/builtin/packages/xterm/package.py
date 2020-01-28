# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xterm(AutotoolsPackage):
    """The xterm program is a terminal emulator for the X Window System. It
    provides DEC VT102 and Tektronix 4014 compatible terminals for programs
    that can't use the window system directly."""

    homepage = "http://invisible-island.net/xterm/"
    url      = "ftp://ftp.invisible-island.net/xterm/xterm-327.tgz"

    version('327', sha256='66fb2f6c35b342148f549c276b12a3aa3fb408e27ab6360ddec513e14376150b')

    depends_on('libxft')
    depends_on('fontconfig')
    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt')
    depends_on('libx11')
    depends_on('libxinerama')
    depends_on('libxpm')
    depends_on('libice')
    depends_on('freetype')
    depends_on('libxrender')
    depends_on('libxext')
    depends_on('libsm')
    depends_on('libxcb')
    depends_on('libxau')
    depends_on('bzip2')

    depends_on('pkgconfig', type='build')
