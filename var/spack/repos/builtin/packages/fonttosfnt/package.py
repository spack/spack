# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fonttosfnt(AutotoolsPackage):
    """Wrap a bitmap font in a sfnt (TrueType) wrapper."""

    homepage = "http://cgit.freedesktop.org/xorg/app/fonttosfnt"
    url      = "https://www.x.org/archive/individual/app/fonttosfnt-1.0.4.tar.gz"

    version('1.0.4', 'ba77fd047a9cca400f17db8c46b06ce8')

    depends_on('freetype')
    depends_on('libfontenc')

    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
