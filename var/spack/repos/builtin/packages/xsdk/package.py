# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack import *
from copy import deepcopy


def depends_on_cuda(cuda_var, *args, **kwargs):
    # require ~cuda when xsdk~cuda
    if not isinstance(cuda_var, list):
        cuda_var = [cuda_var]
    args_new = list(deepcopy(args))
    for idx, var in enumerate(cuda_var):
        # skip variants starting with '?' so that
        # that that they are left unspecified by xsdk
        if not var.startswith('?'):
            args_new[0] += ' ~%s' % var
        else:
            cuda_var[idx] = var.replace('?', '')
    kwargs_new = deepcopy(kwargs)
    if 'when' in kwargs_new:
        kwargs_new['when'] += ' ~cuda'
    else:
        kwargs_new['when'] = '~cuda'
    depends_on(*args_new, **kwargs_new)

    # require +cuda when xsdk+cuda, and match the arch
    for arch in CudaPackage.cuda_arch_values:
        args_new = list(deepcopy(args))
        kwargs_new = deepcopy(kwargs)
        args_new[0] += '+%s cuda_arch=%s' % ('+'.join(cuda_var), arch)
        if 'when' in kwargs_new:
            kwargs_new['when'] += ' +cuda cuda_arch=%s' % arch
        else:
            kwargs_new['when'] = '+cuda cuda_arch=%s' % arch
        depends_on(*args_new, **kwargs_new)


def depends_on_rocm(rocm_var, *args, **kwargs):
    # require ~rocm when xsdk~rocm
    args_new = list(deepcopy(args))
    if not isinstance(rocm_var, list):
        rocm_var = [rocm_var]
    for idx, var in enumerate(rocm_var):
        # skip variants starting with '?' so that
        # that that they are left unspecified by xsdk
        if not var.startswith('?'):
            args_new[0] += ' ~%s' % var
        else:
            rocm_var[idx] = var.replace('?', '')
    kwargs_new = deepcopy(kwargs)
    if 'when' in kwargs_new:
        kwargs_new['when'] += ' ~rocm'
    else:
        kwargs_new['when'] = '~rocm'
    depends_on(*args_new, **kwargs_new)

    # require +rocm when xsdk+rocm, and match the target
    for tgt in ROCmPackage.amdgpu_targets:
        args_new = list(deepcopy(args))
        kwargs_new = deepcopy(kwargs)
        args_new[0] += ' +%s amdgpu_target=%s' % ('+'.join(rocm_var), tgt)
        if 'when' in kwargs_new:
            kwargs_new['when'] += ' +rocm amdgpu_target=%s' % tgt
        else:
            kwargs_new['when'] = '+rocm amdgpu_target=%s' % tgt
        depends_on(*args_new, **kwargs_new)


class Xsdk(BundlePackage, CudaPackage, ROCmPackage):
    """Xsdk is a suite of Department of Energy (DOE) packages for numerical
       simulation. This is a Spack bundle package that installs the xSDK
       packages
    """

    homepage = "https://xsdk.info"
    maintainers = ['balay', 'luszczek', 'balos1']

    def xsdk_depends_on(*args, cuda_var='', rocm_var='', **kwargs):
        """
        Wrapper for depends_on which can handle propagating cuda and rocm
        variants.

        Currently, it propagates +cuda_var when xsdk+cuda and rocm_var
        when xsdk+rocm. When xsdk~[cuda|rocm], then ~[cuda|rocm]_var is
        selected unless the variant string is prefixed with a '?'
        (see the tasmanian use below). When '?' prefix is used, then
        the variant is left unspecified.

        [cuda|rocm]_var can be an array of variant strings or just a single
        variant string. The spack '+' and '~' symbols should not appear
        in the strings.
        """
        if bool(cuda_var):
            depends_on_cuda(cuda_var, *args, **kwargs)
        if bool(rocm_var):
            depends_on_rocm(rocm_var, *args, **kwargs)
        else:
            depends_on(*args, **kwargs)

    version('develop')
    version('0.7.0')
    version('0.6.0')
    version('0.5.0')
    version('0.4.0', deprecated=True)
    version('0.3.0', deprecated=True)

    variant('debug', default=False, description='Compile in debug mode')
    variant('trilinos', default=True, description='Enable trilinos package build')
    variant('datatransferkit', default=True, description='Enable datatransferkit package build')
    variant('omega-h', default=True, description='Enable omega-h package build')
    variant('strumpack', default=True, description='Enable strumpack package build')
    variant('dealii', default=True, description='Enable dealii package build')
    variant('alquimia', default=True, description='Enable alquimia package build')
    variant('phist', default=True, description='Enable phist package build')
    variant('ginkgo', default=True, description='Enable ginkgo package build')
    variant('libensemble', default=True, description='Enable py-libensemble package build')
    variant('precice', default=(sys.platform != 'darwin'),
            description='Enable precice package build')
    variant('butterflypack', default=True, description='Enable butterflypack package build')
    variant('heffte', default=True, description='Enable heffte package build')
    variant('slate', default=True, description='Enable slate package build')
    variant('arborx', default=True, description='Enable ArborX build')

    xsdk_depends_on('hypre@develop+superlu-dist+shared', when='@develop')
    xsdk_depends_on('hypre@2.23.0+superlu-dist+shared', when='@0.7.0')
    xsdk_depends_on('hypre@2.20.0+superlu-dist+shared', when='@0.6.0')
    xsdk_depends_on('hypre@2.18.2+superlu-dist+shared', when='@0.5.0')
    xsdk_depends_on('hypre@2.15.1~internal-superlu', when='@0.4.0')
    xsdk_depends_on('hypre@2.12.1~internal-superlu', when='@0.3.0')

    xsdk_depends_on('mfem@develop+mpi+superlu-dist+petsc+sundials+examples+miniapps', when='@develop', cuda_var='cuda', rocm_var='rocm')
    xsdk_depends_on('mfem@4.3.0+mpi+superlu-dist+petsc+sundials+examples+miniapps', when='@0.7.0', cuda_var='cuda', rocm_var='rocm')
    xsdk_depends_on('mfem@4.2.0+mpi+superlu-dist+petsc+sundials+examples+miniapps', when='@0.6.0', cuda_var='cuda')
    xsdk_depends_on('mfem@4.0.1-xsdk+mpi~superlu-dist+petsc+sundials+examples+miniapps', when='@0.5.0')
    xsdk_depends_on('mfem@3.4.0+mpi+superlu-dist+petsc+sundials+examples+miniapps', when='@0.4.0')
    xsdk_depends_on('mfem@3.3.2+mpi+superlu-dist+petsc+sundials+examples+miniapps', when='@0.3.0')

    xsdk_depends_on('superlu-dist@develop', when='@develop')
    xsdk_depends_on('superlu-dist@7.1.1', when='@0.7.0')
    xsdk_depends_on('superlu-dist@6.4.0', when='@0.6.0')
    xsdk_depends_on('superlu-dist@6.1.1', when='@0.5.0')
    xsdk_depends_on('superlu-dist@6.1.0', when='@0.4.0')
    xsdk_depends_on('superlu-dist@5.2.2', when='@0.3.0')

    xsdk_depends_on('trilinos@develop+hypre+superlu-dist+hdf5~mumps+boost~suite-sparse+tpetra+nox+ifpack2+zoltan+zoltan2+amesos2~exodus~dtk+intrepid2+shards+stratimikos gotype=int cxxstd=14',
                    when='@develop +trilinos')
    xsdk_depends_on('trilinos@13.2.0+hypre+superlu-dist+hdf5~mumps+boost~suite-sparse+tpetra+nox+ifpack2+zoltan+zoltan2+amesos2~exodus~dtk+intrepid2+shards+stratimikos gotype=int cxxstd=14',
                    when='@0.7.0 +trilinos')
    xsdk_depends_on('trilinos@13.0.1+hypre+superlu-dist+hdf5~mumps+boost~suite-sparse+tpetra+nox+ifpack2+zoltan+zoltan2+amesos2~exodus~dtk+intrepid2+shards gotype=int',
                    when='@0.6.0 +trilinos')
    xsdk_depends_on('trilinos@12.18.1+hypre+superlu-dist+hdf5~mumps+boost~suite-sparse+tpetra+nox+ifpack2+zoltan+zoltan2+amesos2~exodus+dtk+intrepid2+shards',
                    when='@0.5.0 +trilinos')
    xsdk_depends_on('trilinos@12.14.1+hypre+superlu-dist+hdf5~mumps+boost~suite-sparse+tpetra+nox+ifpack2+zoltan+zoltan2+amesos2~exodus+dtk+intrepid2+shards',
                    when='@0.4.0 +trilinos')
    xsdk_depends_on('trilinos@12.12.1+hypre+superlu-dist+hdf5~mumps+boost~suite-sparse~tpetra~ifpack2~zoltan~zoltan2~amesos2~exodus',
                    when='@0.3.0 +trilinos')

    xsdk_depends_on('datatransferkit@master', when='@develop +trilinos +datatransferkit')
    dtk7ver = '3.1-rc2' if sys.platform == 'darwin' else '3.1-rc3'
    xsdk_depends_on('datatransferkit@'+dtk7ver, when='@0.7.0 +trilinos +datatransferkit')
    xsdk_depends_on('datatransferkit@3.1-rc2', when='@0.6.0 +trilinos +datatransferkit')

    xsdk_depends_on('petsc +trilinos', when='+trilinos @:0.6.0')
    xsdk_depends_on('petsc +batch', when='platform=cray @0.5.0:')
    xsdk_depends_on('petsc@main+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64',
                    when='@develop', cuda_var='cuda')
    xsdk_depends_on('petsc@3.16.0+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64',
                    when='@0.7.0', cuda_var='cuda')
    xsdk_depends_on('petsc@3.14.1+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64',
                    when='@0.6.0', cuda_var='cuda')
    xsdk_depends_on('petsc@3.12.1+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64',
                    when='@0.5.0')
    xsdk_depends_on('petsc@3.10.3+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64',
                    when='@0.4.0')
    xsdk_depends_on('petsc@3.8.2+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64',
                    when='@0.3.0')

    xsdk_depends_on('dealii +trilinos~adol-c', when='+trilinos +dealii')
    xsdk_depends_on('dealii ~trilinos', when='~trilinos +dealii')
    xsdk_depends_on('dealii@master~assimp~python~doc~gmsh+petsc+slepc+mpi~int64+hdf5~netcdf+metis~sundials~ginkgo~symengine~nanoflann~simplex~arborx', when='@develop +dealii')
    xsdk_depends_on('dealii@9.3.2~assimp~python~doc~gmsh+petsc+slepc+mpi~int64+hdf5~netcdf+metis~sundials~ginkgo~symengine~simplex~arborx', when='@0.7.0 +dealii')
    xsdk_depends_on('dealii@9.2.0~assimp~python~doc~gmsh+petsc+slepc+mpi~int64+hdf5~netcdf+metis~sundials~ginkgo~symengine~simplex~arborx', when='@0.6.0 +dealii')
    xsdk_depends_on('dealii@9.1.1~assimp~python~doc~gmsh+petsc+slepc+mpi~int64+hdf5~netcdf+metis~sundials~ginkgo~symengine', when='@0.5.0 +dealii')
    xsdk_depends_on('dealii@9.0.1~assimp~python~doc~gmsh+petsc~slepc+mpi~int64+hdf5~netcdf+metis~ginkgo~symengine', when='@0.4.0 +dealii')

    xsdk_depends_on('pflotran@develop', when='@develop')
    xsdk_depends_on('pflotran@3.0.2', when='@0.7.0')
    xsdk_depends_on('pflotran@xsdk-0.6.0', when='@0.6.0')
    xsdk_depends_on('pflotran@xsdk-0.5.0', when='@0.5.0')
    xsdk_depends_on('pflotran@xsdk-0.4.0', when='@0.4.0')
    xsdk_depends_on('pflotran@xsdk-0.3.0', when='@0.3.0')

    xsdk_depends_on('alquimia@develop', when='@develop +alquimia')
    xsdk_depends_on('alquimia@1.0.9', when='@0.7.0 +alquimia')
    xsdk_depends_on('alquimia@xsdk-0.6.0', when='@0.6.0 +alquimia')
    xsdk_depends_on('alquimia@xsdk-0.5.0', when='@0.5.0 +alquimia ')
    xsdk_depends_on('alquimia@xsdk-0.4.0', when='@0.4.0 +alquimia')
    xsdk_depends_on('alquimia@xsdk-0.3.0', when='@0.3.0 +alquimia')

    xsdk_depends_on('sundials +trilinos', when='+trilinos @0.6.0:')
    xsdk_depends_on('sundials@develop~int64+hypre+petsc+superlu-dist', when='@develop', cuda_var='cuda', rocm_var='rocm')
    xsdk_depends_on('sundials@5.8.0~int64+hypre+petsc+superlu-dist', when='@0.7.0', cuda_var='cuda', rocm_var='rocm')
    xsdk_depends_on('sundials@5.5.0~int64+hypre+petsc+superlu-dist', when='@0.6.0', cuda_var='cuda')
    xsdk_depends_on('sundials@5.0.0~int64+hypre+petsc+superlu-dist', when='@0.5.0')
    xsdk_depends_on('sundials@3.2.1~int64+hypre', when='@0.4.0')
    xsdk_depends_on('sundials@3.1.0~int64+hypre', when='@0.3.0')

    xsdk_depends_on('plasma@develop:', when='@develop %gcc@6.0:')
    xsdk_depends_on('plasma@21.8.29:', when='@0.7.0 %gcc@6.0:')
    xsdk_depends_on('plasma@20.9.20:', when='@0.6.0 %gcc@6.0:')
    xsdk_depends_on('plasma@19.8.1:', when='@0.5.0 %gcc@6.0:')
    xsdk_depends_on('plasma@18.11.1:', when='@0.4.0 %gcc@6.0:')

    xsdk_depends_on('magma@master', when='@develop', cuda_var='cuda', rocm_var='rocm')
    xsdk_depends_on('magma@2.6.1', when='@0.7.0', cuda_var='cuda', rocm_var='rocm')
    xsdk_depends_on('magma@2.5.4', when='@0.6.0', cuda_var='cuda')
    xsdk_depends_on('magma@2.5.1', when='@0.5.0', cuda_var='cuda')
    xsdk_depends_on('magma@2.4.0', when='@0.4.0', cuda_var='cuda')
    xsdk_depends_on('magma@2.2.0', when='@0.3.0', cuda_var='cuda')

    xsdk_depends_on('amrex@develop+sundials', when='@develop %intel', cuda_var='cuda', rocm_var='rocm')
    xsdk_depends_on('amrex@develop+sundials', when='@develop %gcc', cuda_var='cuda', rocm_var='rocm')
    xsdk_depends_on('amrex@develop+sundials', when='@develop %cce', cuda_var='cuda', rocm_var='rocm')
    xsdk_depends_on('amrex@21.10+sundials', when='@0.7.0 %intel', cuda_var='cuda', rocm_var='rocm')
    xsdk_depends_on('amrex@21.10+sundials', when='@0.7.0 %gcc', cuda_var='cuda', rocm_var='rocm')
    xsdk_depends_on('amrex@21.10+sundials', when='@0.7.0 %cce', cuda_var='cuda', rocm_var='rocm')
    xsdk_depends_on('amrex@20.10', when='@0.6.0 %intel')
    xsdk_depends_on('amrex@20.10', when='@0.6.0 %gcc')
    xsdk_depends_on('amrex@19.08', when='@0.5.0 %intel')
    xsdk_depends_on('amrex@19.08', when='@0.5.0 %gcc')
    xsdk_depends_on('amrex@18.10.1', when='@0.4.0 %intel')
    xsdk_depends_on('amrex@18.10.1', when='@0.4.0 %gcc')

    xsdk_depends_on('slepc@main', when='@develop')
    xsdk_depends_on('slepc@3.16.0', when='@0.7.0')
    xsdk_depends_on('slepc@3.14.0', when='@0.6.0')
    xsdk_depends_on('slepc@3.12.0', when='@0.5.0')
    xsdk_depends_on('slepc@3.10.1', when='@0.4.0')

    xsdk_depends_on('omega-h +trilinos', when='+trilinos +omega-h')
    xsdk_depends_on('omega-h ~trilinos', when='~trilinos +omega-h')
    xsdk_depends_on('omega-h@main', when='@develop +omega-h')
    xsdk_depends_on('omega-h@9.34.1', when='@0.7.0 +omega-h')
    xsdk_depends_on('omega-h@9.32.5', when='@0.6.0 +omega-h')
    xsdk_depends_on('omega-h@9.29.0', when='@0.5.0 +omega-h')
    xsdk_depends_on('omega-h@9.19.1', when='@0.4.0 +omega-h')

    xsdk_depends_on('strumpack ~cuda', when='~cuda @0.6.0: +strumpack')
    xsdk_depends_on('strumpack@master~slate~openmp', when='@develop +strumpack')
    xsdk_depends_on('strumpack@6.0.0~slate~openmp', when='@0.7.0 +strumpack')
    xsdk_depends_on('strumpack@5.0.0~slate~openmp', when='@0.6.0 +strumpack')
    xsdk_depends_on('strumpack@3.3.0~slate~openmp', when='@0.5.0 +strumpack')
    xsdk_depends_on('strumpack@3.1.1~slate~openmp', when='@0.4.0 +strumpack')

    xsdk_depends_on('pumi@master', when='@develop')
    xsdk_depends_on('pumi@2.2.6', when='@0.7.0')
    xsdk_depends_on('pumi@2.2.5', when='@0.6.0')
    xsdk_depends_on('pumi@2.2.1', when='@0.5.0')
    xsdk_depends_on('pumi@2.2.0', when='@0.4.0')

    tasmanian_openmp = '~openmp' if sys.platform == 'darwin' else '+openmp'
    xsdk_depends_on('tasmanian@develop+xsdkflags+blas' + tasmanian_openmp, when='@develop', cuda_var=['cuda', '?magma'], rocm_var=['rocm', '?magma'])
    xsdk_depends_on('tasmanian@7.7+xsdkflags+mpi+blas' + tasmanian_openmp, when='@0.7.0', cuda_var=['cuda', '?magma'])
    #xsdk_depends_on('tasmanian@7.7+xsdkflags+mpi+blas' + tasmanian_openmp, when='@0.7.0', cuda_var=['cuda', '?magma'], rocm_var=['rocm', '?magma']) # TODO: not sure why this causes a conflict
    xsdk_depends_on('tasmanian@7.3+xsdkflags+mpi+blas' + tasmanian_openmp, when='@0.6.0', cuda_var=['cuda', '?magma'])
    xsdk_depends_on('tasmanian@7.0+xsdkflags+mpi+blas' + tasmanian_openmp, when='@0.5.0', cuda_var=['cuda', '?magma'])
    xsdk_depends_on('tasmanian@6.0+xsdkflags+blas~openmp', when='@0.4.0', cuda_var=['cuda', '?magma'])

    xsdk_depends_on('arborx@master', when='@develop +arborx')
    xsdk_depends_on('arborx@1.1', when='@0.7.0 +arborx')

    # the Fortran 2003 bindings of phist require python@3:, but this
    # creates a conflict with other packages like petsc@main. Actually
    # these are type='build' dependencies, but spack reports a conflict anyway.
    # This will be fixed once the new concretizer becomes available
    # (says @adamjstewart)

    xsdk_depends_on('phist kernel_lib=tpetra', when='+trilinos +phist')
    xsdk_depends_on('phist kernel_lib=petsc', when='~trilinos +phist')
    xsdk_depends_on('phist@develop ~fortran ~scamac ~openmp ~host ~int64', when='@develop +phist')
    xsdk_depends_on('phist@1.9.5 ~fortran ~scamac ~openmp ~host ~int64', when='@0.7.0 +phist')
    xsdk_depends_on('phist@1.9.3 ~fortran ~scamac ~openmp ~host ~int64', when='@0.6.0 +phist')
    xsdk_depends_on('phist@1.8.0 ~fortran ~scamac ~openmp ~host ~int64', when='@0.5.0 +phist')
    xsdk_depends_on('phist@1.7.5 ~fortran ~scamac ~openmp ~host ~int64', when='@0.4.0 +phist')

    xsdk_depends_on('ginkgo@develop ~openmp', when='@develop +ginkgo', cuda_var='cuda', rocm_var='rocm')
    xsdk_depends_on('ginkgo@1.4.0 ~openmp', when='@0.7.0 +ginkgo', cuda_var='cuda', rocm_var='rocm')
    xsdk_depends_on('ginkgo@1.3.0 ~openmp', when='@0.6.0 +ginkgo', cuda_var='cuda')
    xsdk_depends_on('ginkgo@1.1.0 ~openmp', when='@0.5.0 +ginkgo')

    xsdk_depends_on('py-libensemble@develop+petsc4py', type='run', when='@develop +libensemble')
    xsdk_depends_on('py-petsc4py@main', type='run', when='@develop +libensemble')
    xsdk_depends_on('py-libensemble@0.8.0+petsc4py', type='run', when='@0.7.0 +libensemble')
    xsdk_depends_on('py-petsc4py@3.16.0', type='run', when='@0.7.0 +libensemble')
    xsdk_depends_on('py-libensemble@0.7.1+petsc4py', type='run', when='@0.6.0 +libensemble')
    xsdk_depends_on('py-petsc4py@3.14.0', type='run', when='@0.6.0 +libensemble')
    xsdk_depends_on('py-libensemble@0.5.2+petsc4py', type='run', when='@0.5.0 +libensemble')
    xsdk_depends_on('py-petsc4py@3.12.0', type='run', when='@0.5.0 +libensemble')

    xsdk_depends_on('precice ~petsc', when='platform=cray +precice')
    xsdk_depends_on('precice@develop', when='@develop +precice')
    xsdk_depends_on('precice@2.3.0', when='@0.7.0 +precice')
    xsdk_depends_on('precice@2.1.1', when='@0.6.0 +precice')
    xsdk_depends_on('precice@1.6.1', when='@0.5.0 +precice')

    xsdk_depends_on('butterflypack@master', when='@develop +butterflypack')
    xsdk_depends_on('butterflypack@2.0.0', when='@0.7.0 +butterflypack')
    xsdk_depends_on('butterflypack@1.2.1', when='@0.6.0 +butterflypack')
    xsdk_depends_on('butterflypack@1.1.0', when='@0.5.0 +butterflypack')

    xsdk_depends_on('heffte@develop+fftw', when='@develop +heffte', cuda_var=['cuda', '?magma'], rocm_var=['rocm', '?magma'])
    xsdk_depends_on('heffte@2.2.0+fftw', when='@0.7.0 +heffte', cuda_var=['cuda', '?magma'], rocm_var=['rocm', '?magma'])
    xsdk_depends_on('heffte@2.0.0+fftw', when='@0.6.0 +heffte', cuda_var=['cuda', '?magma'])
    xsdk_depends_on('openmpi+cuda', when='+cuda +heffte') # openmpi does not use CudaPackage and has no cuda_arch variant

    xsdk_depends_on('slate@master', when='@develop +slate %gcc@6.0:', cuda_var='cuda')
    xsdk_depends_on('slate@2021.05.02 ~cuda', when='@0.7.0 ~cuda +slate %gcc@6.0:') # TODO: should this version have +cuda?
    xsdk_depends_on('slate@2020.10.00', when='@0.6.0 +slate %gcc@6.0:', cuda_var='cuda')

    # How do we propagate debug flag to all depends on packages ?
    # If I just do spack install xsdk+debug will that propogate it down?
