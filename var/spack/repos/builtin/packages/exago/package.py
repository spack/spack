# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Exago(CMakePackage, CudaPackage):
    """ExaGO is a package for solving large-scale power grid optimization
    problems on parallel and distributed architectures, particularly targeted
    for exascale machines."""

    homepage = 'https://gitlab.pnnl.gov/exasgd/frameworks/exago'
    git = 'https://gitlab.pnnl.gov/exasgd/frameworks/exago.git'
    maintainers = ['ashermancinelli', 'CameronRutherford']

    version('1.2.0', commit='255a214e', submodules=True)
    version('1.1.2', commit='db3bb16e', submodules=True)
    version('1.1.1', commit='0e0a3f27', submodules=True)
    version('1.1.0', commit='dc8dd855', submodules=True)
    version('1.0.0', commit='230d7df2')
    version('0.99.2', commit='56961641')
    version('0.99.1', commit='0ae426c7')
    version('master', branch='master')
    version('develop', branch='develop')

    # Progrmming model options
    variant('mpi', default=True, description='Enable/Disable MPI')
    variant('raja', default=False, description='Enable/Disable RAJA')

    # Solver options
    variant('hiop', default=False, description='Enable/Disable HiOp')
    variant('ipopt', default=False, description='Enable/Disable IPOPT')

    # Dependencides
    depends_on('mpi', when='+mpi')
    depends_on('blas')
    depends_on('cuda', when='+cuda')

    depends_on('raja', when='+raja')
    depends_on('raja+cuda', when='+raja+cuda')
    depends_on('raja@0.14.0:', when='@1.1.0: +raja')

    depends_on('umpire', when='+raja')
    depends_on('umpire@6.0.0:', when='@1.1.0: +raja')

    # Some allocator code in Umpire only works with static libs
    depends_on('umpire+cuda~shared', when='+raja+cuda')

    # For some versions of RAJA package, camp cuda variant does not get set
    # correctly, so we must explicitly depend on it even though we don't use
    # camp
    depends_on('camp+cuda', when='+raja+cuda')

    depends_on('cmake@3.18:', type='build')

    # HiOp dependency logic
    depends_on('hiop+raja', when='+hiop+raja')
    depends_on('hiop@0.3.99:', when='@0.99:+hiop')
    depends_on('hiop@0.5.1:', when='@1.1.0:+hiop')
    depends_on('hiop+cuda', when='+hiop+cuda')
    depends_on('hiop~mpi', when='+hiop~mpi')
    depends_on('hiop+mpi', when='+hiop+mpi')

    # Require PETSc < 3.15 per ExaGO issue #199
    depends_on('petsc@3.13:3.14')
    depends_on('petsc~mpi', when='~mpi')

    depends_on('ipopt', when='+ipopt')

    flag_handler = build_system_flags

    def cmake_args(self):
        args = []
        spec = self.spec

        args.append("-DEXAGO_RUN_TESTS=ON")

        args.append(self.define_from_variant('EXAGO_ENABLE_MPI', 'mpi'))
        args.append(self.define_from_variant('EXAGO_ENABLE_RAJA', 'raja'))
        args.append(self.define_from_variant('EXAGO_ENABLE_HIOP', 'hiop'))
        args.append(self.define_from_variant('EXAGO_ENABLE_IPOPT', 'ipopt'))
        args.append(self.define_from_variant('EXAGO_ENABLE_GPU', 'cuda'))
        args.append(self.define_from_variant('EXAGO_ENABLE_CUDA', 'cuda'))
        args.append("-DPETSC_DIR='{0}'".format(spec['petsc'].prefix))

        if '+cuda' in spec:
            cuda_arch_list = spec.variants['cuda_arch'].value
            cuda_arch = cuda_arch_list[0]
            if cuda_arch != 'none':
                args.append(
                    "-DCMAKE_CUDA_ARCHITECTURES={0}".format(cuda_arch))

        return args
