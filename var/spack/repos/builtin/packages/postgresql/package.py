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


class Postgresql(AutotoolsPackage):
    """PostgreSQL is a powerful, open source object-relational database system.
    It has more than 15 years of active development and a proven architecture
    that has earned it a strong reputation for reliability, data integrity, and
    correctness."""

    homepage = "http://www.postgresql.org/"
    url      = "http://ftp.postgresql.org/pub/source/v9.3.4/postgresql-9.3.4.tar.bz2"

    version('10.3', '506498796a314c549388cafb3d5c717a')
    version('10.2', 'e97c3cc72bdf661441f29069299b260a')
    version('9.3.4', 'd0a41f54c377b2d2fab4a003b0dac762')
    version('9.5.3', '3f0c388566c688c82b01a0edf1e6b7a0')

    depends_on('openssl')
    depends_on('readline')

    variant('threadsafe', default=False, description='Build with thread safe.')

    def configure_arg(self):
        config_args = ["--with-openssl"]
        if '+threadsafe' in self.spec:
            config_args.append("--enable-thread-safety")
        else:
            config_args.append("--disable-thread-safety")

        return config_args
