# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    maintainers = ['dalcinl', 'balay']

    version('develop', branch='master')
    version('3.13.0', sha256='fd41d9c399f8a110f33b62c46ece776755113116bf42d4984053ea3a52a3efae')
    version('3.12.0', sha256='1ddffc35163ec81de50ca43b8a82fdbe73baf02d9e24d594685d5f4a6c17a8cb')
    version('3.11.0', sha256='50a7bbca76000da287d5b18969ddf4743b360bda1f6ee3b43b5829095569cc46')
    version('3.10.1', sha256='4eae5eaf459875b1329cae36fa1e5e185f603e8b01a4e05b59b0983c02b5a174')
    version('3.10.0', sha256='737e7812ccc54b1e0d6e8de4bdcd886c8ce287129297831f1f0e33089fa352f2')
    version('3.9.1',  sha256='9bad0bab69a19bbceb201b9203708104a0bbe0ee19c0fa839b6ea6aa55dc238c')
    version('3.9.0',  sha256='034d097b88ae874de712785f39f9d9a06329da071479c0dd834704dc6885dc97')
    version('3.8.1',  sha256='da07ffef7da61164ad75b23af59860fea467ae47532302d91b7b4ec561aa0f9c')
    version('3.8.0',  sha256='b9b728e39245213cd8e74cf4724be9bb48bd295f99634135e37dbbdbec275244')
    version('3.7.0',  sha256='fb78b50c596c3ba6a097751dd9a379e7acaf57edd36311a3afa94caa4312ee08')

    variant('mpi', default=True,  description='Activates MPI support')

    depends_on('py-cython', type='build', when='@develop')
    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-mpi4py', when='+mpi', type=('build', 'run'))

    depends_on('petsc+mpi', when='+mpi')
    depends_on('petsc~mpi', when='~mpi')
    depends_on('petsc@develop', when='@develop')
    depends_on('petsc@3.13:3.13.99', when='@3.13:3.13.99')
    depends_on('petsc@3.12:3.12.99', when='@3.12:3.12.99')
    depends_on('petsc@3.11:3.11.99', when='@3.11:3.11.99')
    depends_on('petsc@3.10.3:3.10.99', when='@3.10.1:3.10.99')
    depends_on('petsc@3.10:3.10.2', when='@3.10.0')
    depends_on('petsc@3.9:3.9.99', when='@3.9:3.9.99')
    depends_on('petsc@3.8:3.8.99', when='@3.8:3.8.99')
    depends_on('petsc@3.7:3.7.99', when='@3.7:3.7.99')
    depends_on('petsc@3.6:3.6.99', when='@3.6:3.6.99')
