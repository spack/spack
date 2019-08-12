# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fstobdf(AutotoolsPackage):
    """The fstobdf program reads a font from a font server and prints a BDF
    file on the standard output that may be used to recreate the font.
    This is useful in testing servers, debugging font metrics, and
    reproducing lost BDF files."""

    homepage = "http://cgit.freedesktop.org/xorg/app/fstobdf"
    url      = "https://www.x.org/archive/individual/app/fstobdf-1.0.6.tar.gz"

    version('1.0.6', '6d3f24673fcb9ce266f49dc140bbf250')

    depends_on('libx11')
    depends_on('libfs')

    depends_on('xproto@7.0.25:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
