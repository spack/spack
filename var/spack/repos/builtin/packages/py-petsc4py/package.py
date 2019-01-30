# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPetsc4py(PythonPackage):
    """This package provides Python bindings for the PETSc package.
    """

    homepage = "https://pypi.python.org/pypi/petsc4py"
    url      = "https://pypi.io/packages/source/p/petsc4py/petsc4py-3.8.1.tar.gz"

    version('3.8.1', '5157220c2b81765c581d2b17c03259f8')
    version('3.8.0', '02029be4bdec904854f0e0692005fb06')
    version('3.7.0', '816a20040a6a477bd637f397c9fb5b6d')

    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-mpi4py', type=('build', 'run'))
    depends_on('petsc+mpi')
