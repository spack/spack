# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BppSeq(CMakePackage):
    """Bio++ seq library."""

    homepage = "http://biopp.univ-montp2.fr/wiki/index.php/Installation"
    url      = "http://biopp.univ-montp2.fr/repos/sources/bpp-seq-2.2.0.tar.gz"

    version('2.2.0', '44adef0ff4d5ca4e69ccf258c9270633')

    depends_on('cmake@2.6:', type='build')
    depends_on('bpp-core')

    def cmake_args(self):
        return ['-DBUILD_TESTING=FALSE']
