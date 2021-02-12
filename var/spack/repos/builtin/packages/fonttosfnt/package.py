# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fonttosfnt(AutotoolsPackage, XorgPackage):
    """Wrap a bitmap font in a sfnt (TrueType) wrapper."""

    homepage = "http://cgit.freedesktop.org/xorg/app/fonttosfnt"
    xorg_mirror_path = "app/fonttosfnt-1.0.4.tar.gz"

    version('1.2.1', sha256='208efbf4f8edc3eb8818b3c537d327bb48afc3853d7bcec48075716af7a51f3d')
    version('1.2.0', sha256='6508c68fd2b7fadff33ada019448ba3509e49076ce5214ffef2192a075a83d9c')
    version('1.1.0', sha256='a83261120dd0742166fc93a610b254daa6db764ed35a7b96f4a8f96dc9a94792')
    version('1.0.5', sha256='f9230158531875625fddfff597d6325a43be131a3227f5253531633970dd20e4')
    version('1.0.4', sha256='3873636be5b3b8e4160070e8f9a7a9221b5bd5efbf740d7abaa9092e10732673')

    depends_on('freetype')
    depends_on('libfontenc')

    depends_on('xproto')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
