# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Encodings(Package):
    """X.org encodings font."""

    homepage = "http://cgit.freedesktop.org/xorg/font/encodings"
    url      = "https://www.x.org/archive/individual/font/encodings-1.0.4.tar.gz"

    version('1.0.4', '1a631784ce204d667abcc329b851670c')

    depends_on('font-util')

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
