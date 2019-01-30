# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xkbprint(AutotoolsPackage):
    """xkbprint generates a printable or encapsulated PostScript description
    of an XKB keyboard description."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xkbprint"
    url      = "https://www.x.org/archive/individual/app/xkbprint-1.0.4.tar.gz"

    version('1.0.4', '4dd9d4fdbdc08f70dc402da149e4d5d8')

    depends_on('libxkbfile')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
