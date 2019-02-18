# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FontXfree86Type1(Package):
    """X.org xfree86-type1 font."""

    homepage = "http://cgit.freedesktop.org/xorg/font/xfree86-type1"
    url      = "https://www.x.org/archive/individual/font/font-xfree86-type1-1.0.4.tar.gz"

    version('1.0.4', '89c33c5176cd580de6636ad50ce7777b')

    depends_on('font-util')

    depends_on('fontconfig', type='build')
    depends_on('mkfontdir', type='build')
    depends_on('mkfontscale', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix))

        make('install')

        # `make install` copies the files to the font-util installation.
        # Create a fake directory to convince Spack that we actually
        # installed something.
        mkdir(prefix.lib)
