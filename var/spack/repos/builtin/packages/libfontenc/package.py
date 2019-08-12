# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libfontenc(AutotoolsPackage):
    """libfontenc - font encoding library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libfontenc"
    url      = "https://www.x.org/archive/individual/lib/libfontenc-1.1.3.tar.gz"

    version('1.1.3', '0ffa28542aa7d246299b1f7211cdb768')

    depends_on('zlib')

    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
