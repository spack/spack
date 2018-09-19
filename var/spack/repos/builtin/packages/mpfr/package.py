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


class Mpfr(AutotoolsPackage):
    """The MPFR library is a C library for multiple-precision
       floating-point computations with correct rounding."""

    homepage = "http://www.mpfr.org"
    url      = "https://ftpmirror.gnu.org/mpfr/mpfr-4.0.1.tar.bz2"

    version('4.0.1', '8c21d8ac7460493b2b9f3ef3cc610454')
    version('4.0.0', 'ef619f3bb68039e35c4a219e06be72d0')
    version('3.1.6', '320c28198def956aeacdb240b46b8969')
    version('3.1.5', 'b1d23a55588e3b2a13e3be66bc69fd8d')
    version('3.1.4', 'b8a2f6b0e68bef46e53da2ac439e1cf4')
    version('3.1.3', '5fdfa3cfa5c86514ee4a241a1affa138')
    version('3.1.2', 'ee2c3ac63bf0c2359bf08fc3ee094c19')

    # mpir is a drop-in replacement for gmp
    depends_on('gmp@4.1:')  # 4.2.3 or higher is recommended
    depends_on('gmp@5.0:', when='@4.0.0:')  # http://www.mpfr.org/mpfr-4.0.0/

    # Check the Bugs section of old release pages for patches.
    # http://www.mpfr.org/mpfr-X.Y.Z/#bugs
    patches = {
        '3.1.6': '66a5d58364113a21405fc53f4a48f4e8',
        '3.1.5': '1dc5fe65feb5607b89fe0f410d53b627',
        '3.1.4': 'd124381573404fe83654c7d5a79aeabf',
        '3.1.3': 'ebd1d835e0ae2fd8a9339210ccd1d0a8',
        '3.1.2': '9f96a5c7cac1d6cd983ed9cf7d997074',
    }

    for ver, checksum in patches.items():
        patch('http://www.mpfr.org/mpfr-{0}/allpatches'.format(ver),
              when='@' + ver, sha256=checksum)

    def configure_args(self):
        args = [
            '--with-gmp=' + self.spec['gmp'].prefix,
        ]
        return args
