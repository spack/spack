# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxcursor(AutotoolsPackage):
    """libXcursor - X Window System Cursor management library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXcursor"
    url      = "https://www.x.org/archive/individual/lib/libXcursor-1.1.14.tar.gz"

    version('1.1.14', '39c8423de190d64f1c52fbc00022e52c')

    depends_on('libxrender@0.8.2:')
    depends_on('libxfixes')
    depends_on('libx11')

    depends_on('fixesproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
