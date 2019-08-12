# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BppCore(CMakePackage):
    """Bio++ core library."""

    homepage = "http://biopp.univ-montp2.fr/wiki/index.php/Installation"
    url      = "http://biopp.univ-montp2.fr/repos/sources/bpp-core-2.2.0.tar.gz"

    version('2.2.0', '5789ed2ae8687d13664140cd77203477')

    depends_on('cmake@2.6:', type='build')

    def cmake_args(self):
        return ['-DBUILD_TESTING=FALSE']
