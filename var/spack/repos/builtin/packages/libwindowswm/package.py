# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libwindowswm(AutotoolsPackage):
    """WindowsWM - Cygwin/X rootless window management extension.

    WindowsWM is a simple library designed to interface with the
    Windows-WM extension.  This extension allows X window managers to
    better interact with the Cygwin XWin server when running X11 in a
    rootless mode."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libWindowsWM"
    url      = "https://www.x.org/archive/individual/lib/libWindowsWM-1.0.1.tar.gz"

    version('1.0.1', 'f260e124706ff6209c566689528667c6')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xextproto', type='build')
    depends_on('windowswmproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
