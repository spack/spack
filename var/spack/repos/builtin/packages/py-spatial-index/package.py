# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySpatialIndex(PythonPackage):
    """Spatial index for NGV project"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/molecularsystems/MorphSpatialIndex"
    git      = "ssh://bbpcode.epfl.ch/molecularsystems/MorphSpatialIndex"

    version('develop', branch='master', submodules=True)
    version('0.0.1', tag='spatial-index-v0.0.1', submodules=True, preferred=True)

    depends_on('cmake@3.2:', type='build')
    depends_on('boost@1.65:', type='build')
    depends_on('py-setuptools', type='build')

    depends_on('py-numpy@1.13.1:', type='run')
