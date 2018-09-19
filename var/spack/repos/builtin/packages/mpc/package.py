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
            url = "https://ftp.gnu.org/gnu/mpc/mpc-{0}.tar.gz"

        return url.format(version)

    def configure_args(self):
        spec = self.spec
        return [
            '--with-mpfr={0}'.format(spec['mpfr'].prefix),
            '--with-gmp={0}'.format(spec['gmp'].prefix)
        ]
