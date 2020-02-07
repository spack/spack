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
    url      = "https://github.com/ThomasDickey/xterm-snapshots/archive/xterm-353.tar.gz"

    version('353', sha256='f5859a0e07a958576f78866aa32a59d66c34b4bd8f1894d0d1db30733d4380b1')
    version('350', sha256='382ee3c321fbec18eeecb7772ec0485d4cb9fba7968cbe2f7c82dc9d2f2e93c8')
    version('340', sha256='7488deeecdae7275a064518fae202179af5fc97916c2ea36a8132927b51441c6')
    version('330', sha256='e9845fc91330bdedefbe4f427b095d7854f679274f43b3d342da9e4029aab244')
    version('327', sha256='3bc81be814f612095a4c16a01db89fcfc8cce410a04ae567090a70efa829c726')

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
