# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FontBh75dpi(Package):
    """X.org bh-75dpi font."""

    homepage = "http://cgit.freedesktop.org/xorg/font/bh-75dpi"
    url      = "https://www.x.org/archive/individual/font/font-bh-75dpi-1.0.3.tar.gz"

    version('1.0.3', '88fec4ebc4a265684bff3abdd066f14f')

    depends_on('font-util')

    depends_on('fontconfig', type='build')
    depends_on('mkfontdir', type='build')
    depends_on('bdftopcf', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix))

        make()
        make('install')

        # `make install` copies the files to the font-util installation.
        # Create a fake directory to convince Spack that we actually
        # installed something.
        mkdir(prefix.lib)
