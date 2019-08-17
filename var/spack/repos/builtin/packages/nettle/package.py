# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nettle(AutotoolsPackage):
    """The Nettle package contains the low-level cryptographic library
    that is designed to fit easily in many contexts."""

    homepage = "https://www.lysator.liu.se/~nisse/nettle/"
    url      = "https://ftpmirror.gnu.org/nettle/nettle-3.3.tar.gz"

    version('3.4.1', sha256='f941cf1535cd5d1819be5ccae5babef01f6db611f9b5a777bae9c7604b8a92ad')
    version('3.4',   'dc0f13028264992f58e67b4e8915f53d')
    version('3.3',   '10f969f78a463704ae73529978148dbe')
    version('3.2',   'afb15b4764ebf1b4e6d06c62bd4d29e4')
    version('2.7.1', '003d5147911317931dd453520eb234a5')
    version('2.7',   '2caa1bd667c35db71becb93c5d89737f')

    depends_on('gmp')
    depends_on('m4', type='build')

    def configure_args(self):
        return ['CFLAGS={0}'.format(self.compiler.c99_flag)]
