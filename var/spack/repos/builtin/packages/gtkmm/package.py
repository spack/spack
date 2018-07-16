##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
