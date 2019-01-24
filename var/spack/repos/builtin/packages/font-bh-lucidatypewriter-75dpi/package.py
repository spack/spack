# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FontBhLucidatypewriter75dpi(Package):
    """X.org bh-lucidatypewriter-75dpi font."""

    homepage = "http://cgit.freedesktop.org/xorg/font/bh-lucidatypewriter-75dpi"
    url      = "https://www.x.org/archive/individual/font/font-bh-lucidatypewriter-75dpi-1.0.3.tar.gz"

    version('1.0.3', 'cab8a44ae329aab7141c7adeef0daf5a')

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
