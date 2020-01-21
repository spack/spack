# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libaec(CMakePackage):
    """Libaec provides fast lossless compression of 1 up to 32 bit wide signed
       or unsigned integers (samples). It implements Golomb-Rice compression
       method under the BSD license and includes a free drop-in replacement for
       the SZIP library.
    """

    homepage = 'https://gitlab.dkrz.de/k202009/libaec'
    url = 'https://gitlab.dkrz.de/api/v4/projects/k202009%2Flibaec/repository/archive.tar.gz?sha=v1.0.2'
    list_url = 'https://gitlab.dkrz.de/k202009/libaec/tags'

    provides('szip')

    version('1.0.2', sha256='b9e5bbbc8bf9cbfd3b9b4ce38b3311f2c88d3d99f476edb35590eb0006aa1fc5')
    version('1.0.1', sha256='3668eb4ed36724441e488a7aadc197426afef4b1e8bd139af6d3e36023906459')
    version('1.0.0', sha256='849f08b08ddaaffe543d06d0ced5e4ee3e526b13a67c5f422d126b1c9cf1b546')
