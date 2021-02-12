# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dos2unix(MakefilePackage):
    """DOS/Mac to Unix and vice versa text file format converter."""

    homepage = "https://waterlan.home.xs4all.nl/dos2unix.html"
    url      = "https://waterlan.home.xs4all.nl/dos2unix/dos2unix-7.3.4.tar.gz"

    version('7.4.2', sha256='6035c58df6ea2832e868b599dfa0d60ad41ca3ecc8aa27822c4b7a9789d3ae01')
    version('7.4.1', sha256='1cd58a60b03ed28fa39046102a185c5e88c4f7665e1e0417c25de7f8b9f78623')
    version('7.4.0', sha256='bac765abdbd95cdd87a71989d4382c32cf3cbfeee2153f0086cb9cf18261048a')
    version('7.3.5', sha256='a72caa2fb5cb739403315472fe522eda41aabab2a02ad6f5589639330af262e5')
    version('7.3.4', sha256='8ccda7bbc5a2f903dafd95900abb5bf5e77a769b572ef25150fde4056c5f30c5')

    depends_on('gettext', type='build')

    def install(self, spec, prefix):
        make('prefix={0}'.format(prefix), 'install')
