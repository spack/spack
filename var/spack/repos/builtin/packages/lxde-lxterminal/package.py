# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LxdeLxterminal(AutotoolsPackage):
    """LXDE Terminal Emulator"""

    homepage = "https://wiki.lxde.org/en/LXTerminal"
    url      = "https://downloads.sourceforge.net/project/lxde/LXTerminal%20%28terminal%20emulator%29/LXTerminal%200.2.0/lxterminal-0.2.0.tar.gz"

    version('0.2.0', 'e80ad1b6e26212f3d43908c2ad87ba4d')

    depends_on('libtool', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('binutils', type='build')
    depends_on('intltool', type='build')
    depends_on('perl-xml-parser', type='build')
    depends_on('perl', type='build')
    depends_on('libx11')
    depends_on('gtkplus')
    depends_on('glib')
    depends_on('lxde-menu-cache')
    depends_on('vte')
