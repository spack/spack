# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Minizip(AutotoolsPackage):
    """C library for zip/unzip via zLib."""

    homepage = "http://www.winimage.com/zLibDll/minizip.html"
    url      = "https://zlib.net/fossils/zlib-1.2.11.tar.gz"

    version('1.2.11', sha256='c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1')

    configure_directory = 'contrib/minizip'

    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('zlib')
