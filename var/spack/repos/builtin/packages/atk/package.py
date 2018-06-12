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


class Atk(MesonPackage):
    """ATK provides the set of accessibility interfaces that are
       implemented by other toolkits and applications. Using the ATK
       interfaces, accessibility tools have full access to view and
       control running applications."""
    homepage = "https://developer.gnome.org/atk/"
    url      = "http://ftp.gnome.org/pub/gnome/sources/atk/2.14/atk-2.14.0.tar.xz"
    list_url = "http://ftp.gnome.org/pub/gnome/sources/atk/"
    list_depth = 2

    version('2.28.1', 'dfb5e7474220afa3f4ca7e45af9f3a11')

    depends_on('glib')
    depends_on('pkgconfig', type='build')
    depends_on('gobject-introspection')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path("XDG_DATA_DIRS",
                               self.prefix.share)
        run_env.prepend_path("XDG_DATA_DIRS",
                             self.prefix.share)
