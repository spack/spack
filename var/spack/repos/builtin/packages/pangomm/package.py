# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pangomm(AutotoolsPackage):
    """Pangomm is a C++ interface to Pango."""

    homepage = "http://www.pango.org/"
    url      = "https://ftp.gnome.org/pub/GNOME/sources/pangomm/2.14/pangomm-2.14.1.tar.gz"

    version('2.14.1', '607a404291d9eeb895f1df3d08f531d7')
    version('2.14.0', '897d8c56cec4a9c297a426eb0fc2af91')

    depends_on('pango')
    depends_on('glibmm')
    depends_on('cairomm')

    def url_for_version(self, version):
        """Handle version-based custom URLs."""
        url = "https://ftp.acc.umu.se/pub/GNOME/sources/pangomm"
        ext = '.tar.gz' if version < Version('2.28.3') else '.tar.xz'
        return url + "/%s/pangomm-%s%s" % (version.up_to(2), version, ext)
