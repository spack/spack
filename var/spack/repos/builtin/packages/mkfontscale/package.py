# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mkfontscale(AutotoolsPackage):
    """mkfontscale creates the fonts.scale and fonts.dir index files used by the
    legacy X11 font system."""

    homepage = "http://cgit.freedesktop.org/xorg/app/mkfontscale"
    url      = "https://www.x.org/archive/individual/app/mkfontscale-1.1.2.tar.gz"

    version('1.1.2', 'fab4e1598b8948c124ec7a9f06d30e5b')

    depends_on('libfontenc')
    depends_on('freetype')

    depends_on('xproto@7.0.25:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
