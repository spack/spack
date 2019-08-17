# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gtkmm(AutotoolsPackage):
    """Gtkmm is the official C++ interface for the popular GUI library GTK+."""

    homepage = "https://www.gtkmm.org/en/"
    url      = "https://ftp.acc.umu.se/pub/GNOME/sources/gtkmm/2.16/gtkmm-2.16.0.tar.gz"

    version('2.19.7', '2afc018e5b15cde293cd2d21db9b6a55')
    version('2.19.6', 'fb140e82e583620defe0d70bfe7eefd7')
    version('2.19.4', '60006a23306487938dfe0e4b17e3fa46')
    version('2.19.2', 'dc208575a24e8d5265af2fd59c08f3d8')
    version('2.17.11', '2326ff83439aac83721ed4694acf14e5')
    version('2.17.1', '19358644e5e620ad738658be2cb6d739')
    version('2.16.0', 'de178c2a6f23eda0b6a8bfb0219e2e1c')
    version('2.4.11', 'a339958bc4ab7f74201b312bd3562d46')

    depends_on('glibmm')
    depends_on('atk')
    depends_on('gtkplus')
    depends_on('pangomm')
    depends_on('cairomm')

    def url_for_version(self, version):
        """Handle glib's version-based custom URLs."""
        url = "https://ftp.acc.umu.se/pub/GNOME/sources/gtkmm"
        ext = '.tar.gz' if version < Version('3.1.0') else '.tar.xz'
        return url + "/%s/gtkmm-%s%s" % (version.up_to(2), version, ext)
