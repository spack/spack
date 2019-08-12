# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class AtSpi2Atk(MesonPackage):
    """The At-Spi2 Atk package contains a library that bridges ATK to
       At-Spi2 D-Bus service."""

    homepage = "http://www.linuxfromscratch.org/blfs/view/cvs/x/at-spi2-atk.html"
    url      = "http://ftp.gnome.org/pub/gnome/sources/at-spi2-atk/2.26/at-spi2-atk-2.26.1.tar.xz"
    list_url = "http://ftp.gnome.org/pub/gnome/sources/at-spi2-atk"
    list_depth = 1

    version('2.26.2', '355c7916a69513490cb83ad34016b169')
    version('2.26.1', 'eeec6cead3350dca48a235271c105b3e')

    depends_on('pkgconfig', type='build')
    depends_on('at-spi2-core@2.28.0:')
    depends_on('atk@2.28.1:')

    def url_for_version(self, version):
        """Handle gnome's version-based custom URLs."""
        url = 'http://ftp.gnome.org/pub/gnome/sources/at-spi2-atk'
        return url + '/%s/at-spi2-atk-%s.tar.xz' % (version.up_to(2), version)
