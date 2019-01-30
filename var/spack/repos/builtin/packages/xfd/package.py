# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xfd(AutotoolsPackage):
    """xfd - display all the characters in a font using either the
    X11 core protocol or libXft2."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xfd"
    url      = "https://www.x.org/archive/individual/app/xfd-1.1.2.tar.gz"

    version('1.1.2', '12fe8f7c3e71352bf22124ad56d4ceaf')

    depends_on('libxaw')
    depends_on('fontconfig')
    depends_on('libxft')
    depends_on('libxrender')
    depends_on('libxmu')
    depends_on('libxt')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
