# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install frontistr
#
# You can edit this file again by typing:
#
#     spack edit frontistr
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Frontistr(CMakePackage):
    """Large-Scale Parallel FEM Program for Nonlinear Structural Analysis : FrontISTR"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.frontistr.com"
    url      = "https://gitlab.com/FrontISTR-Commons/FrontISTR/-/archive/v5.0/FrontISTR-v5.0.tar.gz"
    #url      = "https://gitlab.com/FrontISTR-Commons/FrontISTR/-/archive/master/FrontISTR-master.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('5.0', sha256='b60e77146da0b46d0b094416bab01298a44c33bbcf705763473be294a78c8993')
    #version('master', git='https://gitlab.com/FrontISTR-Commons/FrontISTR.git', commit='73aed597fc0894bde7ae8d19365447acfde424d5')
    version('master', git='https://gitlab.com/FrontISTR-Commons/FrontISTR.git')

    # FIXME: Add dependencies if required.
    depends_on('mpi', type=('build', 'link', 'run'))
    depends_on('lapack', type=('build', 'link'))
    depends_on('blas', type=('build', 'link'))
    depends_on('mumps +metis', type=('build', 'link'))
    depends_on('metis', type=('build', 'link'))
    depends_on('trilinos -zoltan2 -tpetra -teuchos -suite-sparse -sacado -muelu -kokkos -ifpack2 -ifpack -hypre -hdf5 -gtest -explicit_template_instantiation -exodus -epetraext -epetra -boost -belos -aztec -anasazi -amesos2 -amesos', type=('build', 'link'))
    depends_on('cmake', type='build')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
