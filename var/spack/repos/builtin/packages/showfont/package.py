# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Showfont(AutotoolsPackage):
    """showfont displays data about a font from an X font server.
    The information shown includes font information, font properties,
    character metrics, and character bitmaps."""

    homepage = "http://cgit.freedesktop.org/xorg/app/showfont"
    url      = "https://www.x.org/archive/individual/app/showfont-1.0.5.tar.gz"

    version('1.0.5', 'cea973363df01fb27a87e939600137fd')

    depends_on('libfs')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
