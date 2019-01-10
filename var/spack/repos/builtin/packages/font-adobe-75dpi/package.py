# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FontAdobe75dpi(AutotoolsPackage):
    """X.org adobe-75dpi font."""

    homepage = "http://cgit.freedesktop.org/xorg/font/adobe-75dpi"
    url      = "https://www.x.org/archive/individual/font/font-adobe-75dpi-1.0.3.tar.gz"

    version('1.0.3', '7a414bb661949cec938938fd678cf649')

    depends_on('font-util')

    depends_on('fontconfig', type='build')
    depends_on('mkfontdir', type='build')
    depends_on('bdftopcf', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    def install(self, spec, prefix):
        make('install')

        # `make install` copies the files to the font-util installation.
        # Create a fake directory to convince Spack that we actually
        # installed something.
        mkdir(prefix.lib)
