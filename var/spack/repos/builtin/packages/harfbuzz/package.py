# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Harfbuzz(AutotoolsPackage):
    """The Harfbuzz package contains an OpenType text shaping engine."""
    homepage = "http://www.freedesktop.org/wiki/Software/HarfBuzz/"
    url      = "http://www.freedesktop.org/software/harfbuzz/release/harfbuzz-0.9.37.tar.bz2"

    version('1.4.6', '21a78b81cd20cbffdb04b59ac7edfb410e42141869f637ae1d6778e74928d293')
    version('0.9.37', 'bfe733250e34629a188d82e3b971bc1e')

    depends_on("pkgconfig", type="build")
    depends_on("glib")
    depends_on("icu4c")
    depends_on("freetype")
    depends_on("cairo")
    depends_on("zlib")

    def patch(self):
        change_sed_delimiter('@', ';', 'src/Makefile.in')
