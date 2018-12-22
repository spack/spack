# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xbitmaps(AutotoolsPackage):
    """The xbitmaps package contains bitmap images used by multiple
    applications built in Xorg."""

    homepage = "https://cgit.freedesktop.org/xorg/data/bitmaps/"
    url      = "https://www.x.org/archive/individual/data/xbitmaps-1.1.1.tar.gz"

    version('1.1.1', '288bbe310db67280a9e2e5ebc5602595')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
