# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Phist(CMakePackage):
    """The Pipelined, Hybrid-parallel Iterative Solver Toolkit provides
    implementations of and interfaces to block iterative solvers for sparse
    linear and eigenvalue problems. In contrast to other libraries we support
    multiple backends (e.g. Trilinos, PETSc and our own optimized kernels),
    and interfaces in multiple languages such as C, C++, Fortran 2003 and
    Python. PHIST has a clear focus on portability and hardware performance:
    in particular support row-major storage of block vectors and using GPUs
    (via the ghost library or Trilinos/Tpetra).
    """

    homepage = "https://bitbucket.org/essex/phist/"
    url      = "https://bitbucket.org/essex/phist/get/phist-1.4.3.tar.gz"
    git      = "https://bitbucket.org/essex/phist/phist.git"

    maintainers = ['jthies']

    version('develop', branch='devel')
    version('master', branch='master')
    version('1.8.0', sha256='ee42946bce187e126452053b5f5c200b57b6e40ee3f5bcf0751f3ced585adeb0')
    version('1.7.5', sha256='f11fe27f2aa13d69eb285cc0f32c33c1603fa1286b84e54c81856c6f2bdef500')
    version('1.7.4', sha256='ef0c97fda9984f53011020aff3e61523833320f5f5719af2f2ed84463cccb98b')
    version('1.7.3', sha256='ab2d853c9ba13bcd3069fcc61c359cb412466a2e4b22ebbd2f5263cffa685126')
    version('1.7.2', sha256='29b504d78b5efd57b87d2ca6e20bc8a32b1ba55b40f5a5b7189cc0d28e43bcc0')
    version('1.6.1', sha256='4ed4869f24f920a494aeae0f7d1d94fe9efce55ebe0d298a5948c9603e07994d')
    version('1.6.0', '751f855230d6227b972b5ab7bce2c65f')
    version('1.4.3', 'af3300378d4282366d148e38c3a3199a')

    variant(name='kernel_lib', default='builtin',
            description='select the kernel library (backend) for phist',
            values=['builtin',
                    'epetra',
                    'tpetra',
                    'petsc',
                    'eigen',
                    'ghost'])

    variant(name='outlev', default='2', values=['0', '1', '2', '3', '4', '5'],
            description='verbosity. 0: errors 1: +warnings 2: +info '
                        '3: +verbose 4: +extreme 5; +debug')

    variant('host', default=True,
            description='allow PHIST to use compiler flags that lead to host-'
            'specific code. Set this to False when cross-compiling.')

    variant('shared',  default=True,
            description='Enables the build of shared libraries')

    variant('mpi', default=True,
            description='enable/disable MPI (note that the kernel library may '
            'not support this choice)')

    variant('openmp', default=True,
            description='enable/disable OpenMP')

    variant('parmetis', default=False,
            description='enable/disable ParMETIS partitioning (only actually '
                        'used with kernel_lib=builtin)')

    variant('scamac', default=True,
            description='enable/disable building the "SCAlable MAtrix '
                        'Collection" matrix generators.')

    variant('trilinos', default=False,
            description='enable/disable Trilinos third-party libraries. '
                        'For all kernel_libs, we can use Belos and Anasazi '
                        'iterative solvers. For the Trilinos backends '
                        '(kernel_lib=epetra|tpetra) we can use preconditioner '
                        'packages such as Ifpack, Ifpack2 and ML.')

    variant('fortran', default=True,
            description='generate Fortran 2003 bindings (requires Python3 and '
                        'a Fortran compiler)')

    # in older versions, it is not possible to completely turn off OpenMP
    conflicts('~openmp', when='@:1.7.3')
    # in older versions, it is not possible to turn off the use of host-
    # specific compiler flags in Release mode.
    conflicts('~host', when='@:1.7.3')

    # ###################### Dependencies ##########################

    depends_on('cmake@3.8:', type='build')
    depends_on('blas')
    depends_on('lapack')
    # Python 3 or later is required for generating the Fortran 2003 bindings
    # since version 1.7, you can get rid of the dependency by switching off
    # the feature (e.g. use the '~fortran' variant)
    depends_on('python@3:', when='@1.7: +fortran', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('trilinos+anasazi+belos+teuchos', when='+trilinos')
    depends_on('trilinos@12:+tpetra', when='kernel_lib=tpetra')
    # Epetra backend also works with older Trilinos versions
    depends_on('trilinos+epetra', when='kernel_lib=epetra')
    depends_on('petsc', when='kernel_lib=petsc')
    depends_on('eigen', when='kernel_lib=eigen')
    depends_on('ghost', when='kernel_lib=ghost')

    depends_on('trilinos', when='+trilinos')
    depends_on('parmetis ^metis+int64', when='+parmetis')

    # Fortran 2003 bindings were included in version 1.7, previously they
    # required a separate package
    conflicts('+fortran', when='@:1.6.99')

    # older gcc's may produce incorrect SIMD code and fail
    # to compile some OpenMP statements
    conflicts('%gcc@:4.9.1')

    def cmake_args(self):
        spec = self.spec

        kernel_lib = spec.variants['kernel_lib'].value
        outlev = spec.variants['outlev'].value

        lapacke_libs = (spec['lapack:c'].libs + spec['blas:c'].libs +
                        find_system_libraries(['libm'])).joined(';')
        lapacke_include_dir = spec['lapack:c'].headers.directories[0]

        args = ['-DPHIST_KERNEL_LIB=%s' % kernel_lib,
                '-DPHIST_OUTLEV=%s' % outlev,
                '-DTPL_LAPACKE_LIBRARIES=%s' % lapacke_libs,
                '-DTPL_LAPACKE_INCLUDE_DIRS=%s' % lapacke_include_dir,
                '-DPHIST_ENABLE_MPI:BOOL=%s'
                % ('ON' if '+mpi' in spec else 'OFF'),
                '-DPHIST_ENABLE_OPENMP=%s'
                % ('ON' if '+openmp' in spec else 'OFF'),
                '-DBUILD_SHARED_LIBS:BOOL=%s'
                % ('ON' if '+shared' in spec else 'OFF'),
                '-DPHIST_ENABLE_SCAMAC:BOOL=%s'
                % ('ON' if '+scamac' in spec else 'OFF'),
                '-DPHIST_USE_TRILINOS_TPLS:BOOL=%s'
                % ('ON' if '+trilinos' in spec else 'OFF'),
                '-DPHIST_USE_SOLVER_TPLS:BOOL=%s'
                % ('ON' if '+trilinos' in spec else 'OFF'),
                '-DPHIST_USE_PRECON_TPLS:BOOL=%s'
                % ('ON' if '+trilinos' in spec else 'OFF'),
                '-DXSDK_ENABLE_Fortran:BOOL=%s'
                % ('ON' if '+fortran' in spec else 'OFF'),
                '-DPHIST_HOST_OPTIMIZE:BOOL=%s'
                % ('ON' if '+host' in spec else 'OFF'),
                ]

        return args

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def check(self):
        with working_dir(self.build_directory):
            make("check")

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        with working_dir(self.build_directory):
            make("test_install")
