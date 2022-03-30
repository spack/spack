# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from llnl.util import tty

from spack import *


class Sundials(CMakePackage, CudaPackage, ROCmPackage):
    """SUNDIALS (SUite of Nonlinear and DIfferential/ALgebraic equation
    Solvers)"""

    homepage = "https://computing.llnl.gov/projects/sundials"
    url = "https://github.com/LLNL/sundials/releases/download/v2.7.0/sundials-2.7.0.tar.gz"
    git = "https://github.com/llnl/sundials.git"
    tags = ['radiuss', 'e4s']
    test_requires_compiler = True

    maintainers = ['balos1', 'cswoodward', 'gardner48']

    # ==========================================================================
    # Versions
    # ==========================================================================
    version('develop', branch='develop')
    version('6.1.1', sha256='cfaf637b792c330396a25ef787eb59d58726c35918ebbc08e33466e45d50470c')
    version('6.1.0', sha256='eea49f52140640e54931c779e73aece65f34efa996a26b2263db6a1e27d0901c')
    version('6.0.0', sha256='c7178e54df20a9363ae3e5ac5b3ee9db756a4ddd4b8fff045127e93b73b151f4')
    version('5.8.0', sha256='d4ed403351f72434d347df592da6c91a69452071860525385b3339c824e8a213')
    version('5.7.0', sha256='48da7baa8152ddb22aed1b02d82d1dbb4fbfea22acf67634011aa0303a100a43')
    version('5.6.1', sha256='16b77999ec7e7f2157aa1d04ca1de4a2371ca8150e056d24951d0c58966f2a83')
    version('5.6.0', sha256='95e4201912e150f29c6f6f7625de763385e2073dae7f929c4a544561ea29915d')
    version('5.5.0', sha256='2a755e89aab96d2ff096a4e30bf00bb162e80be20e9e99f424dccfb249098237')
    version('5.4.0', sha256='04d8a2ebe02cdaeef5a9e22ff7e3146bb563d8400f65772b6c7af80001413ffa')
    version('5.3.0', sha256='88dff7e11a366853d8afd5de05bf197a8129a804d9d4461fb64297f1ef89bca7')
    version('5.2.0', sha256='95f058acce5bd66e654de65acdbb1c9f44c90cf1b4e28f8d933cdb4415ebba3e')
    version('5.1.0', sha256='fb22d14fad42203809dc46d046b001149ec4e901b23882bd4a80619157fd9b21')
    version('5.0.0', sha256='345141ec01c641d0bdfb3476c478b7e74fd6a7192a478a27cafe75d9da2d7dd3')
    version('4.1.0', sha256='280de1c27b2360170a6f46cb3799b2aee9dff3bddbafc8b08c291a47ab258aa5')
    version('4.0.1', sha256='29e409c8620e803990edbda1ebf49e03a38c08b9187b90658d86bddae913aed4')
    version('3.2.1', sha256='47d94d977ab2382cdcdd02f72a25ebd4ba8ca2634bbb2f191fe1636e71c86808')
    version('3.2.0', sha256='d2b690afecadf8b5a048bb27ab341de591d714605b98d3518985dfc2250e93f9')
    version('3.1.2', sha256='a8985bb1e851d90e24260450667b134bc13d71f5c6effc9e1d7183bd874fe116')
    version('3.1.1', sha256='a24d643d31ed1f31a25b102a1e1759508ce84b1e4739425ad0e18106ab471a24')
    version('3.1.0', sha256='18d52f8f329626f77b99b8bf91e05b7d16b49fde2483d3a0ea55496ce4cdd43a')
    version('3.0.0', sha256='28b8e07eecfdef66e2c0d0ea0cb1b91af6e4e94d71008abfe80c27bf39f63fde')
    version('2.7.0', sha256='d39fcac7175d701398e4eb209f7e92a5b30a78358d4a0c0fcc23db23c11ba104')
    version('2.6.2', sha256='d8ed0151509dd2b0f317b318a4175f8b95a174340fc3080b8c20617da8aa4d2f')

    # ==========================================================================
    # Variants
    # ==========================================================================

    # SUNDIALS solvers
    sun_solvers = ['CVODE', 'CVODES', 'ARKODE', 'IDA', 'IDAS', 'KINSOL']

    for pkg in sun_solvers:
        variant(pkg, default=True,
                description='Enable %s solver' % pkg)

    # Language standards
    variant('cstd', default='99',
            description='C language standard',
            values=('90', '99', '11', '17'))

    variant('cxxstd', default='14',
            description='C++ language standard',
            values=('99', '11', '14', '17'))

    # Real type
    variant(
        'precision',
        default='double',
        description='real type precision',
        values=('single', 'double', 'extended'),
        multi=False
    )

    # Index type
    variant('int64', default=False,
            description='Use 64bit integers for indices')

    # Parallelism
    variant('mpi',     default=True,
            description='Enable MPI parallel vector')
    variant('openmp',  default=False,
            description='Enable OpenMP parallel vector')
    variant('pthread', default=False,
            description='Enable Pthreads parallel vector')
    variant('raja',    default=False,
            description='Enable RAJA vector')
    variant('sycl',    default=False,
            description='Enable SYCL vector')

    # External libraries
    variant('caliper',      default=False, when='@6.0.0: +profiling',
            description='Enable Caliper instrumentation/profiling')
    variant('hypre',        default=False,
            description='Enable Hypre MPI parallel vector')
    variant('lapack',       default=False,
            description='Enable LAPACK direct solvers')
    variant('klu',          default=False,
            description='Enable KLU sparse, direct solver')
    variant('petsc',        default=False,
            description='Enable PETSc interfaces')
    variant('superlu-mt',   default=False,
            description='Enable SuperLU_MT sparse, direct solver')
    variant('superlu-dist', default=False,
            description='Enable SuperLU_DIST sparse, direct solver')
    variant('trilinos', default=False,
            description='Enable Trilinos interfaces')

    # Library type
    variant('shared', default=True,
            description='Build shared libraries')
    variant('static', default=True,
            description='Build static libraries')

    # Fortran interfaces
    variant('fcmix', default=False,
            description='Enable Fortran 77 interface')
    variant('f2003', default=False,
            description='Enable Fortran 2003 interface')

    # Examples
    variant('examples',         default=True,
            description='Enable examples')
    variant('examples-install', default=True,
            description='Install examples')

    # Generic (std-c) math libraries (UNIX only)
    variant('generic-math', default=True,
            description='Use generic (std-c) math libraries on unix systems')

    # Monitoring
    variant('monitoring', default=False, when='@5.5.0:',
            description='Build with simulation monitoring capabilities')

    # Profiling
    variant('profiling', default=False, when='@6.0.0:',
            description='Build with profiling capabilities')

    # ==========================================================================
    # Conflicts
    # ==========================================================================

    conflicts('+hypre',         when='@:2.6.2')
    conflicts('+petsc',         when='@:2.6.2')
    conflicts('+cuda',          when='@:2.7.0')
    conflicts('+raja',          when='@:2.7.0')
    conflicts('+sycl',          when='@:5.6.0')
    conflicts('~int64',         when='@:2.7.0')
    conflicts('+superlu-dist',  when='@:4.1.0')
    conflicts('+f2003',         when='@:4.1.0')
    conflicts('+trilinos',      when='@:4.1.0')
    conflicts('+rocm',          when='@:5.6.0')

    # External libraries incompatible with 64-bit indices
    conflicts('+lapack', when='@3.0.0: +int64')
    conflicts('+hypre',  when='+hypre@:2.6.1a +int64')

    # External libraries incompatible with single precision
    conflicts('+klu',          when='precision=single')
    conflicts('+hypre',        when='+hypre@:2.12.0 precision=single')
    conflicts('+superlu-dist', when='precision=single')

    # External libraries incompatible with extended (quad) precision
    conflicts('+lapack',       when='precision=extended')
    conflicts('+superlu-mt',   when='precision=extended')
    conflicts('+superlu-dist', when='precision=extended')
    conflicts('+klu',          when='precision=extended')
    conflicts('+hypre',        when='+hypre@:2.12.0 precision=extended')

    # SuperLU_MT interface requires lapack for external blas (before v3.0.0)
    conflicts('+superlu-mt', when='@:2.7.0 ~lapack')

    # rocm+examples and cstd do not work together in 6.0.0
    conflicts('+rocm+examples', when='@6.0.0')

    # ==========================================================================
    # Dependencies
    # ==========================================================================

    # Build dependencies
    depends_on('cmake@3.12:', type='build')

    # MPI related dependencies
    depends_on('mpi', when='+mpi')
    depends_on('mpi', when='+hypre')
    depends_on('mpi', when='+petsc')
    depends_on('mpi', when='+superlu-dist')

    # Other parallelism dependencies
    depends_on('raja',      when='+raja')
    depends_on('raja+cuda', when='+raja +cuda')
    depends_on('raja+rocm', when='+raja +rocm')

    # External libraries
    depends_on('caliper',                 when='+caliper')
    depends_on('lapack',                  when='+lapack')
    depends_on('hypre+mpi~int64',         when='@5.7.1: +hypre ~int64')
    depends_on('hypre+mpi+int64',         when='@5.7.1: +hypre +int64')
    depends_on('hypre@:2.22.0+mpi~int64', when='@:5.7.0 +hypre ~int64')
    depends_on('hypre@:2.22.0+mpi+int64', when='@:5.7.0 +hypre +int64')
    depends_on('petsc+mpi',               when='+petsc')
    depends_on('suite-sparse',            when='+klu')
    depends_on('superlu-dist@6.1.1:',     when='@:5.4.0 +superlu-dist')
    depends_on('superlu-dist@6.3.0:',     when='@5.5.0: +superlu-dist')
    depends_on('trilinos+tpetra',         when='+trilinos')

    # Require that external libraries built with the same precision
    depends_on('petsc~double~complex', when='+petsc precision=single')
    depends_on('petsc+double~complex', when='+petsc precision=double')

    # Require that external libraries built with the same index type
    depends_on('petsc~int64', when='+petsc ~int64')
    depends_on('petsc+int64', when='+petsc +int64')
    depends_on('superlu-dist+int64', when='+superlu-dist +int64')

    # Require that SuperLU_MT built with external blas
    depends_on('superlu-mt+blas', when='+superlu-mt')

    # ==========================================================================
    # Patches
    # ==========================================================================

    # remove OpenMP header file and function from hypre vector test code
    patch('test_nvector_parhyp.patch', when='@2.7.0:3.0.0')
    patch('FindPackageMultipass.cmake.patch', when='@5.0.0')
    patch('5.5.0-xsdk-patches.patch', when='@5.5.0')
    patch('0001-add-missing-README-to-examples-cvode-hip.patch', when='@5.6.0:5.7.0')
    # remove sundials_nvecopenmp target from ARKODE SuperLU_DIST example
    patch('remove-links-to-OpenMP-vector.patch', when='@5.5.0:5.7.0')

    # ==========================================================================
    # SUNDIALS Settings
    # ==========================================================================

    def cmake_args(self):
        spec = self.spec
        define = CMakePackage.define
        from_variant = self.define_from_variant

        # List of CMake arguments
        # Note: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE are set automatically
        args = []

        # SUNDIALS solvers
        for pkg in self.sun_solvers:
            args.append(from_variant('BUILD_' + pkg, pkg))

        args.extend([
            # language standard
            from_variant('CMAKE_C_STANDARD', 'cstd'),
            from_variant('CMAKE_CXX_STANDARD', 'cxxstd'),
            # precision
            from_variant('SUNDIALS_PRECISION', 'precision'),
        ])

        # index type (v3.0.0 or later)
        if spec.satisfies('@3:'):
            intsize = "64" if '+int64' in spec else "32"
            args.extend([
                define('SUNDIALS_INDEX_SIZE', intsize),
                define('SUNDIALS_INDEX_TYPE', 'int{}_t'.format(intsize)),
            ])

        args.extend([
            # Fortran interface
            from_variant('F77_INTERFACE_ENABLE', 'fcmix'),
            from_variant('F2003_INTERFACE_ENABLE', 'f2003'),
            # library type
            from_variant('BUILD_SHARED_LIBS', 'shared'),
            from_variant('BUILD_STATIC_LIBS', 'static'),
            # Generic (std-c) math libraries
            from_variant('USE_GENERIC_MATH', 'generic-math'),
            # Monitoring
            from_variant('SUNDIALS_BUILD_WITH_MONITORING', 'monitoring'),
            # Profiling
            from_variant('SUNDIALS_BUILD_WITH_PROFILING', 'profiling'),
            from_variant('ENABLE_CALIPER', 'caliper'),
        ])

        if '+caliper' in spec:
            args.append(define('CALIPER_DIR', spec['caliper'].prefix))

        # parallelism
        args.extend([
            from_variant('MPI_ENABLE', 'mpi'),
            from_variant('OPENMP_ENABLE', 'openmp'),
            from_variant('PTHREAD_ENABLE', 'pthread'),
            from_variant('ENABLE_SYCL', 'sycl'),
            from_variant('CUDA_ENABLE', 'cuda'),
            from_variant('ENABLE_HIP', 'rocm'),
            from_variant('HYPRE_ENABLE', 'hypre'),
            from_variant('KLU_ENABLE', 'klu'),
            from_variant('LAPACK_ENABLE', 'lapack'),
            from_variant('PETSC_ENABLE', 'petsc'),
            from_variant('RAJA_ENABLE', 'raja'),
            from_variant('SUPERLUMT_ENABLE', 'superlu-mt'),
            from_variant('SUPERLUDIST_ENABLE', 'superlu-dist'),
            from_variant('Trilinos_ENABLE', 'trilinos'),
            from_variant('EXAMPLES_INSTALL', 'examples-install'),
        ])

        if '+cuda' in spec:
            args.append(define(
                'CMAKE_CUDA_ARCHITECTURES', spec.variants['cuda_arch'].value
            ))

        if '+rocm' in spec:
            args.extend([
                define('CMAKE_C_COMPILER', spec['llvm-amdgpu'].prefix.bin.clang),
                define('CMAKE_CXX_COMPILER', spec['hip'].hipcc),
                define('HIP_PATH', spec['hip'].prefix),
                define('HIP_CLANG_INCLUDE_PATH', spec['llvm-amdgpu'].prefix.include),
                define('ROCM_PATH', spec['llvm-amdgpu'].prefix),
                define('AMDGPU_TARGETS', spec.variants['amdgpu_target'].value),
            ])

        # MPI support
        if '+mpi' in spec:
            args.extend([
                define('MPI_MPICC', spec['mpi'].mpicc),
                define('MPI_MPICXX', spec['mpi'].mpicxx),
                define('MPI_MPIF77', spec['mpi'].mpif77),
                define('MPI_MPIF90', spec['mpi'].mpifc),
            ])

        # Building with Hypre
        if '+hypre' in spec:
            args.extend([
                define('HYPRE_INCLUDE_DIR', spec['hypre'].prefix.include),
                define('HYPRE_LIBRARY_DIR', spec['hypre'].prefix.lib)
            ])

        # Building with KLU
        if '+klu' in spec:
            args.extend([
                define('KLU_INCLUDE_DIR', spec['suite-sparse'].prefix.include),
                define('KLU_LIBRARY_DIR', spec['suite-sparse'].prefix.lib)
            ])

        # Building with LAPACK
        if '+lapack' in spec:
            args.append(define('LAPACK_LIBRARIES',
                        spec['lapack'].libs + spec['blas'].libs))

        # Building with PETSc
        if '+petsc' in spec:
            if spec.version >= Version('5'):
                args.append(define('PETSC_DIR', spec['petsc'].prefix))
            else:
                args.extend([
                    define('PETSC_INCLUDE_DIR', spec['petsc'].prefix.include),
                    define('PETSC_LIBRARY_DIR', spec['petsc'].prefix.lib),
                ])

        # Building with RAJA
        if '+raja' in spec:
            args.append(define('RAJA_DIR', spec['raja'].prefix))

        # Building with SuperLU_MT
        if '+superlu-mt' in spec:
            if spec.satisfies('@3:'):
                args.extend([
                    define('BLAS_ENABLE', True),
                    define('BLAS_LIBRARIES', spec['blas'].libs),
                ])
            args.extend([
                define('SUPERLUMT_INCLUDE_DIR', spec['superlu-mt'].prefix.include),
                define('SUPERLUMT_LIBRARY_DIR', spec['superlu-mt'].prefix.lib),
                define('SUPERLUMT_THREAD_TYPE',
                       'OpenMP' if '^superlu-mt+openmp' in spec else 'Pthread'),
            ])

        # Building with SuperLU_DIST
        if '+superlu-dist' in spec:
            args.extend([
                define('OPENMP_ENABLE', '^superlu-dist+openmp' in spec),
                define('SUPERLUDIST_INCLUDE_DIR', spec['superlu-dist'].prefix.include),
                define('SUPERLUDIST_LIBRARY_DIR', spec['superlu-dist'].prefix.lib),
                define('SUPERLUDIST_LIBRARIES', spec['blas'].libs),
                define('SUPERLUDIST_OpenMP', '^superlu-dist+openmp' in spec),
            ])

        # Building with Trilinos
        if '+trilinos' in spec:
            args.append(define('Trilinos_DIR', spec['trilinos'].prefix))

        # Examples
        if spec.satisfies('@3:'):
            args.extend([
                from_variant('EXAMPLES_ENABLE_C', 'examples'),
                from_variant('EXAMPLES_ENABLE_CXX', 'examples'),
                define('EXAMPLES_ENABLE_CUDA', '+examples+cuda' in spec),
                define('EXAMPLES_ENABLE_F77', '+examples+fcmix' in spec),
                define('EXAMPLES_ENABLE_F90', '+examples+fcmix' in spec),
                define('EXAMPLES_ENABLE_F2003', '+examples+f2003' in spec),
            ])
        else:
            args.extend([
                from_variant('EXAMPLES_ENABLE', 'examples'),
                from_variant('CXX_ENABLE', 'examples'),
                define('F90_ENABLE', '+examples+fcmix' in spec),
            ])

        return args

    # ==========================================================================
    # Post Install Actions
    # ==========================================================================

    @run_after('install')
    def post_install(self):
        """Run after install to fix install name of dynamic libraries
        on Darwin to have full path and install the LICENSE file."""
        spec = self.spec
        prefix = self.spec.prefix

        if (sys.platform == 'darwin'):
            fix_darwin_install_name(prefix.lib)

        if spec.satisfies('@:3.0.0'):
            install('LICENSE', prefix)

    @run_after('install')
    def filter_compilers(self):
        """Run after install to tell the example program Makefiles
        to use the compilers that Spack built the package with.

        If this isn't done, they'll have CC, CPP, and F77 set to
        Spack's generic cc and f77. We want them to be bound to
        whatever compiler they were built with."""

        spec = self.spec

        kwargs = {'ignore_absent': True, 'backup': False, 'string': True}
        dirname = os.path.join(self.prefix, 'examples')

        cc_files = [
            'arkode/C_openmp/Makefile',
            'arkode/C_parallel/Makefile',
            'arkode/C_parhyp/Makefile',
            'arkode/C_petsc/Makefile',
            'arkode/C_serial/Makefile',
            'cvode/C_openmp/Makefile',
            'cvode/parallel/Makefile',
            'cvode/parhyp/Makefile',
            'cvode/petsc/Makefile',
            'cvode/serial/Makefile',
            'cvodes/C_openmp/Makefile',
            'cvodes/parallel/Makefile',
            'cvodes/serial/Makefile',
            'ida/C_openmp/Makefile',
            'ida/parallel/Makefile',
            'ida/petsc/Makefile',
            'ida/serial/Makefile',
            'idas/C_openmp/Makefile',
            'idas/parallel/Makefile',
            'idas/serial/Makefile',
            'kinsol/C_openmp/Makefile',
            'kinsol/parallel/Makefile',
            'kinsol/serial/Makefile',
            'nvector/C_openmp/Makefile',
            'nvector/parallel/Makefile',
            'nvector/parhyp/Makefile',
            'nvector/petsc/Makefile',
            'nvector/pthreads/Makefile',
            'nvector/serial/Makefile',
            'sunlinsol/band/Makefile',
            'sunlinsol/dense/Makefile',
            'sunlinsol/klu/Makefile',
            'sunlinsol/lapackband/Makefile',
            'sunlinsol/lapackdense/Makefile',
            'sunlinsol/pcg/parallel/Makefile',
            'sunlinsol/pcg/serial/Makefile',
            'sunlinsol/spbcgs/parallel/Makefile',
            'sunlinsol/spbcgs/serial/Makefile',
            'sunlinsol/spfgmr/parallel/Makefile',
            'sunlinsol/spfgmr/serial/Makefile',
            'sunlinsol/spgmr/parallel/Makefile',
            'sunlinsol/spgmr/serial/Makefile',
            'sunlinsol/sptfqmr/parallel/Makefile',
            'sunlinsol/sptfqmr/serial/Makefile',
            'sunlinsol/superlumt/Makefile',
            'sunlinsol/superludist/Makefile',
            'sunmatrix/band/Makefile',
            'sunmatrix/dense/Makefile',
            'sunmatrix/sparse/Makefile'
        ]

        cxx_files = [
            'arkode/CXX_parallel/Makefile',
            'arkode/CXX_serial/Makefile'
            'cvode/cuda/Makefile',
            'cvode/raja/Makefile',
            'nvector/cuda/Makefile',
            'nvector/raja/Makefile'
        ]

        f77_files = [
            'arkode/F77_parallel/Makefile',
            'arkode/F77_serial/Makefile',
            'cvode/fcmix_parallel/Makefile',
            'cvode/fcmix_serial/Makefile',
            'ida/fcmix_openmp/Makefile',
            'ida/fcmix_parallel/Makefile',
            'ida/fcmix_pthreads/Makefile',
            'ida/fcmix_serial/Makefile',
            'kinsol/fcmix_parallel/Makefile',
            'kinsol/fcmix_serial/Makefile'
        ]

        f90_files = [
            'arkode/F90_parallel/Makefile',
            'arkode/F90_serial/Makefile'
        ]

        f2003_files = [
            'arkode/F2003_serial/Makefile',
            'cvode/F2003_serial/Makefile',
            'cvodes/F2003_serial/Makefike',
            'ida/F2003_serial/Makefile',
            'idas/F2003_serial/Makefile',
            'kinsol/F2003_serial/Makefile'
        ]

        for filename in cc_files:
            filter_file(os.environ['CC'], self.compiler.cc,
                        os.path.join(dirname, filename), **kwargs)

        for filename in cc_files:
            filter_file(r'^CPP\s*=.*', self.compiler.cc,
                        os.path.join(dirname, filename), **kwargs)

        for filename in cxx_files:
            filter_file(os.environ['CXX'], self.compiler.cxx,
                        os.path.join(dirname, filename), **kwargs)

        for filename in cxx_files:
            filter_file(r'^CPP\s*=.*', self.compiler.cc,
                        os.path.join(dirname, filename), **kwargs)

        if ('+fcmix' in spec) and ('+examples' in spec):
            for filename in f77_files:
                filter_file(os.environ['F77'], self.compiler.f77,
                            os.path.join(dirname, filename), **kwargs)

        if ('+fcmix' in spec) and ('+examples' in spec):
            for filename in f90_files:
                filter_file(os.environ['FC'], self.compiler.fc,
                            os.path.join(dirname, filename), **kwargs)

        if ('+f2003' in spec) and ('+examples' in spec):
            for filename in f2003_files:
                filter_file(os.environ['FC'], self.compiler.fc,
                            os.path.join(dirname, filename), **kwargs)

    @property
    def headers(self):
        """Export the headers and defines of SUNDIALS.
           Sample usage: spec['sundials'].headers.cpp_flags
        """
        # SUNDIALS headers are inside subdirectories, so we use a fake header
        # in the include directory.
        hdr = find(self.prefix.include.nvector, 'nvector_serial.h',
                   recursive=False)
        return HeaderList(join_path(self.spec.prefix.include, 'fake.h')) \
            if hdr else None

    @property
    def libs(self):
        """Export the libraries of SUNDIALS.
           Sample usage: spec['sundials'].libs.ld_flags
                         spec['sundials:arkode,cvode'].libs.ld_flags
        """
        query_parameters = self.spec.last_query.extra_parameters
        if not query_parameters:
            sun_libs = 'libsundials_*[!0-9]'
            # Q: should the result be ordered by dependency?
        else:
            sun_libs = ['libsundials_' + p for p in query_parameters]
        is_shared = '+shared' in self.spec

        libs = find_libraries(sun_libs, root=self.prefix, shared=is_shared,
                              recursive=True)

        return libs or None  # Raise an error if no libs are found

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        """Perform make test_install.
        """
        with working_dir(self.build_directory):
            make("test_install")

    @property
    def _smoke_tests(self):
        # smoke_tests tuple: exe, args, purpose, use cmake (true/false)
        smoke_tests = [('nvector/serial/test_nvector_serial', ['10', '0'],
                        'Test serial N_Vector', False)]
        if '+CVODE' in self.spec:
            smoke_tests.append(('cvode/serial/cvAdvDiff_bnd', [],
                                'Test CVODE', True))

        if '+cuda' in self.spec:
            smoke_tests.append(('nvector/cuda/test_nvector_cuda', ['10', '0', '0'],
                                'Test CUDA N_Vector', True))
            if '+CVODE' in self.spec:
                smoke_tests.append(('cvode/cuda/cvAdvDiff_kry_cuda', [],
                                    'Test CVODE with CUDA', True))

        if '+hip' in self.spec:
            smoke_tests.append(('nvector/hip/test_nvector_hip', ['10', '0', '0'],
                                'Test HIP N_Vector', True))
            if '+CVODE' in self.spec:
                smoke_tests.append(('cvode/hip/cvAdvDiff_kry_hip', [],
                                    'Test CVODE with HIP', True))

        if '+sycl' in self.spec:
            smoke_tests.append(('nvector/sycl/test_nvector_sycl', ['10', '0', '0'],
                                'Test SYCL N_Vector'))
            if '+CVODE' in self.spec:
                smoke_tests.append(('cvode/sycl/cvAdvDiff_kry_sycl', [],
                                    'Test CVODE with SYCL', True))

        return smoke_tests

    @property
    def _smoke_tests_path(self):
        # examples/smoke-tests are cached for testing
        return self.prefix.examples

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
        elif os.path.isfile(filepath):
            with open(filepath, 'r') as in_file:
                return in_file.read().strip()

    @run_after('install')
    def setup_smoke_tests(self):
        install_tree(self._smoke_tests_path,
                     join_path(self.install_test_root, 'testing'))
        self.cmake_bin(set=True)

    def build_smoke_tests(self):
        cmake_bin = self.cmake_bin(set=False)

        if not cmake_bin:
            tty.msg('Skipping sundials test: cmake_bin_path.txt not found')
            return

        for smoke_test in self._smoke_tests:
            work_dir = join_path(self._smoke_tests_path, os.path.dirname(smoke_test[0]))
            with working_dir(work_dir):
                if smoke_test[3]:  # use cmake
                    self.run_test(exe=cmake_bin, options=['.'])
                self.run_test(exe='make')

    def run_smoke_tests(self):
        for smoke_test in self._smoke_tests:
            self.run_test(exe=join_path(self._smoke_tests_path, smoke_test[0]),
                          options=smoke_test[1], status=[0], installed=True,
                          skip_missing=True, purpose=smoke_test[2])

    def clean_smoke_tests(self):
        for smoke_test in self._smoke_tests:
            work_dir = join_path(self._smoke_tests_path, os.path.dirname(smoke_test[0]))
            with working_dir(work_dir):
                self.run_test(exe='make', options=['clean'])

    def test(self):
        self.build_smoke_tests()
        self.run_smoke_tests()
        self.clean_smoke_tests()
        return
