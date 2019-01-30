# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
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

    version('2.9', 'd2db25c437b359fc5a065ed938962237')

    variant('shared', default=True,
            description='Enables the build of shared libraries')

    def cmake_args(self):
        return [
            '-DJANSSON_BUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in self.spec else 'OFF'),
        ]
