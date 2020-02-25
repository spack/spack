# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Meshball(CMakePackage):
    """Tool for generating meshes from morphology file"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/viz/MeshBall"
    git = "ssh://bbpcode.epfl.ch/viz/MeshBall"

    generator = 'Ninja'

    version('0.1.0', tag='v0.1.0', submodules=True)

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')

    depends_on('brion')
    depends_on('cgal')

    def cmake_args(self):
        return ['-DGLM_INSTALL_ENABLE=OFF',
                '-DCMAKE_CXX_FLAGS=-Wno-deprecated-declarations']
