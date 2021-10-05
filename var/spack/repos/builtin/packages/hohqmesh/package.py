# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hohqmesh(CMakePackage):
    """High Order mesh generator for Hexahedral and Quadrilateral meshes."""

    homepage = "https://github.com/trixi-framework/HOHQMesh"
    url      = "https://github.com/trixi-framework/HOHQMesh"
    git      = "https://github.com/trixi-framework/HOHQMesh.git"

    maintainers = ['schoonovernumerics']

    version('main', branch='main')

    depends_on('ftobjectlibrary')

    parallel = False
