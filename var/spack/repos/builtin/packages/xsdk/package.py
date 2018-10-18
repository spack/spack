# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
from spack import *


class Xsdk(Package):
    """Xsdk is a suite of Department of Energy (DOE) packages for numerical
       simulation. This is a Spack bundle package that installs the xSDK
       packages
    """

    homepage = "http://xsdk.info"

    # Dummy url since Spack complains if I don't list something, will be
    # removed when metapackage is available
    url      = 'http://ftp.mcs.anl.gov/pub/petsc/externalpackages/xsdk.tar.gz'

    version('develop', 'a52dc710c744afa0b71429b8ec9425bc')
    version('0.3.0', 'a52dc710c744afa0b71429b8ec9425bc', preferred=True)
    version('xsdk-0.2.0', 'a52dc710c744afa0b71429b8ec9425bc')

    variant('debug', default=False, description='Compile in debug mode')
    variant('cuda', default=False, description='Enable CUDA dependent packages')

    depends_on('hypre@develop~internal-superlu', when='@develop')
    depends_on('hypre@2.12.1~internal-superlu', when='@0.3.0')
    depends_on('hypre@xsdk-0.2.0~internal-superlu', when='@xsdk-0.2.0')

    depends_on('mfem@develop+mpi+hypre+superlu-dist+petsc+sundials+examples+miniapps', when='@develop')
    depends_on('mfem@3.3.2+mpi+hypre+superlu-dist+petsc+sundials+examples+miniapps', when='@0.3.0')

    depends_on('superlu-dist@develop', when='@develop')
    depends_on('superlu-dist@5.2.2', when='@0.3.0')
    depends_on('superlu-dist@xsdk-0.2.0', when='@xsdk-0.2.0')

    depends_on('trilinos@develop+hypre+superlu-dist+metis+hdf5~mumps+boost~suite-sparse+tpetra+nox+ifpack2+zoltan2+amesos2~exodus',
               when='@develop')
    depends_on('trilinos@12.12.1+hypre+superlu-dist+metis+hdf5~mumps+boost~suite-sparse~tpetra~ifpack2~zoltan2~amesos2~exodus',
               when='@0.3.0')
    depends_on('trilinos@xsdk-0.2.0+hypre+superlu-dist+metis+hdf5~mumps+boost~suite-sparse~tpetra~ifpack2~zoltan2~amesos2~exodus',
               when='@xsdk-0.2.0')

    depends_on('petsc@develop+trilinos+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64',
               when='@develop')
    depends_on('petsc@3.8.2+trilinos+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64',
               when='@0.3.0')
    depends_on('petsc@xsdk-0.2.0+trilinos+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64',
               when='@xsdk-0.2.0')

    depends_on('dealii@develop~assimp~python~doc~slepc~gmsh+petsc+mpi+trilinos~int64+hdf5~netcdf+metis', when='@develop')

    depends_on('pflotran@develop', when='@develop')
    depends_on('pflotran@xsdk-0.3.0', when='@0.3.0')
    depends_on('pflotran@xsdk-0.2.0', when='@xsdk-0.2.0')

    depends_on('alquimia@develop', when='@develop')
    depends_on('alquimia@xsdk-0.3.0', when='@0.3.0')
    depends_on('alquimia@xsdk-0.2.0', when='@xsdk-0.2.0')

    depends_on('sundials@3.1.0~int64+hypre', when='@develop')
    depends_on('sundials@3.1.0~int64+hypre', when='@0.3.0')

    depends_on('plasma@17.2:', when='@develop %gcc@6.0:')

    depends_on('magma@2.2.0', when='@develop +cuda')
    depends_on('magma@2.2.0', when='@0.3.0 +cuda')

    depends_on('amrex@develop', when='@develop %intel')
    depends_on('amrex@develop', when='@develop %gcc')

    depends_on('slepc@develop', when='@develop')

    # xSDKTrilinos depends on the version of Trilinos built with
    # +tpetra which is turned off for faster xSDK
    # depends_on('xsdktrilinos@xsdk-0.2.0', when='@xsdk-0.2.0')
    # depends_on('xsdktrilinos@develop', when='@develop')

    # How do we propagate debug flag to all depends on packages ?
    # If I just do spack install xsdk+debug will that propogate it down?

    # Dummy install for now,  will be removed when metapackage is available
    def install(self, spec, prefix):
        # Prevent the error message
        #      ==> Error: Install failed for xsdk.  Nothing was installed!
        #      ==> Error: Installation process had nonzero exit code : 256
        with open(os.path.join(spec.prefix, 'bundle-package.txt'), 'w') as out:
            out.write('This is a bundle\n')
            out.close()
