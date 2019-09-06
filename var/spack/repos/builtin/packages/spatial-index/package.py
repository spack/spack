# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class SpatialIndex(PythonPackage):
    """Spatial indexer for geometries and morphologies"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/hpc/SpatialIndex"
    git      = "ssh://bbpcode.epfl.ch/hpc/SpatialIndex"
    url      = "ssh://bbpcode.epfl.ch/hpc/SpatialIndex"

    depends_on("py-setuptools")
    depends_on("cmake")
    depends_on("boost")

    version('0.1.0', tag='0.1.0', submodules=True)


