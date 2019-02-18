# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FontAdobeUtopiaType1(Package):
    """X.org adobe-utopia-type1 font."""

    homepage = "https://cgit.freedesktop.org/xorg/font/adobe-utopia-type1"
    url      = "https://www.x.org/archive/individual/font/font-adobe-utopia-type1-1.0.4.tar.gz"

    version('1.0.4', 'b0676c3495acabad519ee98a94163904')

    depends_on('font-util', type='build')
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
