# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cups(AutotoolsPackage):
    """CUPS is the standards-based, open source printing system developed by
    Apple Inc. for macOS and other UNIX-like operating systems. CUPS uses the
    Internet Printing Protocol (IPP) to support printing to local and network
    printers. This provides the core CUPS libraries, not a complete CUPS
    install."""

    homepage = "https://www.cups.org/"
    url = "https://github.com/apple/cups/releases/download/v2.2.3/cups-2.2.3-source.tar.gz"

    version('2.2.3', '006a8156680a516e43c59034e31df8bf')

    depends_on('gnutls')

    def configure_args(self):
        args = ['--enable-gnutls', '--with-components=core']
        return args
