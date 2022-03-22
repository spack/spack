# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hiop(CMakePackage, CudaPackage, ROCmPackage):
    """HiOp is an optimization solver for solving certain mathematical
    optimization problems expressed as nonlinear programming problems.
    HiOp is a lightweight HPC solver that leverages application"s existing
    data parallelism to parallelize the optimization iterations by using
    specialized linear algebra kernels."""

    homepage = 'https://github.com/LLNL/hiop'
    git = 'https://github.com/LLNL/hiop.git'
    maintainers = ['ashermancinelli', 'CameronRutherford']

    # Most recent tagged snapshot is the preferred version when profiling.
    version('0.5.4', commit='a37a7a677884e95d1c0ad37936aef3778fc91c3e')
    version('0.5.3', commit='698e8d0fdc0ff9975d8714339ff8c782b70d85f9')
    version('0.5.2', commit='662ad76dee1f501f648a8bec9a490cb5881789e9')
    version('0.5.1', commit='6789bbb55824e68e428c2df1009d647af81f9cf1')
    version('0.5.0', commit='a39da8025037c7c8ae2eb31234eb80cc73bec2af')
    version('0.4.6', commit='b72d163d52c9225c3196ceb2baebdc7cf09a69de')
    version('0.4.5', commit='c353580456c4776c50811b97cf8ff802dc27b90c')
    version('0.4.4', commit='e858eefa6b914f5c87c3717bbce811931ea69386')
    version('0.4.3', commit='c0394af4d84ebb84b7d2b95283ad65ffd84e0d45')
    version('0.4.2', commit='3fcb788d223eec24c0241680070c4a9a5ec71ef3')
    version('0.4.1', commit='3f269560f76d5a89bcbd1d3c4f9f0e5acaa6fd64')
    version('0.4', commit='91d21085a1149eacdb27cd738d4a74a7e412fcff')
    version('0.3.99.3', commit='bed1dbef260e53a9d139ccfb77d2e83a98aab216')
    version('0.3.99.2', commit='9eb026768bc5e0a2c1293d0487cc39913001ae19')
    version('0.3.99.1', commit='220e32c0f318665d6d394ca3cd0735b9d26a65eb')
    version('0.3.99.0', commit='589b9c76781447108fa55788d5fa1b83ff71a3d1')
    version('0.3', commit='7e8adae9db757aed48e5c2bc448316307598258f')
    version('0.2', commit='c52a6f6b9baaaa2d7f233a749aa98f901349723f')
    version('0.1', commit='5f60e11b79d532115fb41694378b54c9c707aad9')

    # Development branches
    version('master', branch='master')
    version('develop', branch='develop')

    variant(
        'jsrun', default=False, description='Enable/Disable jsrun command for testing'
    )
    variant('shared', default=False, description='Enable/Disable shared libraries')
    variant('mpi', default=True, description='Enable/Disable MPI')
    variant('raja', default=False, description='Enable/Disable RAJA')
    variant('kron', default=False, description='Enable/Disable Kron reduction')
    variant('sparse', default=False, description='Enable/Disable Sparse linear algebra')
    variant(
        'deepchecking',
        default=False,
        description='Ultra safety checks - '
        'used for increased robustness and self-diagnostics',
    )

    depends_on('lapack')
    depends_on('blas')
    depends_on('cmake@3.18:', type='build')

    depends_on('mpi', when='+mpi')

    depends_on('magma+cuda', when='+cuda')
    depends_on('magma+rocm', when='+rocm')

    # Depends on Magma when +rocm or +cuda
    magma_ver_constraints = (
        ('2.5.4', '0.4'),
        ('2.6.1', '0.4.6'),
        ('2.6.2', '0.5.4'),
    )
    for (magma_v, hiop_v) in magma_ver_constraints:
        depends_on('magma@{0}:'.format(magma_v), when='@{0}:+cuda'.format(hiop_v))
        depends_on('magma@{0}:'.format(magma_v), when='@{0}:+rocm'.format(hiop_v))

    depends_on('raja+openmp', when='+raja')
    depends_on('raja@0.14.0:', when='@0.5.0:+raja')
    depends_on('raja+cuda', when='+raja+cuda')
    depends_on('raja+rocm', when='+raja+rocm')
    depends_on('umpire', when='+raja')
    depends_on('umpire+cuda~shared', when='+raja+cuda')
    depends_on('umpire+rocm', when='+raja+rocm')
    depends_on('umpire@6.0.0:', when='@0.5.0:+raja')
    depends_on('hip', when='+rocm')
    depends_on('hipblas', when='+rocm')
    depends_on('hipsparse', when='+rocm')

    depends_on('suite-sparse', when='+kron')

    depends_on('coinhsl+blas', when='+sparse')
    depends_on('metis', when='+sparse')

    conflicts(
        '+shared',
        when='+cuda+raja',
        msg='umpire+cuda exports device code and requires static libs',
    )

    flag_handler = build_system_flags

    def cmake_args(self):
        args = []
        spec = self.spec

        if spec.satisfies('+rocm') or spec.satisfies('+cuda'):
            args.append('-DHIOP_USE_GPU=ON')
            args.append('-DHIOP_USE_MAGMA=ON')

        args.extend([
            self.define('HIOP_BUILD_STATIC', True),
            self.define('LAPACK_FOUND', True),
            self.define('LAPACK_LIBRARIES', spec['lapack'].libs + spec['blas'].libs),
            self.define('HIOP_USE_HIP', False),
            self.define_from_variant('HIOP_BUILD_SHARED', 'shared'),
            self.define_from_variant('HIOP_USE_MPI', 'mpi'),
            self.define_from_variant('HIOP_DEEPCHECKS', 'deepchecking'),
            self.define_from_variant('HIOP_USE_CUDA', 'cuda'),
            self.define_from_variant('HIOP_USE_HIP', 'rocm'),
            self.define_from_variant('HIOP_USE_RAJA', 'raja'),
            self.define_from_variant('HIOP_USE_UMPIRE', 'raja'),
            self.define_from_variant('HIOP_WITH_KRON_REDUCTION', 'kron'),
            self.define_from_variant('HIOP_SPARSE', 'sparse'),
            self.define_from_variant('HIOP_USE_COINHSL', 'sparse'),
            self.define_from_variant('HIOP_TEST_WITH_BSUB', 'jsrun'),
        ])

        if '+mpi' in spec:
            args.extend([
                self.define('MPI_HOME', spec['mpi'].prefix),
                self.define('MPI_C_COMPILER', spec['mpi'].mpicc),
                self.define('MPI_CXX_COMPILER', spec['mpi'].mpicxx),
                self.define('MPI_Fortran_COMPILER', spec['mpi'].mpifc),
            ])

        if '+cuda' in spec:
            cuda_arch_list = spec.variants['cuda_arch'].value
            cuda_arch = cuda_arch_list[0]
            if cuda_arch != 'none':
                args.extend([
                    self.define('HIOP_NVCC_ARCH', 'sm_{0}'.format(cuda_arch)),
                    self.define('CMAKE_CUDA_ARCHITECTURES', cuda_arch),
                ])
            if '+magma' in spec:
                args.append(self.define('HIOP_MAGMA_DIR', spec['magma'].prefix))

        if '+kron' in spec:
            args.append(self.define('HIOP_UMFPACK_DIR', spec['suite-sparse'].prefix))

        # Unconditionally disable strumpack, even when +sparse. This may be
        # used in place of COINHSL for sparse interface, however this is not
        # fully supported in spack at the moment.
        args.append(self.define('HIOP_USE_STRUMPACK', False))

        if '+sparse' in spec:
            args.append(self.define('HIOP_COINHSL_DIR', spec['coinhsl'].prefix))

        return args
