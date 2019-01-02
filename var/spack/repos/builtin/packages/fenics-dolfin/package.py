# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FenicsDolfin(CMakePackage):
    """DOLFIN is the C++/Python interface of FEniCS."""

    homepage = "http://fenicsproject.org/"
    git      = "https://bitbucket.org/fenics-project/dolfin.git"

    # Use this url for version >= 2017.1.0
    url      = "https://bitbucket.org/fenics-project/dolfin/get/2018.1.0.post2.tar.gz"

    # version('develop', branch='master')
    version('2018.1.0.post2', sha256='a71db38740a7ea508f8a725af4b08ccd024168b450033b032b003a5aac1708cf')
    version('2018.1.0.post1', sha256='ca8f95d03cafd999fe592941c2776474130406a09abf072ea2e6e93e249af38b')
    version('2018.1.0.post0', sha256='6c5195c9795decc021ffc713614b7885098912fcd89e3da79fd8428cbaf8212b')
    version('2018.1.0',       sha256='2afb54e2f8a2c7be5a89e4ef224b68ae514c32168c9a94b1921d62339f8decd4')
    version('2017.2.0.post0', sha256='4169c7e4d22af76bad39c2c20443c4fa75356078d4e7360d4ea924c76a5c9cd3')
    version('2017.2.0',       sha256='90f77796372eed63f529bafa7c05afa3d5bfeb5f378d3e4e9d53959c0c06bbe7')
    version('2017.1.0.post0', sha256='25e557491d7fdff0967ef99c678ec77eb0e5f58a3a6b8b31c45e5ca2bdc85912')
    version('2017.1.0',       sha256='a496574e9a1310806838c7ef32d442ef77379f879ab6a5742bbe521f171d5f88')

    # FIXME: Older versions prepend name to version in url
    # url      = "https://bitbucket.org/fenics-project/dolfin/get/dolfin-2016.2.0.tar.gz"

    # version('2016.2.0',       sha256='c6760996660a476f77889e11e4a0bc117cc774be0eec777b02a7f01d9ce7f43d')
    # version('2016.1.0',       sha256='0db95c8f193fd56d741cb90682e0a6a21e366c4f48d33e1eb501d2f98aa1a05b')
    # version('1.6.0',          sha256='67f66c39983a8c5a1ba3c0787fa9b9082778bc7227b25c7cad80dc1299e0a201')
    # version('1.5.0',          sha256='9dd915b44fd833f16121dbb14b668795ab276ada40a111d9366261077200bed3')
    # version('1.4.0',          sha256='64f058466a312198ea2b9de191bd4fbecaa70eb1c88325d03e680edb606b46cd')
    # version('1.3.0',          sha256='04ea667c25ca57c84436d9dfe0233d610fc7e25c3ade3fb8c6c38b1260d68dae')

    variant('python',       default=False, description='Compile with DOLFIN Python interface')
    variant('hdf5',         default=True,  description='Compile with HDF5')
    variant('parmetis',     default=True,  description='Compile with ParMETIS')
    variant('scotch',       default=True,  description='Compile with Scotch')
    variant('petsc',        default=False, description='Compile with PETSc')
    variant('slepc',        default=False, description='Compile with SLEPc')
    variant('trilinos',     default=True,  description='Compile with Trilinos')
    variant('suite-sparse', default=True,  description='Compile with SuiteSparse solvers')
    variant('vtk',          default=False, description='Compile with VTK')
    variant('qt',           default=False, description='Compile with QT')
    variant('mpi',          default=True,  description='Enables the distributed memory support')
    variant('openmp',       default=True,  description='Enables the shared memory support')
    variant('shared',       default=True,  description='Enables the build of shared libraries')
    variant('doc',          default=False, description='Builds the documentation')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo',
                    'MinSizeRel', 'Developer'))

    patch('petsc-3.7.patch', when='@1.6.1^petsc@3.7:')
    patch('petsc-version-detection.patch', when='@:1.6.1')
    patch('hdf5~cxx-detection.patch', when='@2016.2.0')

    extends('python', when='+python')

    depends_on('py-fenics-ffc', type=('build'), when='~python')
    depends_on('py-fenics-ffc', type=('build', 'run'), when='+python')

    depends_on('eigen@3.2.0:')
    depends_on('boost+filesystem+program_options+system+iostreams+timer+regex+chrono')

    depends_on('mpi', when='+mpi')
    # FIXME: next line fixes concretization with petsc
    depends_on('hdf5+hl+fortran', when='+hdf5+petsc')
    depends_on('hdf5+hl', when='+hdf5~petsc')
    depends_on('parmetis@4.0.2:^metis+real64', when='+parmetis')
    depends_on('scotch~metis', when='+scotch~mpi')
    depends_on('scotch+mpi~metis', when='+scotch+mpi')
    depends_on('petsc@3.6:3.9.99', when='+petsc')
    depends_on('slepc@3.6:3.9.99', when='+slepc')
    depends_on('py-petsc4py@3.6:3.9.99', when='+petsc+python')
    depends_on('py-slepc4py@3.6:3.9.99', when='+slepc+python')
    depends_on('trilinos', when='+trilinos')
    depends_on('vtk', when='+vtk')
    depends_on('suite-sparse', when='+suite-sparse')
    depends_on('qt', when='+qt')

    depends_on('py-pybind11@2.2.3', when='@2018.1:+python')
    depends_on('swig@3.0.3:', type=('build', 'run'), when='@:2017.2.0.99+python')
    depends_on('cmake@2.8.12:', type='build')

    depends_on('py-setuptools', type='build', when='+python')
    depends_on('py-sphinx@1.0.1:', type='build', when='+python+doc')

    def cmake_is_on(self, option):
        return 'ON' if option in self.spec else 'OFF'

    def cmake_args(self):
        return [
            '-DDOLFIN_ENABLE_DOCS:BOOL={0}'.format(
                self.cmake_is_on('+doc')),
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                self.cmake_is_on('+shared')),
            '-DDOLFIN_SKIP_BUILD_TESTS:BOOL=ON',
            '-DDOLFIN_ENABLE_OPENMP:BOOL={0}'.format(
                self.cmake_is_on('+openmp')),
            '-DDOLFIN_ENABLE_CHOLMOD:BOOL={0}'.format(
                self.cmake_is_on('suite-sparse')),
            '-DDOLFIN_ENABLE_HDF5:BOOL={0}'.format(
                self.cmake_is_on('hdf5')),
            '-DDOLFIN_ENABLE_MPI:BOOL={0}'.format(
                self.cmake_is_on('mpi')),
            '-DDOLFIN_ENABLE_PARMETIS:BOOL={0}'.format(
                self.cmake_is_on('parmetis')),
            '-DDOLFIN_ENABLE_PASTIX:BOOL={0}'.format(
                self.cmake_is_on('pastix')),
            '-DDOLFIN_ENABLE_PETSC:BOOL={0}'.format(
                self.cmake_is_on('petsc')),
            '-DDOLFIN_ENABLE_PETSC4PY:BOOL={0}'.format(
                self.cmake_is_on('py-petsc4py')),
            '-DDOLFIN_ENABLE_PYTHON:BOOL={0}'.format(
                self.cmake_is_on('python')),
            '-DDOLFIN_ENABLE_QT:BOOL={0}'.format(
                self.cmake_is_on('qt')),
            '-DDOLFIN_ENABLE_SCOTCH:BOOL={0}'.format(
                self.cmake_is_on('scotch')),
            '-DDOLFIN_ENABLE_SLEPC:BOOL={0}'.format(
                self.cmake_is_on('slepc')),
            '-DDOLFIN_ENABLE_SLEPC4PY:BOOL={0}'.format(
                self.cmake_is_on('py-slepc4py')),
            '-DDOLFIN_ENABLE_SPHINX:BOOL={0}'.format(
                self.cmake_is_on('py-sphinx')),
            '-DDOLFIN_ENABLE_TRILINOS:BOOL={0}'.format(
                self.cmake_is_on('trilinos')),
            '-DDOLFIN_ENABLE_UMFPACK:BOOL={0}'.format(
                self.cmake_is_on('suite-sparse')),
            '-DDOLFIN_ENABLE_VTK:BOOL={0}'.format(
                self.cmake_is_on('vtk')),
            '-DDOLFIN_ENABLE_ZLIB:BOOL={0}'.format(
                self.cmake_is_on('zlib')),
        ]

    # FIXME: Install DOLFIN Python interface
