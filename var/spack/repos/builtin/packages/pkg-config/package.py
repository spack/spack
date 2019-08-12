# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
