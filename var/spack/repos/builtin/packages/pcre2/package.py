# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pcre2(AutotoolsPackage):
    """The PCRE2 package contains Perl Compatible Regular Expression
       libraries. These are useful for implementing regular expression
       pattern matching using the same syntax and semantics as Perl 5."""

    homepage = "http://www.pcre.org"""
    url      = "https://ftp.pcre.org/pub/pcre/pcre2-10.31.tar.bz2"

    version('10.31', 'e0b91c891a3c49050f7fd15de33d0ba4')
    version('10.20', 'dcd027c57ecfdc8a6c3af9d0acf5e3f7')

    variant('multibyte', default=True,
            description='Enable support for 16 and 32 bit characters.')

    def configure_args(self):
        args = []

        if '+multibyte' in self.spec:
            args.append('--enable-pcre2-16')
            args.append('--enable-pcre2-32')

        return args
