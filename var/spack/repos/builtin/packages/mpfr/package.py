# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mpfr(AutotoolsPackage):
    """The MPFR library is a C library for multiple-precision
       floating-point computations with correct rounding."""

    homepage = "https://www.mpfr.org/"
    url      = "https://ftpmirror.gnu.org/mpfr/mpfr-4.0.2.tar.bz2"

    version('4.0.2', sha256='c05e3f02d09e0e9019384cdd58e0f19c64e6db1fd6f5ecf77b4b1c61ca253acc')
    version('4.0.1', '8c21d8ac7460493b2b9f3ef3cc610454')
    version('4.0.0', 'ef619f3bb68039e35c4a219e06be72d0')
    version('3.1.6', '320c28198def956aeacdb240b46b8969')
    version('3.1.5', 'b1d23a55588e3b2a13e3be66bc69fd8d')
    version('3.1.4', 'b8a2f6b0e68bef46e53da2ac439e1cf4')
    version('3.1.3', '5fdfa3cfa5c86514ee4a241a1affa138')
    version('3.1.2', 'ee2c3ac63bf0c2359bf08fc3ee094c19')

    # mpir is a drop-in replacement for gmp
    depends_on('gmp@4.1:')  # 4.2.3 or higher is recommended
    depends_on('gmp@5.0:', when='@4.0.0:')  # https://www.mpfr.org/mpfr-4.0.0/

    # Check the Bugs section of old release pages for patches.
    # https://www.mpfr.org/mpfr-X.Y.Z/#bugs
    patches = {
        '4.0.2': 'f2d2a530acb5e70e1a9d5b80881dbb4a504d56535c4bc103d83e0bb630172029',
        '4.0.1': '5230aab653fa8675fc05b5bdd3890e071e8df49a92a9d58c4284024affd27739',
        '3.1.6': '66a5d58364113a21405fc53f4a48f4e8',
        '3.1.5': '1dc5fe65feb5607b89fe0f410d53b627',
        '3.1.4': 'd124381573404fe83654c7d5a79aeabf',
        '3.1.3': 'ebd1d835e0ae2fd8a9339210ccd1d0a8',
        '3.1.2': '9f96a5c7cac1d6cd983ed9cf7d997074',
    }

    for ver, checksum in patches.items():
        patch('https://www.mpfr.org/mpfr-{0}/allpatches'.format(ver),
              when='@' + ver, sha256=checksum)

    def flag_handler(self, name, flags):
        # Work around macOS Catalina / Xcode 11 code generation bug
        # (test failure t-toom53, due to wrong code in mpn/toom53_mul.o)
        if self.spec.satisfies('os=catalina') and name == 'cflags':
            flags.append('-fno-stack-check')
        return (flags, None, None)

    def configure_args(self):
        args = [
            '--with-gmp=' + self.spec['gmp'].prefix,
        ]
        return args
