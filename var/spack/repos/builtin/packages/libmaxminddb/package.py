# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libmaxminddb(AutotoolsPackage):
    """C library for the MaxMind DB file format"""

    homepage = "https://github.com/maxmind/libmaxminddb"
    url      = "https://github.com/maxmind/libmaxminddb/releases/download/1.3.2/libmaxminddb-1.3.2.tar.gz"

    version('1.3.2', '67a861965b30d045bf29a2126bcc05ed')

    def configure_args(self):
        args = ['--disable-debug',
                '--disable-dependency-tracking',
                '--disable-silent-rules']
        return args
