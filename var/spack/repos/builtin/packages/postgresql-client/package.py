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
import inspect


class PostgresqlClient(AutotoolsPackage):
    """PostgreSQL is a powerful, open source object-relational database
    system.  It has more than 15 years of active development and a
    proven architecture that has earned it a strong reputation for
    reliability, data integrity, and correctness. This package comprises
    only the client libraries and bindings.
    """

    homepage = "http://www.postgresql.org/"
    url      = "http://ftp.postgresql.org/pub/source/v9.6.6/postgresql-9.6.6.tar.bz2"

    version('10.3', '506498796a314c549388cafb3d5c717a')
    version('10.2', 'e97c3cc72bdf661441f29069299b260a')
    version('9.6.6', '7c65858172597de7937efd88f208969b')
    version('9.5.3', '3f0c388566c688c82b01a0edf1e6b7a0')
    version('9.3.4', 'd0a41f54c377b2d2fab4a003b0dac762')

    variant('threadsafe', default=False, description='Enable thread safety.')
    variant('lineedit',
            default='readline',
            values=('readline', 'libedit', 'none'),
            multi=False,
            description='Line editing library')
    variant('python', default=False,
            description='Enable Python bindings.')
    variant('perl', default=False,
            description='Enable Perl bindings.')
    variant('tcl', default=False,
            description='Enable Tcl bindings.')
    variant('gssapi', default=False,
            description='Build with GSSAPI functionality.')

    provides('postgresql-c')
    provides('postgresql-python', when='+python')
    provides('postgresql-perl', when='+perl')
    provides('postgresql-tcl', when='+tcl')

    depends_on('readline', when='lineedit=readline')
    depends_on('libedit', when='lineedit=libedit')
    depends_on('openssl')
    depends_on('tcl', when='+tcl')
    depends_on('perl', when='+perl')
    depends_on('python', when='+python')

    def configure_args(self):
        config_args = ["--with-openssl"]

        if '+threadsafe' in self.spec:
            config_args.append('--enable-thread-safety')
        else:
            config_args.append('--disable-thread-safety')

        if self.spec.variants['lineedit'].value == 'libedit':
            config_args.append('--with-libedit-preferred')
        elif self.spec.variants['lineedit'].value == 'none':
            config_args.append('--without-readline')

        if '+gssapi' in self.spec:
            config_args.append('--with-gssapi')

        if '+python' in self.spec:
            config_args.append('--with-python')

        if '+perl' in self.spec:
            config_args.append('--with-perl')

        if '+tcl' in self.spec:
            config_args.append('--with-tcl')

        return config_args

    def install(self, spec, prefix):
        """Install only the client libraries.
        """
        for subdir in ('src/bin', 'src/include', 'src/interfaces', 'src/pl'):
            with working_dir(subdir):
                inspect.getmodule(self).make('install')
