# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Slate(CMakePackage, CudaPackage, ROCmPackage):
    """The Software for Linear Algebra Targeting Exascale (SLATE) project is
    to provide fundamental dense linear algebra capabilities to the US
    Department of Energy and to the high-performance computing (HPC) community
    at large. To this end, SLATE will provide basic dense matrix operations
    (e.g., matrix multiplication, rank-k update, triangular solve), linear
    systems solvers, least square solvers, singular value and eigenvalue
    solvers."""

    homepage = "https://icl.utk.edu/slate/"
    git      = "https://bitbucket.org/icl/slate"
    url      = 'https://bitbucket.org/icl/slate/downloads/slate-2020.10.00.tar.gz'
    maintainers = ['G-Ragghianti', 'mgates3']

    tags = ['e4s']
    test_requires_compiler = True

    version('master', branch='master')
    version('2021.05.02', sha256='29667a9e869e41fbc22af1ae2bcd425d79b4094bbb3f21c411888e7adc5d12e3')
    version('2021.05.01', sha256='d9db2595f305eb5b1b49a77cc8e8c8e43c3faab94ed910d8387c221183654218')
    version('2020.10.00', sha256='ff58840cdbae2991d100dfbaf3ef2f133fc2f43fc05f207dc5e38a41137882ab')

    variant('mpi',    default=True, description='Build with MPI support (without MPI is experimental).')
    variant('openmp', default=True, description='Build with OpenMP support.')
    variant('shared', default=True, description='Build shared library')

    # The runtime dependency on cmake is needed by the stand-alone tests (spack test).
    depends_on('cmake', type='run')

    depends_on('mpi', when='+mpi')
    depends_on('blas')
    depends_on('blaspp ~cuda', when='~cuda')
    depends_on('blaspp +cuda', when='+cuda')
    depends_on('blaspp ~rocm', when='~rocm')
    for val in ROCmPackage.amdgpu_targets:
        depends_on('blaspp +rocm amdgpu_target=%s' % val, when='amdgpu_target=%s' % val)
    depends_on('lapackpp@2021.04.00:', when='@2021.05.01:')
    depends_on('lapackpp@2020.10.02', when='@2020.10.00')
    depends_on('lapackpp@master', when='@master')
    depends_on('scalapack')

    cpp_17_msg = 'Requires C++17 compiler support'
    conflicts('%gcc@:5', msg=cpp_17_msg)
    conflicts('%xl', msg=cpp_17_msg)
    conflicts('%xl_r', msg=cpp_17_msg)
    conflicts('%intel@19:', msg='Does not currently build with icpc >= 2019')
    conflicts('+rocm', when='@:2020.10.00', msg='ROCm support requires SLATE 2021.05.01 or greater')
    conflicts('+rocm', when='+cuda', msg='SLATE only supports one GPU backend at a time')

    def cmake_args(self):
        spec = self.spec
        backend_config = '-Duse_cuda=%s' % ('+cuda' in spec)
        if self.version >= Version('2021.05.01'):
            backend = 'none'
            if '+cuda' in spec:
                backend = 'cuda'
            if '+rocm' in spec:
                backend = 'hip'
            backend_config = '-Dgpu_backend=%s' % backend

        return [
            '-Dbuild_tests=%s'       % self.run_tests,
            '-Duse_openmp=%s'        % ('+openmp' in spec),
            '-DBUILD_SHARED_LIBS=%s' % ('+shared' in spec),
            backend_config,
            '-Duse_mpi=%s'           % ('+mpi' in spec),
            '-DSCALAPACK_LIBRARIES=%s'    % spec['scalapack'].libs.joined(';')
        ]

    @run_after('install')
    def cache_test_sources(self):
        if self.spec.satisfies('@2020.10.00'):
            return
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources(['examples'])

    def test(self):
        if self.spec.satisfies('@2020.10.00') or '+mpi' not in self.spec:
            print('Skipping: stand-alone tests')
            return

        test_dir = join_path(self.test_suite.current_test_cache_dir,
                             'examples', 'build')
        with working_dir(test_dir, create=True):
            cmake_bin = join_path(self.spec['cmake'].prefix.bin, 'cmake')
            prefixes = ';'.join([self.spec['blaspp'].prefix,
                                 self.spec['lapackpp'].prefix,
                                 self.spec['mpi'].prefix,
                                 ])
            self.run_test(cmake_bin, ['-DCMAKE_PREFIX_PATH=' + prefixes, '..'])
            make()
            test_args = ['-n', '4', './ex05_blas']
            mpi_path = self.spec['mpi'].prefix.bin
            mpiexe_f = which('srun', 'mpirun', 'mpiexec', path=mpi_path)
            self.run_test(mpiexe_f.command, test_args,
                          purpose='SLATE smoke test')
            make('clean')
