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
