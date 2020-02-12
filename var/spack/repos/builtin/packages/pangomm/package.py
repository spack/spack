# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pangomm(AutotoolsPackage):
    """Pangomm is a C++ interface to Pango."""

    homepage = "http://www.pango.org/"
    url      = "https://ftp.gnome.org/pub/GNOME/sources/pangomm/2.14/pangomm-2.14.1.tar.gz"

    version('2.14.1', sha256='2ea6cee273cca1aae2ee5a5dac0c416b4dc354e46debb51f20c6eeba828f5ed5')
    version('2.14.0', sha256='baa3b231c9498fb1140254e3feb4eb93c638f07e6e26ae0e36c3699ec14d80fd')

    depends_on('pango')
    depends_on('glibmm')
    depends_on('cairomm')

    def url_for_version(self, version):
        """Handle version-based custom URLs."""
        url = "https://ftp.acc.umu.se/pub/GNOME/sources/pangomm"
        ext = '.tar.gz' if version < Version('2.28.3') else '.tar.xz'
        return url + "/%s/pangomm-%s%s" % (version.up_to(2), version, ext)
