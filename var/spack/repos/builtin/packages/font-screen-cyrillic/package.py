# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FontScreenCyrillic(Package):
    """X.org screen-cyrillic font."""

    homepage = "http://cgit.freedesktop.org/xorg/font/screen-cyrillic"
    url      = "https://www.x.org/archive/individual/font/font-screen-cyrillic-1.0.4.tar.gz"

    version('1.0.4', '4cadaf2ba4c4d0f4cb9b4e7b8f0a3019')

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
