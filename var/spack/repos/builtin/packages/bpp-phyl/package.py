# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BppPhyl(CMakePackage):
    """Bio++ phylogeny library."""

    homepage = "http://biopp.univ-montp2.fr/wiki/index.php/Installation"
    url      = "http://biopp.univ-montp2.fr/repos/sources/bpp-phyl-2.2.0.tar.gz"

    version('2.2.0', '5c40667ec0bf37e0ecaba321be932770')

    depends_on('cmake@2.6:', type='build')
    depends_on('bpp-core')
    depends_on('bpp-seq')

    def cmake_args(self):
        return ['-DBUILD_TESTING=FALSE']
