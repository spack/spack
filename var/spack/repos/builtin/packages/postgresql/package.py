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
from spack.pkg.builtin.postgresql_client import PostgresqlClient


# Inherit from the client only build, adding any server-specific tweaks.
class Postgresql(PostgresqlClient):
    """PostgreSQL is a powerful, open source object-relational database system.
    It has more than 15 years of active development and a proven architecture
    that has earned it a strong reputation for reliability, data integrity, and
    correctness."""

    homepage = "http://www.postgresql.org/"
    url      = "http://ftp.postgresql.org/pub/source/v9.3.4/postgresql-9.3.4.tar.bz2"

    version('10.3', '506498796a314c549388cafb3d5c717a')
    version('10.2', 'e97c3cc72bdf661441f29069299b260a')
    version('9.6.6', '7c65858172597de7937efd88f208969b')
    version('9.5.3', '3f0c388566c688c82b01a0edf1e6b7a0')
    version('9.3.4', 'd0a41f54c377b2d2fab4a003b0dac762')

    # Note that variants and dependencies are inherited from
    # PostgresqlClient. If you override configure_args(), be sure to
    # invoke the superclass' configure_args() to make sure the common
    # variant selections are honored.

    def install(self, spec, prefix):
        """Invoke the standard package install method, bypassing
        that from the client.
        """
        AutotoolsPackage.install(self, spec, prefix)
