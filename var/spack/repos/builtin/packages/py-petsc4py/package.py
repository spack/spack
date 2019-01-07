# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPetsc4py(PythonPackage):
    """This package provides Python bindings for the PETSc package.
    """

    homepage = "https://bitbucket.org/petsc/petsc4py"
    url      = "https://bitbucket.org/petsc/petsc4py/get/3.10.0.tar.gz"
    git      = "https://bitbucket.org/petsc/petsc4py.git"

    version('3.10.0', sha256='737e7812ccc54b1e0d6e8de4bdcd886c8ce287129297831f1f0e33089fa352f2')
    version('3.9.1',  sha256='9bad0bab69a19bbceb201b9203708104a0bbe0ee19c0fa839b6ea6aa55dc238c')
    version('3.9.0',  sha256='034d097b88ae874de712785f39f9d9a06329da071479c0dd834704dc6885dc97')
    version('3.8.1',  sha256='da07ffef7da61164ad75b23af59860fea467ae47532302d91b7b4ec561aa0f9c')
    version('3.8.0',  sha256='b9b728e39245213cd8e74cf4724be9bb48bd295f99634135e37dbbdbec275244')
    version('3.7.0',  sha256='fb78b50c596c3ba6a097751dd9a379e7acaf57edd36311a3afa94caa4312ee08')

    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-mpi4py', type=('build', 'run'))

    depends_on('petsc+mpi')
    depends_on('petsc@3.10:3.10.99+mpi', when='@3.10:3.10.99')
    depends_on('petsc@3.9:3.9.99+mpi', when='@3.9:3.9.99')
    depends_on('petsc@3.8:3.8.99+mpi', when='@3.8:3.8.99')
    depends_on('petsc@3.7:3.7.99+mpi', when='@3.7:3.7.99')
    depends_on('petsc@3.6:3.6.99+mpi', when='@3.6:3.6.99')
