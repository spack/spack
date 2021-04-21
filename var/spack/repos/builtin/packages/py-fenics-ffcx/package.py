# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFenicsFfcx(PythonPackage):
    """Next generation FEniCS Form Compiler"""

    homepage = "https://github.com/FEniCS/ffcx"
    git = "https://github.com/FEniCS/ffcx.git"
    maintainers = ["js947", "chrisrichardson"]

    version('main', branch='main')
    # version('0.1.0', sha256='')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cffi', type=('build', 'run'))

    depends_on('py-fenics-ufl', type=('build', 'run'), when='@main')
    depends_on('py-fenics-ufl@2019.2.0', type=('build', 'run'), when='@0.1.0')

    depends_on('py-fenics-basix', type=('build', 'run'), when='@main')
    depends_on('py-fenics-basix@0.1.0', type=('build', 'run'), when='@0.1.0')

    depends_on('py-numpy', type=('build', 'run'))
