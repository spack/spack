# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
