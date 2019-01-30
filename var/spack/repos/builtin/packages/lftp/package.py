# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lftp(AutotoolsPackage):
    """LFTP is a sophisticated file transfer program supporting a number
       of network protocols (ftp, http, sftp, fish, torrent)."""

    homepage = "http://lftp.yar.ru/"
    url      = "http://lftp.yar.ru/ftp/lftp-4.7.7.tar.gz"

    version('4.8.1', '419b27c016d968a0226b2e5df1454c22')
    version('4.7.7', 'ddc71b3b11a1af465e829075ae14b3ff')
    version('4.6.4', 'f84ecfc368b7afcc56fe7d3da2457d12')

    depends_on('expat')
    depends_on('libiconv')
    depends_on('ncurses')
    depends_on('openssl')
    depends_on('readline')
    depends_on('zlib')

    def configure_args(self):
        return [
            '--with-expat={0}'.format(self.spec['expat'].prefix),
            '--with-libiconv={0}'.format(self.spec['libiconv'].prefix),
            '--with-openssl={0}'.format(self.spec['openssl'].prefix),
            '--with-readline={0}'.format(self.spec['readline'].prefix),
            '--with-zlib={0}'.format(self.spec['zlib'].prefix),
            '--disable-dependency-tracking',
        ]
