# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tethex(CMakePackage):
    """Tethex is designed to convert triangular (in 2D) or tetrahedral (in 3D)
    Gmsh's mesh to quadrilateral or hexahedral one respectively. These meshes
    can be used in software packages working with hexahedrals only - for
    example, deal.II.
    """

    homepage = "https://github.com/martemyev/tethex"
    url      = "https://github.com/martemyev/tethex/archive/v0.0.7.tar.gz"
    git      = "https://github.com/martemyev/tethex.git"

    maintainers = ['davydden']

    version('develop', branch='master')
    version('0.0.7', '6c9e4a18a6637deb4400c6d77ec03184')

    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))

    depends_on('cmake@2.8:', type='build')

    def install(self, spec, prefix):
        # install by hand
        mkdirp(prefix.bin)
        install('tethex', prefix.bin)
