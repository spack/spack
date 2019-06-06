# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMorphspatial(PythonPackage):
    """Spatial operations functions for NGV project"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/molecularsystems/MorphSpatial"
    git      = "ssh://bbpcode.epfl.ch/molecularsystems/MorphSpatial"

    version('develop', branch='master')
    version('0.0.4', tag='morphspatial-v0.0.4', preferred=True)

    depends_on('py-setuptools', type='build')

    depends_on('py-numpy@1.13:', type='run')
    depends_on('py-scipy@1.0:', type='run')

    depends_on('py-morphmath', type='run')
