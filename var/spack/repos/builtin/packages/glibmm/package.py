# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Glibmm(AutotoolsPackage):
    """Glibmm is a C++ wrapper for the glib library."""

    homepage = "https://developer.gnome.org/glib/"
    url      = "https://ftp.gnome.org/pub/GNOME/sources/glibmm/2.19/glibmm-2.19.3.tar.gz"

    version('2.19.3', 'b50180bb93f501172a2ac4c54e83e88a')
    version('2.16.0', '24390d2da1734205f1e572f24d4942f0')
    version('2.4.8', 'fa8b2889cd845752446c6ce15a94bb32')

    depends_on('libsigcpp')
    depends_on('glib')

    patch('guint16_cast.patch', when='@2.19.3')

    def url_for_version(self, version):
        """Handle glibmm's version-based custom URLs."""
        url = "https://ftp.acc.umu.se/pub/GNOME/sources/glibmm"
        ext = '.tar.gz' if version < Version('2.28.2') else '.tar.xz'
        return url + "/%s/glibmm-%s%s" % (version.up_to(2), version, ext)
