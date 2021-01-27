# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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

    # dolfin build options
    variant('python',       default=True,
            description='Compile with Dolfin Pyhton interface')
    variant('hdf5',         default=True,  description='Compile with HDF5')
    variant('parmetis',     default=True,  description='Compile with ParMETIS')
    variant('scotch',       default=True,  description='Compile with Scotch')
    variant('petsc',        default=True,  description='Compile with PETSc')
    variant('slepc',        default=True,  description='Compile with SLEPc')
    variant('py-petsc4py',  default=True,  description='Use PETSC4py')
    variant('py-slepc4py',  default=True,  description='Use SLEPc4py')
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

    variant('zlib',     default=False, description='Compile wit ZLIB')

    # apply patch to fix header issue with latest boost library
    patch('header_fix.patch')

    extends('python', when='+python')

    depends_on('python@3.7.8:', type=('build', 'run'), when='+python')

    # build python components of FEniCS
    depends_on('py-fenics-fiat@2019.1.0', type=('build', 'run'), when='+python')
    depends_on('py-fenics-dijitso@2019.1.0', type=('build', 'run'), when='+python')
    depends_on('py-fenics-ufl@2019.1.0', type=('build', 'run'), when='+python')
    depends_on('py-fenics-ffc@2019.1.0.post0', type=('build'), when='~python')
    depends_on('py-fenics-ffc@2019.1.0.post0', type=('build', 'run'), when='+python')

    depends_on('eigen@3.3.7:')
    depends_on('pkg-config')
    depends_on('zlib')
    depends_on('boost+filesystem+program_options+system+iostreams+timer+regex+chrono')

    depends_on('mpi', when='+mpi')
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
    depends_on('py-pkgconfig', type='run', when='+python')
    depends_on('py-sphinx@1.0.1:', when='+doc', type='build')

    def cmake_args(self):
        opts = [
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define('DOLFIN_SKIP_BUILD_TESTS', True),
            self.define_from_variant('DOLFIN_ENABLE_OPENMP', 'openmp'),
            self.define_from_variant('DOLFIN_ENABLE_CHOLMOD', 'suite-sparse'),
            self.define_from_variant('DOLFIN_ENABLE_HDF5', 'hdf5'),
            self.define_from_variant('DOLFIN_ENABLE_MPI', 'mpi'),
            self.define_from_variant('DOLFIN_ENABLE_PARMETIS', 'parmetis'),
            self.define_from_variant('DOLFIN_ENABLE_PETSC', 'petsc'),
            self.define_from_variant('DOLFIN_ENABLE_PETSC4PY', 'py-petsc4py'),
            self.define_from_variant('DOLFIN_ENABLE_PYTHON', 'python'),
            self.define_from_variant('DOLFIN_ENABLE_QT', 'qt'),
            self.define_from_variant('DOLFIN_ENABLE_SCOTCH', 'scotch'),
            self.define_from_variant('DOLFIN_ENABLE_SLEPC', 'slepc'),
            self.define_from_variant('DOLFIN_ENABLE_SLEPC4PY', 'py-slepc4py'),
            self.define_from_variant('DOLFIN_ENABLE_DOCS', 'doc'),
            self.define_from_variant('DOLFIN_ENABLE_SPHINX', 'doc'),
            self.define_from_variant('DOLFIN_ENABLE_TRILINOS', 'trilinos'),
            self.define_from_variant('DOLFIN_ENABLE_UMFPACK', 'suite-sparse'),
            self.define_from_variant('DOLFIN_ENABLE_VTK', 'vtk'),
            self.define_from_variant('DOLFIN_ENABLE_ZLIB', 'zlib'),
        ]
        return opts

    # set environment for bulding python interface
    def setup_build_environment(self, env):
        env.set('DOLFIN_DIR', self.prefix)

    def setup_run_environment(self, env):
        env.set('DOLFIN_DIR', self.prefix)

    # build python interface of dolfin
    @run_after('install')
    def install_python_interface(self):
        if '+python' in self.spec:
            cd('python')
            python('setup.py', 'install', '--user')
