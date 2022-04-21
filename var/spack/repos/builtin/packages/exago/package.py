# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Exago(CMakePackage, CudaPackage, ROCmPackage):
    """ExaGO is a package for solving large-scale power grid optimization
    problems on parallel and distributed architectures, particularly targeted
    for exascale machines."""

    homepage = 'https://gitlab.pnnl.gov/exasgd/frameworks/exago'
    git = 'https://gitlab.pnnl.gov/exasgd/frameworks/exago.git'
    maintainers = ['ashermancinelli', 'CameronRutherford']

    version('1.4.1', commit='ea607c685444b5f345bfdc9a59c345f0f30adde2', submodules=True, preferred=True)
    version('1.4.0', commit='4f4c3fdb40b52ace2d6ba000e7f24b340ec8e886', submodules=True)
    version('1.3.0', commit='58b039d746a6eac8e84b0afc01354cd58caec485', submodules=True)
    version('1.2.0', commit='255a214e', submodules=True)
    version('1.1.2', commit='db3bb16e', submodules=True)
    version('1.1.1', commit='0e0a3f27', submodules=True)
    version('1.1.0', commit='dc8dd855', submodules=True)
    version('1.0.0', commit='230d7df2')
    version('0.99.2', commit='56961641')
    version('0.99.1', commit='0ae426c7')
    version('master', branch='master')
    version('develop', branch='develop', submodules=True)

    # Progrmming model options
    variant('mpi', default=True, description='Enable/Disable MPI')
    variant('raja', default=False, description='Enable/Disable RAJA')
    variant('python', default=True, description='Enable/Disable Python bindings')
    conflicts('+python', when='@:1.3.0', msg='Python bindings require ExaGO 1.4')

    # Solver options
    variant('hiop', default=False, description='Enable/Disable HiOp')
    variant('ipopt', default=False, description='Enable/Disable IPOPT')

    conflicts('~hiop~ipopt', msg="ExaGO needs at least one solver enabled")

    # Dependencides
    depends_on('mpi', when='+mpi')
    depends_on('blas')
    depends_on('cuda', when='+cuda')
    depends_on('raja', when='+raja')

    depends_on('raja+cuda', when='+raja+cuda')
    depends_on('raja+rocm', when='+raja+rocm')
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
    depends_on('hiop@0.5.3:', when='@1.3.0:+hiop')

    depends_on('hiop+cuda', when='+hiop+cuda')
    depends_on('hiop+rocm', when='+hiop+rocm')
    depends_on('hiop~mpi', when='+hiop~mpi')
    depends_on('hiop+mpi', when='+hiop+mpi')

    depends_on('petsc@3.13:3.14', when='@:1.2.99')
    depends_on('petsc@3.16.0:', when='@1.3.0:')
    depends_on('petsc~mpi', when='~mpi')

    depends_on('ipopt', when='+ipopt')

    depends_on('py-mpi4py', when='@1.3.0:+mpi+python')

    flag_handler = build_system_flags

    def cmake_args(self):
        args = []
        spec = self.spec

        # NOTE: If building with spack develop on a cluster, you may want to
        # change the ctest launch command to use your job scheduler like so:
        #
        # args.append(
        #     self.define('EXAGO_CTEST_LAUNCH_COMMAND', 'srun -t 10:00'))

        args.extend([
            self.define('EXAGO_ENABLE_GPU', '+cuda' in spec or '+rocm' in spec),
            self.define_from_variant('EXAGO_ENABLE_CUDA', 'cuda'),
            self.define_from_variant('EXAGO_ENABLE_HIP', 'rocm'),
            self.define('PETSC_DIR', spec['petsc'].prefix),
            self.define('EXAGO_RUN_TESTS', True),
            self.define_from_variant('EXAGO_ENABLE_MPI', 'mpi'),
            self.define_from_variant('EXAGO_ENABLE_RAJA', 'raja'),
            self.define_from_variant('EXAGO_ENABLE_HIOP', 'hiop'),
            self.define_from_variant('EXAGO_ENABLE_IPOPT', 'ipopt'),
            self.define_from_variant('EXAGO_ENABLE_PYTHON', 'python'),
        ])

        if '+cuda' in spec:
            cuda_arch_list = spec.variants['cuda_arch'].value
            if cuda_arch_list[0] != 'none':
                args.append(
                    self.define('CMAKE_CUDA_ARCHITECTURES', cuda_arch_list))

        # NOTE: if +rocm, some HIP CMake variables may not be set correctly.
        # Namely, HIP_CLANG_INCLUDE_PATH. If the configure phase fails due to
        # this variable being undefined, adding the following line typically
        # resolves this issue:
        #
        # args.append(
        #     self.define('HIP_CLANG_INCLUDE_PATH',
        #         '/opt/rocm-X.Y.Z/llvm/lib/clang/14.0.0/include/'))
        if '+rocm' in spec:
            args.append(self.define('CMAKE_CXX_COMPILER', spec['hip'].hipcc))

            rocm_arch_list = spec.variants['amdgpu_target'].value
            if rocm_arch_list[0] != 'none':
                args.append(self.define('GPU_TARGETS', rocm_arch_list))
                args.append(self.define('AMDGPU_TARGETS', rocm_arch_list))

        return args
