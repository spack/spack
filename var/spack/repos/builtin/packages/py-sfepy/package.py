# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySfepy(PythonPackage):
    """SfePy (https://sfepy.org/) is a software for solving systems of coupled
    partial differential equations (PDEs) by the finite element method in 1D,
    2D and 3D. It can be viewed both as black-box PDE solver, and as a Python
    package which can be used for building custom applications.
    """

    homepage = "https://sfepy.org"
    url      = "https://github.com/sfepy/sfepy/archive/release_2021.3.tar.gz"
    git      = "https://github.com/sfepy/sfepy.git"

    version('2021.3', sha256='b2a760b0f3277ac223ff25821a4156b48d06b3769e6a9a3bd0bffef5a43cbe17')
    version('2017.3', sha256='d13642b7abed63b83b7eaef4dfce6e84a5afc5798bc7ffa1c413e3e44b5e5996', deprecated=True)

    variant('petsc', default=False, description='Enable PETSc support')
    variant('slepc', default=False, description='Enable SLEPc support')
    variant('pyamg', default=False, description='Enable PyAMG support')
    variant('mumps', default=False, description='Enable MUMPS support')

    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six', type='run')
    depends_on('py-scipy', type='run')
    depends_on('py-matplotlib', type='run')
    depends_on('py-sympy', type='run')
    depends_on('hdf5+hl', type='run')
    depends_on('py-tables', type='run')
    depends_on('py-meshio', type='run', when='@2021.3')
    depends_on('py-psutil', type='run', when='@2021.3')
    depends_on('py-pyvista', type='run', when='@2021.3')
    depends_on('py-opt-einsum', type='run', when='@2021.3')
    depends_on('py-dask', type='run', when='@2021.3')
    depends_on('py-petsc4py', type='run', when='+petsc')
    depends_on('py-slepc4py', type='run', when='+slepc @2021.3')
    depends_on('py-pyamg', type='run', when='+pyamg @2021.3')
    depends_on('mumps', type='run', when='+mumps @2021.3')
