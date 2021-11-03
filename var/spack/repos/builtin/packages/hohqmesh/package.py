# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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

    version('1.1.0', sha256='977109d57dbb6b74c2d2c52b9bc3ac5ad4ecbfaa0dbe3ef2291f68eea05f1b78')
    version('1.0.1', sha256='83c2c48aec9cd6b1ade0d9b04a0d68782ea7e0a5d9fb28ac7510d4ad401e64ee')
    version('1.0.0', sha256='b5e983fa4a34311042e29792bf0e233fafc63b8f98873c041b8f7e4f1e26a19f')


    depends_on('ftobjectlibrary')

    parallel = False
