# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FontMiscEthiopic(Package):
    """X.org misc-ethiopic font."""

    homepage = "http://cgit.freedesktop.org/xorg/font/misc-ethiopic"
    url      = "https://www.x.org/archive/individual/font/font-misc-ethiopic-1.0.3.tar.gz"

    version('1.0.3', '02ddea9338d9d36804ad38f3daadb55a')

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
