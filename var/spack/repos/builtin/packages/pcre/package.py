# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pcre(AutotoolsPackage):
    """The PCRE package contains Perl Compatible Regular Expression
    libraries. These are useful for implementing regular expression
    pattern matching using the same syntax and semantics as Perl 5."""

    homepage = "http://www.pcre.org"
    url      = "https://ftp.pcre.org/pub/pcre/pcre-8.42.tar.bz2"

    version('8.42', '085b6aa253e0f91cae70b3cdbe8c1ac2')
    version('8.41', 'c160d22723b1670447341b08c58981c1')
    version('8.40', '41a842bf7dcecd6634219336e2167d1d')
    version('8.39', 'e3fca7650a0556a2647821679d81f585')
    version('8.38', '00aabbfe56d5a48b270f999b508c5ad2')

    patch('intel.patch', when='@8.38')

    variant('jit', default=False,
            description='Enable JIT support.')

    variant('utf', default=True,
            description='Enable support for UTF-8/16/32, '
            'incompatible with EBCDIC.')

    def configure_args(self):
        args = []

        if '+jit' in self.spec:
            args.append('--enable-jit')

        if '+utf' in self.spec:
            args.append('--enable-utf')
            args.append('--enable-unicode-properties')

        return args
