##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Lftp(AutotoolsPackage):
    """LFTP is a sophisticated file transfer program supporting a number
       of network protocols (ftp, http, sftp, fish, torrent)."""

    homepage = "http://lftp.yar.ru/"
    url      = "http://lftp.yar.ru/ftp/lftp-4.7.7.tar.gz"

    version('4.7.7', 'ddc71b3b11a1af465e829075ae14b3ff')

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
