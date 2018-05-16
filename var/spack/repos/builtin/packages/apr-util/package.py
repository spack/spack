##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class AprUtil(AutotoolsPackage):
    """Apache Portable Runtime Utility"""

    homepage  = 'https://apr.apache.org/'
    url       = 'http://archive.apache.org/dist/apr/apr-util-1.6.0.tar.gz'

    version('1.6.0', '3b03dbff60728a4f4c33f5d929e8b35a')
    version('1.5.4', '866825c04da827c6e5f53daff5569f42')

    variant('crypto', default=True,  description='Enable crypto support')
    variant('gdbm',   default=False, description='Enable GDBM support')
    variant('pgsql',  default=False, description='Enable PostgreSQL support')
    variant('sqlite', default=False, description='Enable sqlite DBD driver')
    variant('odbc',   default=False, description='Enalbe ODBC support')

    depends_on('apr')
    depends_on('expat')
    depends_on('libiconv')

    depends_on('openssl', when='+crypto')
    depends_on('gdbm', when='+gdbm')
    depends_on('postgresql', when='+pgsql')
    depends_on('sqlite', when='+sqlite')
    depends_on('unixodbc', when='+odbc')

    def configure_args(self):
        spec = self.spec

        args = [
            '--with-apr={0}'.format(spec['apr'].prefix),
            '--with-expat={0}'.format(spec['expat'].prefix),
            '--with-iconv={0}'.format(spec['libiconv'].prefix),
            # TODO: Add support for the following database managers
            '--without-ndbm',
            '--without-berkeley-db',
            '--without-mysql',
            '--without-oracle',
        ]

        if '+crypto' in spec:
            args.extend([
                '--with-crypto',
                '--with-openssl={0}'.format(spec['openssl'].prefix),
            ])
        else:
            args.append('--without-crypto')

        if '+gdbm' in spec:
            args.append('--with-gdbm={0}'.format(spec['gdbm'].prefix))
        else:
            args.append('--without-gdbm')

        if '+pgsql' in spec:
            args.append('--with-pgsql={0}'.format(spec['postgresql'].prefix))
        else:
            args.append('--without-pgsql')

        if '+sqlite' in spec:
            if spec.satisfies('^sqlite@3.0:3.999'):
                args.extend([
                    '--with-sqlite3={0}'.format(spec['sqlite'].prefix),
                    '--without-sqlite2',
                ])
            elif spec.satisfies('^sqlite@2.0:2.999'):
                args.extend([
                    '--with-sqlite2={0}'.format(spec['sqlite'].prefix),
                    '--without-sqlite3',
                ])
        else:
            args.extend([
                '--without-sqlite2',
                '--without-sqlite3',
            ])

        if '+odbc' in spec:
            args.append('--with-odbc={0}'.format(spec['unixodbc'].prefix))
        else:
            args.append('--without-odbc')

        return args

    def check(self):
        # FIXME: Database driver tests fail, at least on macOS:
        #
        # Failed to load driver file apr_dbd_pgsql.so
        # Failed to load driver file apr_dbd_sqlite3.so
        # Failed to load driver file apr_dbd_odbc.so

        # Tests occassionally fail when run in parallel
        make('check', parallel=False)
