# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMorphmath(PythonPackage):
    """General mathematics functions for NGV project"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/molecularsystems/MorphMath"
    git      = "ssh://bbpcode.epfl.ch/molecularsystems/MorphMath"

    version('develop', branch='master')
    version('0.0.2', tag='morphmath-v0.0.2', preferred=True)

    depends_on('py-setuptools', type='build')

    depends_on('py-numpy', type='run')
    depends_on('py-scipy', type='run')
