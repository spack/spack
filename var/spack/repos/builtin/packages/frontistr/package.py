# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Frontistr(CMakePackage):
    """Large-Scale Parallel FEM Program for Nonlinear Structural Analysis : FrontISTR"""

    homepage = "https://www.frontistr.com"
    url      = "https://gitlab.com/FrontISTR-Commons/FrontISTR/-/archive/v5.0/FrontISTR-v5.0.tar.gz"
    git      = "https://gitlab.com/FrontISTR-Commons/FrontISTR.git"

    version('5.0', sha256='b60e77146da0b46d0b094416bab01298a44c33bbcf705763473be294a78c8993')
    version('master', branch='master')

    variant('build_type', default='RELEASE', description='CMake build type', values=('DEBUG', 'RELEASE'))

    depends_on('cmake~openssl~ncurses', type='build')
    depends_on('mpi', type=('link', 'run'))
    depends_on('lapack', type='link')
    depends_on('blas', type='link')
    depends_on('mumps+metis+parmetis~scotch', type='link')
    depends_on('metis', type='link')
    depends_on('trilinos+openmp~zoltan2~tpetra~teuchos~suite-sparse~sacado\
                ~muelu~kokkos~ifpack2~ifpack~hypre~hdf5~gtest\
                ~explicit_template_instantiation~exodus~epetraext\
                ~epetra~boost~belos~aztec~anasazi~amesos2~amesos\
                ~matio~glm~netcdf', type='link')

    def cmake_args(self):
        args = []
        return args
