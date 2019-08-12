# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxfontcache(AutotoolsPackage):
    """Xfontcache - X-TrueType font cache extension client library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXfontcache"
    url      = "https://www.x.org/archive/individual/lib/libXfontcache-1.0.5.tar.gz"

    version('1.0.5', '5030fc9c7f16dbb52f92a8ba2c574f5c')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xextproto', type='build')
    depends_on('fontcacheproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
