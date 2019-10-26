# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Xsdk(BundlePackage):
    """Xsdk is a suite of Department of Energy (DOE) packages for numerical
       simulation. This is a Spack bundle package that installs the xSDK
       packages
    """

    homepage = "http://xsdk.info"

    maintainers = ['balay', 'luszczek']

    version('develop')
    version('0.4.0')
    version('0.3.0')
    version('xsdk-0.2.0')

    variant('debug', default=False, description='Compile in debug mode')
    variant('cuda', default=False, description='Enable CUDA dependent packages')
    variant('omega-h', default=True, description='Enable omega-h package build')
    variant('dealii', default=True, description='Enable dealii package build')
    variant('phist', default=True, description='Enable phist package build')

    depends_on('hypre@develop~internal-superlu+superlu-dist+shared', when='@develop')
    depends_on('hypre@2.15.1~internal-superlu', when='@0.4.0')
    depends_on('hypre@2.12.1~internal-superlu', when='@0.3.0')
    depends_on('hypre@xsdk-0.2.0~internal-superlu', when='@xsdk-0.2.0')

    depends_on('mfem@develop+mpi+hypre+superlu-dist+petsc~sundials+examples+miniapps', when='@develop')
    depends_on('mfem@3.4.0+mpi+hypre+superlu-dist+petsc+sundials+examples+miniapps', when='@0.4.0')
    depends_on('mfem@3.3.2+mpi+hypre+superlu-dist+petsc+sundials+examples+miniapps', when='@0.3.0')

    depends_on('superlu-dist@develop', when='@develop')
    depends_on('superlu-dist@6.1.0', when='@0.4.0')
    depends_on('superlu-dist@5.2.2', when='@0.3.0')
    depends_on('superlu-dist@xsdk-0.2.0', when='@xsdk-0.2.0')

    depends_on('trilinos@develop+hypre+superlu-dist+metis+hdf5~mumps+boost~suite-sparse+tpetra+nox+ifpack2+zoltan2+amesos2~exodus+dtk+intrepid2+shards',
               when='@develop')
    depends_on('trilinos@12.14.1+hypre+superlu-dist+metis+hdf5~mumps+boost~suite-sparse+tpetra+nox+ifpack2+zoltan2+amesos2~exodus+dtk+intrepid2+shards',
               when='@0.4.0')
    depends_on('trilinos@12.12.1+hypre+superlu-dist+metis+hdf5~mumps+boost~suite-sparse~tpetra~ifpack2~zoltan2~amesos2~exodus',
               when='@0.3.0')
    depends_on('trilinos@xsdk-0.2.0+hypre+superlu-dist+metis+hdf5~mumps+boost~suite-sparse~tpetra~ifpack2~zoltan2~amesos2~exodus',
               when='@xsdk-0.2.0')

    depends_on('petsc@develop+trilinos+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64',
               when='@develop')
    depends_on('petsc@3.10.3+trilinos+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64',
               when='@0.4.0')
    depends_on('petsc@3.8.2+trilinos+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64',
               when='@0.3.0')
    depends_on('petsc@xsdk-0.2.0+trilinos+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64',
               when='@xsdk-0.2.0')

    depends_on('dealii@develop~assimp~python~doc~gmsh+petsc+slepc+mpi+trilinos~int64+hdf5~netcdf+metis~sundials~ginkgo~symengine', when='@develop +dealii')
    depends_on('dealii@9.0.1~assimp~python~doc~gmsh+petsc~slepc+mpi+trilinos~int64+hdf5~netcdf+metis~ginkgo~symengine', when='@0.4.0 +dealii')

    depends_on('pflotran@develop', when='@develop')
    depends_on('pflotran@xsdk-0.4.0', when='@0.4.0')
    depends_on('pflotran@xsdk-0.3.0', when='@0.3.0')
    depends_on('pflotran@xsdk-0.2.0', when='@xsdk-0.2.0')

    depends_on('alquimia@develop', when='@develop')
    depends_on('alquimia@xsdk-0.4.0', when='@0.4.0')
    depends_on('alquimia@xsdk-0.3.0', when='@0.3.0')
    depends_on('alquimia@xsdk-0.2.0', when='@xsdk-0.2.0')

    depends_on('sundials@4.1.0~int64+hypre', when='@develop')
    depends_on('sundials@3.2.1~int64+hypre', when='@0.4.0')
    depends_on('sundials@3.1.0~int64+hypre', when='@0.3.0')

    depends_on('plasma@18.11.1:', when='@develop %gcc@6.0:')
    depends_on('plasma@18.11.1:', when='@0.4.0 %gcc@6.0:')

    depends_on('magma@2.4.0', when='@develop +cuda')
    depends_on('magma@2.4.0', when='@0.4.0 +cuda')
    depends_on('magma@2.2.0', when='@0.3.0 +cuda')

    depends_on('amrex@develop+sundials', when='@develop %intel')
    depends_on('amrex@develop+sundials', when='@develop %gcc')
    depends_on('amrex@18.10.1', when='@0.4.0 %intel')
    depends_on('amrex@18.10.1', when='@0.4.0 %gcc')

    depends_on('slepc@develop', when='@develop')
    depends_on('slepc@3.10.1', when='@0.4.0')

    depends_on('omega-h@develop', when='@develop +omega-h')
    depends_on('omega-h@9.19.1', when='@0.4.0 +omega-h')

    depends_on('strumpack@master', when='@develop')
    depends_on('strumpack@3.1.1', when='@0.4.0')

    depends_on('pumi@develop', when='@develop')
    depends_on('pumi@2.2.0', when='@0.4.0')

    depends_on('tasmanian@develop+xsdkflags+blas~openmp', when='@develop')
    depends_on('tasmanian@develop+xsdkflags+blas+cuda+magma~openmp', when='@develop +cuda')
    depends_on('tasmanian@6.0+xsdkflags+blas~openmp', when='@0.4.0')
    depends_on('tasmanian@6.0+xsdkflags+blas+cuda+magma~openmp', when='@0.4.0 +cuda')

    # the Fortran 2003 bindings of phist require python@3:, but this
    # creates a conflict with other packages like petsc@develop. Actually
    # these are type='build' dependencies, but spack reports a conflict anyway.
    # This will be fixed once the new concretizer becomes available
    # (says @adamjstewart)
    depends_on('phist@develop kernel_lib=tpetra ~fortran ~scamac ~openmp ~host', when='@develop +phist')
    depends_on('phist@1.7.5 kernel_lib=tpetra ~fortran ~scamac ~openmp ~host', when='@0.4.0 +phist')

    # xSDKTrilinos depends on the version of Trilinos built with
    # +tpetra which is turned off for faster xSDK
    # depends_on('xsdktrilinos@xsdk-0.2.0', when='@xsdk-0.2.0')
    # depends_on('xsdktrilinos@develop', when='@develop')

    # How do we propagate debug flag to all depends on packages ?
    # If I just do spack install xsdk+debug will that propogate it down?
