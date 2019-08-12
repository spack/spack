# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libjpeg(AutotoolsPackage):
    """libjpeg is a widely used free library with functions for handling the
    JPEG image data format. It implements a JPEG codec (encoding and decoding)
    alongside various utilities for handling JPEG data."""

    homepage = "http://www.ijg.org"
    url      = "http://www.ijg.org/files/jpegsrc.v9c.tar.gz"

    version('9c', '93c62597eeef81a84d988bccbda1e990')
    version('9b', '6a9996ce116ec5c52b4870dbcd6d3ddb')
    version('9a', '3353992aecaee1805ef4109aadd433e7')

    provides('jpeg')

    def check(self):
        # Libjpeg has both 'check' and 'test' targets that are aliases.
        # Only need to run the tests once.
        make('check')
