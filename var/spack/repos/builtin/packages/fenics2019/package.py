# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fenics2019(CMakePackage):
    """FEniCS is organized as a collection of interoperable components
    that together form the FEniCS Project. These components include
    the problem-solving environment DOLFIN, the form compiler FFC, the
    finite element tabulator FIAT, the just-in-time compiler Instant,
    the code generation interface UFC, the form language UFL and a
    range of additional components."""

    homepage = "http://fenicsproject.org/"
    git      = "https://bitbucket.org/fenics-project/dolfin.git"

    # Tarball for 2019.1.0 git version
    url      = "https://bitbucket.org/fenics-project/dolfin/downloads/dolfin-2019.1.0.tar.gz"
    version('2019.1.0.post0', sha256='61abdcdb13684ba2a3ba4afb7ea6c7907aa0896a46439d3af7e8848483d4392f')

    variant('python',       default=True,
            description='Compile with Dolfin Pyhton interface')
    variant('hdf5',         default=True,  description='Compile with HDF5')
    variant('parmetis',     default=True,  description='Compile with ParMETIS')
    variant('scotch',       default=True,  description='Compile with Scotch')
    variant('petsc',        default=True,  description='Compile with PETSc')
    variant('slepc',        default=True,  description='Compile with SLEPc')
    variant('trilinos',     default=False,  description='Compile with Trilinos')
    variant('suite-sparse', default=True,
            description='Compile with SuiteSparse solvers')
    variant('vtk',          default=False, description='Compile with VTK')
    variant('qt',           default=False, description='Compile with QT')
    variant('mpi',          default=True,
            description='Enables the distributed memory support')
    variant('openmp',       default=True,
            description='Enables the shared memory support')
    variant('shared',       default=True,
            description='Enables the build of shared libraries')
    variant('doc',          default=False,
            description='Builds the documentation')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo',
                    'MinSizeRel', 'Developer'))

    patch('header_fix.patch')

    extends('python', when='+python')

    depends_on('python@3.7.8:', type=('build', 'run'), when='+python')

    depends_on('py-fenics-ffc', type=('build'), when='~python')
    depends_on('py-fenics-ffc', type=('build', 'run'), when='+python')
    depends_on('py-fenics-dijitso', type=('build', 'run'), when='+python')

    depends_on('eigen@3.3.7:')
    depends_on('pkg-config')
    depends_on('zlib')
    depends_on('boost+filesystem+program_options+system+iostreams+timer+regex+chrono')

    depends_on('mpi', when='+mpi')
    # FIXME: next line fixes concretization with petsc
    depends_on('hdf5+hl+fortran', when='+hdf5+petsc')
    depends_on('hdf5+hl', when='+hdf5~petsc')
    depends_on('metis+real64', when='+parmetis')
    depends_on('parmetis', when='+parmetis')
    depends_on('scotch~metis', when='+scotch~mpi')
    depends_on('scotch+mpi~metis', when='+scotch+mpi')
    depends_on('petsc', when='+petsc')
    depends_on('slepc', when='+slepc')
    depends_on('py-petsc4py@3.6:', when='+petsc+python')
    depends_on('trilinos', when='+trilinos')
    depends_on('vtk', when='+vtk')
    depends_on('suite-sparse@4.5.6', when='+suite-sparse')
    depends_on('qt', when='+qt')

    depends_on('py-pybind11', type=('build', 'run'))
    depends_on('cmake@3.17.3:', type='build')

    depends_on('py-setuptools', type='build', when='+python')
    depends_on('py-sphinx@1.0.1:', when='+doc', type='build')

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

    def setup_environment(self, spack_env, run_env):
        spack_env.set('DOLFIN_DIR', self.prefix)

    @run_after('install')
    def install_python_interface(self):
        if '+python' in self.spec:
            cd('python')
            python('setup.py', 'install', '--prefix={0}'.format(self.prefix))
            python('setup.py', 'install',
                   '--single-version-externally-managed',
                   '--root=/', '--prefix={0}'.format(self.prefix))
