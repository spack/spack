# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jansson(CMakePackage):
    """Jansson is a C library for encoding, decoding and manipulating JSON
       data."""

    homepage = "http://www.digip.org/jansson/"
    url      = "https://github.com/akheron/jansson/archive/v2.9.tar.gz"
    maintainers = ['ax3l']

    version('2.9', sha256='952fa714b399e71c1c3aa020e32e899f290c82126ca4d0d14cff5d10af457656')

    variant('shared', default=True,
            description='Enables the build of shared libraries')

    def cmake_args(self):
        return [
            '-DJANSSON_BUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in self.spec else 'OFF'),
        ]
