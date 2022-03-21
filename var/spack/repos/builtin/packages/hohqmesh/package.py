# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hohqmesh(CMakePackage):
    """High Order mesh generator for Hexahedral and Quadrilateral meshes."""

    homepage = "https://github.com/trixi-framework/HOHQMesh"
    git      = "https://github.com/trixi-framework/HOHQMesh.git"
    url      = "https://github.com/trixi-framework/HOHQMesh/archive/v1.0.0.tar.gz"

    maintainers = ['fluidnumerics-joe']

    version('1.2.1', sha256='b1b13a680c3ef6b8d6a8d05406f68c1ff641c26f69c468ccf2d7bed8d556dd7e')
    version('1.1.0', sha256='5fdb75157d9dc29bba55e6ae9dc2be71294754204f4f0912795532ae66aada10')
    version('1.0.1', sha256='8435f13c96d714a287f3c24392330047e2131d53fafe251a77eba365bd2b3141')
    version('1.0.0', sha256='3800e63975d0a61945508f13fb76d5e2145c0260440484252b6b81aa0bfe076d')

    depends_on('ftobjectlibrary')

    parallel = False
