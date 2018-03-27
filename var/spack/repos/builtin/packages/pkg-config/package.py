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


class PkgConfig(AutotoolsPackage):
    """pkg-config is a helper tool used when compiling applications
    and libraries"""

    homepage = "http://www.freedesktop.org/wiki/Software/pkg-config/"
    url = "http://pkgconfig.freedesktop.org/releases/pkg-config-0.29.2.tar.gz"

    version('0.29.2', 'f6e931e319531b736fadc017f470e68a')
    version('0.29.1', 'f739a28cae4e0ca291f82d1d41ef107d')
    version('0.28',   'aa3c86e67551adc3ac865160e34a2a0d')

    provides('pkgconfig')

    variant('internal_glib', default=True,
            description='Builds with internal glib')

    # The following patch is needed for gcc-6.1
    patch('g_date_strftime.patch', when='@:0.29.1')

    parallel = False

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """Adds the ACLOCAL path for autotools."""
        spack_env.append_path('ACLOCAL_PATH',
                              join_path(self.prefix.share, 'aclocal'))

    def configure_args(self):
        config_args = ['--enable-shared']

        if '+internal_glib' in self.spec:
            # There's a bootstrapping problem here;
            # glib uses pkg-config as well, so break
            # the cycle by using the internal glib.
            config_args.append('--with-internal-glib')

        return config_args
