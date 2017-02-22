##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Atk(AutotoolsPackage):
    """ATK provides the set of accessibility interfaces that are
       implemented by other toolkits and applications. Using the ATK
       interfaces, accessibility tools have full access to view and
       control running applications."""
    homepage = "https://developer.gnome.org/atk/"
    url      = "http://ftp.gnome.org/pub/gnome/sources/atk/2.14/atk-2.14.0.tar.xz"

    version('2.20.0', '5187b0972f4d3905f285540b31395e20')
    version('2.14.0', 'ecb7ca8469a5650581b1227d78051b8b')

    depends_on('glib')
    depends_on('pkg-config', type='build')
    depends_on('gobject-introspection')

    def url_for_version(self, version):
        """Handle atk's version-based custom URLs."""
        url = 'http://ftp.gnome.org/pub/gnome/sources/atk'
        return url + '/%s/atk-%s.tar.xz' % (version.up_to(2), version)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path("XDG_DATA_DIRS", join_path(self.prefix, 'share'))
