# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.util.environment import set_env
from spack.util.executable import which


class Strumpack(CMakePackage, CudaPackage, ROCmPackage):
    """STRUMPACK -- STRUctured Matrix PACKage - provides linear solvers
    for sparse matrices and for dense rank-structured matrices, i.e.,
    matrices that exhibit some kind of low-rank property. It provides a
    distributed memory fully algebraic sparse solver and
    preconditioner. The preconditioner is mostly aimed at large sparse
    linear systems which result from the discretization of a partial
    differential equation, but is not limited to any particular type of
    problem. STRUMPACK also provides preconditioned GMRES and BiCGStab
    iterative solvers."""

    homepage = "http://portal.nersc.gov/project/sparse/strumpack"
    url      = "https://github.com/pghysels/STRUMPACK/archive/refs/tags/v6.0.0.tar.gz"
    git      = "https://github.com/pghysels/STRUMPACK.git"

    tags = ['e4s']

    maintainers = ['pghysels']

    test_requires_compiler = True

    version('master', branch='master')
    version('6.0.0', sha256='fcea150b68172d5a4ec2c02f9cce0b7305919b86871c9cf34a9f65b1567d58b7')
    version('5.1.1', sha256='6cf4eaae5beb9bd377f2abce9e4da9fd3e95bf086ae2f04554fad6dd561c28b9')
    version('5.0.0', sha256='bdfd1620ff7158d96055059be04ee49466ebaca8213a2fdab33e2d4571019a49')
    version('4.0.0', sha256='a3629f1f139865c74916f8f69318f53af6319e7f8ec54e85c16466fd7d256938')
    version('3.3.0', sha256='499fd3b58656b4b6495496920e5372895861ebf15328be8a7a9354e06c734bc7')
    version('3.2.0', sha256='34d93e1b2a3b8908ef89804b7e08c5a884cbbc0b2c9f139061627c0d2de282c1')
    version('3.1.1', sha256='c1c3446ee023f7b24baa97b24907735e89ce4ae9f5ef516645dfe390165d1778')

    variant('shared', default=True, description='Build shared libraries')
    variant('mpi', default=True, description='Use MPI')
    variant('openmp', default=True,
            description='Enable thread parallellism via tasking with OpenMP')
    variant('parmetis', default=True,
            description='Enable use of ParMetis')
    variant('scotch', default=False,
            description='Enable use of Scotch')
    variant('butterflypack', default=True,
            description='Enable use of ButterflyPACK')
    variant('zfp', default=True,
            description='Build with support for compression using ZFP')
    variant('c_interface', default=True,
            description='Enable C interface')
    variant('count_flops', default=False,
            description='Build with flop counters')
    variant('task_timers', default=False,
            description='Build with timers for internal routines')
    variant('build_dev_tests', default=False,
            description='Build developer test routines')
    variant('build_tests', default=False,
            description='Build test routines')
    variant('slate', default=True,
            description="Build with SLATE support")

    depends_on('cmake@3.11:', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('openblas threads=openmp', when='^openblas')
    depends_on('scalapack', when='+mpi')
    depends_on('metis')
    depends_on('parmetis', when='+parmetis')
    depends_on('scotch~metis', when='+scotch')
    depends_on('scotch~metis+mpi', when='+scotch+mpi')
    depends_on('butterflypack@1.1.0', when='@3.3.0:3.9 +butterflypack+mpi')
    depends_on('butterflypack@1.2.0:', when='@4.0.0: +butterflypack+mpi')
    depends_on('cuda', when='@4.0.0: +cuda')
    depends_on('zfp', when='+zfp')
    depends_on('hipblas', when='+rocm')
    depends_on('rocsolver', when='+rocm')
    depends_on('slate', when='+slate')
    depends_on('slate+cuda', when='+cuda+slate')
    depends_on('slate+rocm', when='+rocm+slate')
    for val in ROCmPackage.amdgpu_targets:
        depends_on('slate amdgpu_target={0}'.format(val),
                   when='amdgpu_target={0}'.format(val))

    conflicts('+parmetis', when='~mpi')
    conflicts('+butterflypack', when='~mpi')
    conflicts('+butterflypack', when='@:3.2.0')
    conflicts('+zfp', when='@:3.9')
    conflicts('+cuda', when='@:3.9')
    conflicts('+rocm', when='@:5.0')
    conflicts('+rocm', when='+cuda')
    conflicts('+slate', when='@:5.1.1')
    conflicts('+slate', when='~mpi')

    patch('intel-19-compile.patch', when='@3.1.1')
    patch('shared-rocm.patch', when='@5.1.1')

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant('STRUMPACK_USE_MPI', 'mpi'),
            self.define_from_variant('STRUMPACK_USE_OPENMP', 'openmp'),
            self.define_from_variant('STRUMPACK_USE_CUDA', 'cuda'),
            self.define_from_variant('STRUMPACK_USE_HIP', 'rocm'),
            self.define_from_variant('TPL_ENABLE_PARMETIS', 'parmetis'),
            self.define_from_variant('TPL_ENABLE_SCOTCH', 'scotch'),
            self.define_from_variant('TPL_ENABLE_BPACK', 'butterflypack'),
            self.define_from_variant('STRUMPACK_COUNT_FLOPS', 'count_flops'),
            self.define_from_variant('STRUMPACK_TASK_TIMERS', 'task_timers'),
            self.define_from_variant('STRUMPACK_DEV_TESTING', 'build_dev_tests'),
            self.define_from_variant('STRUMPACK_BUILD_TESTS', 'build_tests'),
            '-DTPL_BLAS_LIBRARIES=%s' % spec['blas'].libs.joined(";"),
            '-DTPL_LAPACK_LIBRARIES=%s' % spec['lapack'].libs.joined(";"),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared')
        ]

        if '+mpi' in spec:
            args.append(
                '-DTPL_SCALAPACK_LIBRARIES=%s' % spec['scalapack'].
                libs.joined(";"))

        if spec.satisfies('@:3.9'):
            if '+mpi' in spec:
                args.extend([
                    '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
                    '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
                    '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc
                ])
            args.extend([
                self.define_from_variant('STRUMPACK_C_INTERFACE', 'c_interface'),
            ])

        if '+cuda' in spec:
            args.extend([
                '-DCUDA_TOOLKIT_ROOT_DIR={0}'.format(spec['cuda'].prefix),
                '-DCMAKE_CUDA_HOST_COMPILER={0}'.format(env["SPACK_CXX"])])
            cuda_archs = spec.variants['cuda_arch'].value
            if 'none' not in cuda_archs:
                args.append('-DCUDA_NVCC_FLAGS={0}'.
                            format(' '.join(self.cuda_flags(cuda_archs))))

        if '+rocm' in spec:
            args.append(
                '-DHIP_ROOT_DIR={0}'.format(spec['hip'].prefix))
            rocm_archs = spec.variants['amdgpu_target'].value
            if 'none' not in rocm_archs:
                args.append('-DHIP_HIPCC_FLAGS=--amdgpu-target={0}'.
                            format(",".join(rocm_archs)))

        return args

    test_src_dir = 'test'

    @property
    def test_data_dir(self):
        """Return the stand-alone test data directory."""
        add_sparse = not self.spec.satisfies('@:5.1.1')
        return join_path('examples', 'sparse' if add_sparse else '', 'data')

    # TODO: Replace this method and its 'get' use for cmake path with
    #   join_path(self.spec['cmake'].prefix.bin, 'cmake') once stand-alone
    #   tests can access build dependencies through self.spec['cmake'].
    def cmake_bin(self, set=True):
        """(Hack) Set/get cmake dependency path."""
        filepath = join_path(self.install_test_root, 'cmake_bin_path.txt')
        if set:
            with open(filepath, 'w') as out_file:
                cmake_bin = join_path(self.spec['cmake'].prefix.bin, 'cmake')
                out_file.write('{0}\n'.format(cmake_bin))
        else:
            with open(filepath, 'r') as in_file:
                return in_file.read().strip()

    @run_after('install')
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources([self.test_data_dir, self.test_src_dir])

        # TODO: Remove once self.spec['cmake'] is available here
        self.cmake_bin(set=True)

    def _test_example(self, test_prog, test_dir, test_cmd, test_args):
        cmake_filename = join_path(test_dir, 'CMakeLists.txt')
        with open(cmake_filename, 'w') as mkfile:
            mkfile.write('cmake_minimum_required(VERSION 3.15)\n')
            mkfile.write('project(StrumpackSmokeTest LANGUAGES CXX)\n')
            mkfile.write('find_package(STRUMPACK REQUIRED)\n')
            mkfile.write('add_executable({0} {0}.cpp)\n'.format(test_prog))
            mkfile.write('target_link_libraries({0} '.format(test_prog) +
                         'PRIVATE STRUMPACK::strumpack)\n')

        # TODO: Remove/replace once self.spec['cmake'] is available here
        cmake_bin = self.cmake_bin(set=False)

        opts = self.std_cmake_args
        opts += self.cmake_args()
        opts += ['.']

        self.run_test(cmake_bin, opts, [], installed=False,
                      purpose='test: generating makefile', work_dir=test_dir)
        self.run_test('make', test_prog,
                      purpose='test: building {0}'.format(test_prog),
                      work_dir=test_dir)
        with set_env(OMP_NUM_THREADS='1'):
            self.run_test(test_cmd, test_args, installed=False,
                          purpose='test: running {0}'.format(test_prog),
                          skip_missing=False, work_dir=test_dir)

    def test(self):
        """Run the stand-alone tests for the installed software."""
        test_dir = join_path(
            self.test_suite.current_test_cache_dir, self.test_src_dir
        )
        test_exe = 'test_sparse_seq'
        test_exe_mpi = 'test_sparse_mpi'
        exe_arg = [join_path('..', self.test_data_dir, 'pde900.mtx')]
        if '+mpi' in self.spec:
            test_args = ['-n', '1', test_exe_mpi]
            test_args.extend(exe_arg)
            mpiexe_list = ['srun', 'mpirun', 'mpiexec']
            for mpiexe in mpiexe_list:
                if which(mpiexe) is not None:
                    self._test_example(test_exe_mpi, test_dir,
                                       mpiexe, test_args)
                    break
        else:
            self._test_example(test_exe, test_dir, test_exe, exe_arg)

    def check(self):
        """Skip the builtin testsuite, use the stand-alone tests instead."""
        pass
