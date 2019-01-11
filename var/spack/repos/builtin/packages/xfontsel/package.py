# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xfontsel(AutotoolsPackage):
    """xfontsel application provides a simple way to display the X11 core
    protocol fonts known to your X server, examine samples of each, and
    retrieve the X Logical Font Description ("XLFD") full name for a font."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xfontsel"
    url      = "https://www.x.org/archive/individual/app/xfontsel-1.0.5.tar.gz"

    version('1.0.5', '72a35e7fa786eb2b0194d75eeb4a02e3')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt')
    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
