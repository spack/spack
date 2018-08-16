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


class AtSpi2Atk(MesonPackage):
    """The At-Spi2 Atk package contains a library that bridges ATK to
       At-Spi2 D-Bus service."""

    homepage = "http://www.linuxfromscratch.org/blfs/view/cvs/x/at-spi2-atk.html"
    url      = "http://ftp.gnome.org/pub/gnome/sources/at-spi2-atk/2.26/at-spi2-atk-2.26.1.tar.xz"
    list_url = "http://ftp.gnome.org/pub/gnome/sources/at-spi2-atk"
    list_depth = 1

    version('2.26.2', '355c7916a69513490cb83ad34016b169')
    version('2.26.1', 'eeec6cead3350dca48a235271c105b3e')

    depends_on('at-spi2-core@2.28.0:')
    depends_on('atk@2.28.1:')

    def url_for_version(self, version):
        """Handle gnome's version-based custom URLs."""
        url = 'http://ftp.gnome.org/pub/gnome/sources/at-spi2-atk'
        return url + '/%s/at-spi2-atk-%s.tar.xz' % (version.up_to(2), version)
