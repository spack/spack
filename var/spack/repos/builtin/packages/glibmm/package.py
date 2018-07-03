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
