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


class Libmongoc(AutotoolsPackage):
    """libmongoc is a client library written in C for MongoDB."""

    homepage = "https://github.com/mongodb/mongo-c-driver"
    url      = "https://github.com/mongodb/mongo-c-driver/releases/download/1.7.0/mongo-c-driver-1.7.0.tar.gz"

    version('1.7.0', '21acf3584e92631422bc91e9e3cf4f76')
    version('1.6.3', '0193610cf1d98aae7008f272a1000972')
    version('1.6.2', 'aac86df153282cda1e4905cca181631a')
    version('1.6.1', '826946de9a15f7f453aefecdc76b1c0d')

    variant('ssl', default=True, description='Enable SSL support.')
    variant('snappy', default=True, description='Enable Snappy support.')
    variant('zlib', default=True, description='Enable zlib support.')

    depends_on('libbson')

    depends_on('openssl', when='+ssl')
    depends_on('snappy', when='+snappy')
    depends_on('zlib', when='+zlib')

    def configure_args(self):
        spec = self.spec

        args = [
            '--disable-automatic-init-and-cleanup',
            '--with-libbson=system'
        ]

        if '+ssl' in spec:
            args.append('--enable-ssl=openssl')
        else:
            args.append('--enable-ssl=no')

        if spec.satisfies('@1.7.0:'):
            # --with-{snappy,zlib}=system are currently broken and cause
            # configure to not find the dependencies. We still want to
            # explicitly disable them when appropriate.
            if '+snappy' not in spec:
                args.append('--with-snappy=no')
            if '+zlib' not in spec:
                args.append('--with-zlib=no')

        return args
