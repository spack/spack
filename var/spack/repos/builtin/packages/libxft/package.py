# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxft(AutotoolsPackage):
    """X FreeType library.

    Xft version 2.1 was the first stand alone release of Xft, a library that
    connects X applications with the FreeType font rasterization library. Xft
    uses fontconfig to locate fonts so it has no configuration files."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXft"
    url      = "https://www.x.org/archive/individual/lib/libXft-2.3.2.tar.gz"

    version('2.3.2', '3a2c1ce2641817dace55cd2bfe10b0f0')

    depends_on('freetype@2.1.6:')
    depends_on('fontconfig@2.5.92:')
    depends_on('libx11')
    depends_on('libxrender@0.8.2:')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
