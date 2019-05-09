# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mpc(AutotoolsPackage):
    """Gnu Mpc is a C library for the arithmetic of complex numbers
       with arbitrarily high precision and correct rounding of the
       result."""

    homepage = "http://www.multiprecision.org"
    url      = "https://ftpmirror.gnu.org/mpc/mpc-1.1.0.tar.gz"
    list_url = "http://www.multiprecision.org/mpc/download.html"

    version('1.1.0', '4125404e41e482ec68282a2e687f6c73')
    version('1.0.3', 'd6a1d5f8ddea3abd2cc3e98f58352d26')
    version('1.0.2', '68fadff3358fb3e7976c7a398a0af4c3')

    # Could also be built against mpir instead
    depends_on('gmp@4.3.2:')
    depends_on('gmp@5.0.0:', when='@1.1.0:')
    depends_on('mpfr@2.4.2:')
    depends_on('mpfr@3.0.0:', when='@1.1.0:')

    def url_for_version(self, version):
        if version < Version("1.0.1"):
            url = "http://www.multiprecision.org/mpc/download/mpc-{0}.tar.gz"
        else:
            url = "https://ftpmirror.gnu.org/mpc/mpc-{0}.tar.gz"

        return url.format(version)

    def configure_args(self):
        spec = self.spec
        return [
            '--with-mpfr={0}'.format(spec['mpfr'].prefix),
            '--with-gmp={0}'.format(spec['gmp'].prefix)
        ]
