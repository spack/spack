# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lftp(AutotoolsPackage):
    """LFTP is a sophisticated file transfer program supporting a number
       of network protocols (ftp, http, sftp, fish, torrent)."""

    homepage = "http://lftp.yar.ru/"
    url      = "http://lftp.yar.ru/ftp/lftp-4.7.7.tar.gz"

    version('4.9.2', sha256='a37589c61914073f53c5da0e68bd233b41802509d758a022000e1ae2076da733')
    version('4.9.1', sha256='02336d4ffc617b453e7cfd335f3a424758408ff31a10720d59add86e3737966a')
    version('4.9.0', sha256='2f799849f54e1d7f9013a751b69732782ea13a51b32b119940637cd469111ca7')
    version('4.8.4', sha256='19f3a4236558fbdb88eec01bc9d693c51b122d23487b6bedad4cc67ae6825fc2')
    version('4.8.3', sha256='cfbbbd067c25ff9d629828a010cc700214859b02e33b2405dfe7ed045d080f0f')
    version('4.8.2', sha256='9b21261faaa05d4fd235589cc21e2e45fc14c9314d7b4bb1f1aec44ea39eb3ee')
    version('4.8.1', sha256='6117866215cd889dab30ff73292cd1d35fe0e12a9af5cd76d093500d07ab65a3')
    version('4.7.7', sha256='7bce216050094a1146ed05bed8fe5b3518224764ffe98884a848d44dc76fff8f')
    version('4.6.4', sha256='791e783779d3d6b519d0c23155430b9785f2854023eb834c716f5ba78873b15a')

    depends_on('expat')
    depends_on('iconv')
    depends_on('ncurses')
    depends_on('openssl')
    depends_on('readline')
    depends_on('zlib')

    def configure_args(self):
        return [
            '--with-expat={0}'.format(self.spec['expat'].prefix),
            '--with-libiconv={0}'.format(self.spec['iconv'].prefix),
            '--with-openssl={0}'.format(self.spec['openssl'].prefix),
            '--with-readline={0}'.format(self.spec['readline'].prefix),
            '--with-zlib={0}'.format(self.spec['zlib'].prefix),
            '--disable-dependency-tracking',
        ]
