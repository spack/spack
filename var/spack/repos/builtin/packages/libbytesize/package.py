# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libbytesize(AutotoolsPackage):
    """The goal of this project is to provide a tiny library that would
    facilitate the common operations with sizes in bytes."""

    homepage = "https://github.com/storaged-project/libbytesize"
    url      = "https://github.com/storaged-project/libbytesize/archive/2.4.tar.gz"

    version('2.4', sha256='aab45b8fc4f5d9a949750bd863bd268e50a899777a4576a33bef2fd1d827e225')
    version('2.3', sha256='3c74113fc8cd1a2fbd8870fa0ed7cef2ef24d60ef91e7145fbc041f9aa144479')
    version('2.2', sha256='b93c54b502880c095c9f5767a42464853e2687db2e5e3084908a615bafe73baa')

    depends_on('gettext',  type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    extends('python')
    depends_on('pcre2')
    depends_on('gmp')
    depends_on('mpfr')

    def autoreconf(self, spec, prefix):
        sh = which('sh')
        sh('./autogen.sh')
