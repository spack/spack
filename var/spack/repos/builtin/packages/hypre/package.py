# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package_defs import *


class Hypre(AutotoolsPackage, CudaPackage, ROCmPackage):
    """Hypre is a library of high performance preconditioners that
       features parallel multigrid methods for both structured and
       unstructured grid problems."""

    homepage = "https://computing.llnl.gov/project/linear_solvers/software.php"
    url      = "https://github.com/hypre-space/hypre/archive/v2.14.0.tar.gz"
    git      = "https://github.com/hypre-space/hypre.git"
    tags     = ['e4s', 'radiuss']

    maintainers = ['ulrikeyang', 'osborn9', 'balay']

    test_requires_compiler = True

    version('develop', branch='master')
    version('2.24.0', sha256='f480e61fc25bf533fc201fdf79ec440be79bb8117650627d1f25151e8be2fdb5')
    version('2.23.0', sha256='8a9f9fb6f65531b77e4c319bf35bfc9d34bf529c36afe08837f56b635ac052e2')
    version('2.22.1', sha256='c1e7761b907c2ee0098091b69797e9be977bff8b7fd0479dc20cad42f45c4084')
    version('2.22.0', sha256='2c786eb5d3e722d8d7b40254f138bef4565b2d4724041e56a8fa073bda5cfbb5')
    version('2.21.0', sha256='e380f914fe7efe22afc44cdf553255410dc8a02a15b2e5ebd279ba88817feaf5')
    version('2.20.0', sha256='5be77b28ddf945c92cde4b52a272d16fb5e9a7dc05e714fc5765948cba802c01')
    version('2.19.0', sha256='466b19d8a86c69989a237f6f03f20d35c0c63a818776d2cd071b0a084cffeba5')
    version('2.18.2', sha256='28007b5b584eaf9397f933032d8367788707a2d356d78e47b99e551ab10cc76a')
    version('2.18.1', sha256='220f9c4ad024e815add8dad8950eaa2d8f4f231104788cf2a3c5d9da8f94ba6e')
    version('2.18.0', sha256='62591ac69f9cc9728bd6d952b65bcadd2dfe52b521081612609804a413f49b07')
    version('2.17.0', sha256='4674f938743aa29eb4d775211b13b089b9de84bfe5e9ea00c7d8782ed84a46d7')
    version('2.16.0', sha256='33f8a27041e697343b820d0426e74694670f955e21bbf3fcb07ee95b22c59e90')
    version('2.15.1', sha256='50d0c0c86b4baad227aa9bdfda4297acafc64c3c7256c27351f8bae1ae6f2402')
    version('2.15.0', sha256='2d597472b473964210ca9368b2cb027510fff4fa2193a8c04445e2ed4ff63045')
    version('2.14.0', sha256='705a0c67c68936bb011c50e7aa8d7d8b9693665a9709b584275ec3782e03ee8c')
    version('2.13.0', sha256='3979602689c3b6e491c7cf4b219cfe96df5a6cd69a5302ccaa8a95ab19064bad')
    version('2.12.1', sha256='824841a60b14167a0051b68fdb4e362e0207282348128c9d0ca0fd2c9848785c')
    version('2.11.2', sha256='25b6c1226411593f71bb5cf3891431afaa8c3fd487bdfe4faeeb55c6fdfb269e')
    version('2.11.1', sha256='6bb2ff565ff694596d0e94d0a75f0c3a2cd6715b8b7652bc71feb8698554db93')
    version('2.10.1', sha256='a4a9df645ebdc11e86221b794b276d1e17974887ead161d5050aaf0b43bb183a')
    version('2.10.0b', sha256='b55dbdc692afe5a00490d1ea1c38dd908dae244f7bdd7faaf711680059824c11')

    # Versions 2.13.0 and later can be patched to build shared
    # libraries on Darwin; the patch for this capability does not
    # apply to version 2.12.1 and earlier due to changes in the build system
    # between versions 2.12.1 and 2.13.0.
    variant('shared', default=(sys.platform != 'darwin'),
            description="Build shared library (disables static library)")
    # Use internal SuperLU routines for FEI - version 2.12.1 and below
    variant('internal-superlu', default=False,
            description="Use internal SuperLU routines")
    variant('superlu-dist', default=False,
            description='Activates support for SuperLU_Dist library')
    variant('int64', default=False,
            description="Use 64bit integers")
    variant('mixedint', default=False,
            description="Use 64bit integers while reducing memory use")
    variant('complex', default=False, description='Use complex values')
    variant('mpi', default=True, description='Enable MPI support')
    variant('openmp', default=False, description='Enable OpenMP support')
    variant('debug', default=False,
            description='Build debug instead of optimized version')
    variant('unified-memory', default=False, description='Use unified memory')
    variant('fortran', default=True,
            description='Enables fortran bindings')
    variant('gptune', default=False,
            description='Add the GPTune hookup code')

    # Patch to add gptune hookup codes
    patch('ij_gptune.patch', when='+gptune@2.19.0')

    # Patch to add ppc64le in config.guess
    patch('ibm-ppc64le.patch', when='@:2.11.1')

    # Patch to build shared libraries on Darwin
    patch('darwin-shared-libs-for-hypre-2.13.0.patch', when='+shared@2.13.0 platform=darwin')
    patch('darwin-shared-libs-for-hypre-2.14.0.patch', when='+shared@2.14.0 platform=darwin')
    patch('superlu-dist-link-2.15.0.patch', when='+superlu-dist @2.15:2.16.0')
    patch('superlu-dist-link-2.14.0.patch', when='+superlu-dist @:2.14.0')
    patch('hypre21800-compat.patch', when='@2.18.0')
    # Patch to get config flags right
    patch('detect-compiler.patch', when='@2.15.0:2.20.0')

    depends_on("mpi", when='+mpi')
    depends_on("blas")
    depends_on("lapack")
    depends_on('superlu-dist', when='+superlu-dist+mpi')

    conflicts('+cuda', when='+int64')
    conflicts('+rocm', when='+int64')
    conflicts('+rocm', when='@:2.20')
    conflicts('+unified-memory', when='~cuda~rocm')
    conflicts('+gptune', when='~mpi')

    # Patch to build shared libraries on Darwin does not apply to
    # versions before 2.13.0
    conflicts("+shared@:2.12 platform=darwin")

    # Conflicts
    # Option added in v2.13.0
    conflicts('+superlu-dist', when='@:2.12')

    # Internal SuperLU Option removed in v2.13.0
    conflicts('+internal-superlu', when='@2.13.0:')

    # Option added in v2.16.0
    conflicts('+mixedint', when='@:2.15')

    configure_directory = 'src'

    def url_for_version(self, version):
        if version >= Version('2.12.0'):
            url = 'https://github.com/hypre-space/hypre/archive/v{0}.tar.gz'
        else:
            url = 'http://computing.llnl.gov/project/linear_solvers/download/hypre-{0}.tar.gz'

        return url.format(version)

    def configure_args(self):
        spec = self.spec
        # Note: --with-(lapack|blas)_libs= needs space separated list of names
        lapack = spec['lapack'].libs
        blas = spec['blas'].libs

        configure_args = [
            '--prefix=%s' % prefix,
            '--with-lapack-libs=%s' % ' '.join(lapack.names),
            '--with-lapack-lib-dirs=%s' % ' '.join(lapack.directories),
            '--with-blas-libs=%s' % ' '.join(blas.names),
            '--with-blas-lib-dirs=%s' % ' '.join(blas.directories)
        ]

        if '+mpi' in spec:
            os.environ['CC'] = spec['mpi'].mpicc
            os.environ['CXX'] = spec['mpi'].mpicxx
            if '+fortran' in spec:
                os.environ['F77'] = spec['mpi'].mpif77
            configure_args.append('--with-MPI')
            configure_args.append('--with-MPI-lib-dirs={0}'.format(
                spec['mpi'].prefix.lib))
            configure_args.append('--with-MPI-include={0}'.format(
                spec['mpi'].prefix.include))
        else:
            configure_args.append('--without-MPI')

        configure_args.extend(self.with_or_without('openmp'))

        if '+int64' in spec:
            configure_args.append('--enable-bigint')
        else:
            configure_args.append('--disable-bigint')

        configure_args.extend(self.enable_or_disable('mixedint'))

        configure_args.extend(self.enable_or_disable('complex'))

        if '+shared' in spec:
            configure_args.append("--enable-shared")

        if '~internal-superlu' in spec:
            configure_args.append("--without-superlu")
            # MLI and FEI do not build without superlu on Linux
            configure_args.append("--without-mli")
            configure_args.append("--without-fei")

        if '+superlu-dist' in spec:
            configure_args.append('--with-dsuperlu-include=%s' %
                                  spec['superlu-dist'].prefix.include)
            configure_args.append('--with-dsuperlu-lib=%s' %
                                  spec['superlu-dist'].libs)
            configure_args.append('--with-dsuperlu')

        configure_args.extend(self.enable_or_disable('debug'))

        if '+cuda' in spec:
            configure_args.extend([
                '--with-cuda',
                '--enable-curand',
                '--enable-cusparse',
            ])
            cuda_arch_vals = spec.variants['cuda_arch'].value
            if cuda_arch_vals:
                cuda_arch_sorted = list(sorted(cuda_arch_vals, reverse=True))
                cuda_arch = cuda_arch_sorted[0]
                configure_args.append('--with-gpu-arch={0}'.format(cuda_arch))
            # New in 2.21.0: replaces --enable-cub
            if '@2.21.0:' in spec:
                configure_args.append('--enable-device-memory-pool')
                configure_args.append('--with-cuda-home={0}'.format(
                    spec['cuda'].prefix))
            else:
                configure_args.append('--enable-cub')
        else:
            configure_args.extend([
                '--without-cuda',
                '--disable-curand',
                '--disable-cusparse',
            ])
            if '@:2.20.99' in spec:
                configure_args.append('--disable-cub')

        if '+rocm' in spec:
            configure_args.extend([
                '--with-hip',
                '--enable-rocrand',
                '--enable-rocsparse',
            ])
            rocm_arch_vals = spec.variants['amdgpu_target'].value
            if rocm_arch_vals:
                rocm_arch_sorted = list(sorted(rocm_arch_vals, reverse=True))
                rocm_arch = rocm_arch_sorted[0]
                configure_args.append('--with-gpu-arch={0}'.format(rocm_arch))
        else:
            configure_args.extend([
                '--without-hip',
                '--disable-rocrand',
                '--disable-rocsparse',
            ])

        if '+unified-memory' in spec:
            configure_args.append('--enable-unified-memory')

        configure_args.extend(self.enable_or_disable('fortran'))

        return configure_args

    def setup_build_environment(self, env):
        spec = self.spec
        if '+mpi' in spec:
            env.set('CC', spec['mpi'].mpicc)
            env.set('CXX', spec['mpi'].mpicxx)
            if '+fortran' in spec:
                env.set('F77', spec['mpi'].mpif77)

        if '+cuda' in spec:
            env.set('CUDA_HOME', spec['cuda'].prefix)
            env.set('CUDA_PATH', spec['cuda'].prefix)
            # In CUDA builds hypre currently doesn't handle flags correctly
            env.append_flags(
                'CXXFLAGS', '-O2' if '~debug' in spec else '-g')

        if '+rocm' in spec:
            # As of 2022/04/05, the following are set by 'llvm-amdgpu' and
            # override hypre's default flags, so we unset them.
            env.unset('CFLAGS')
            env.unset('CXXFLAGS')

    def build(self, spec, prefix):
        with working_dir("src"):
            make()

    def install(self, spec, prefix):
        # Hypre's source is staged under ./src so we'll have to manually
        # cd into it.
        with working_dir("src"):
            if self.run_tests:
                make("check")
                make("test")
                Executable(join_path('test', 'ij'))()
                sstruct = Executable(join_path('test', 'struct'))
                sstruct()
                sstruct('-in', 'test/sstruct.in.default', '-solver', '40',
                        '-rhsone')
            make("install")
            if '+gptune' in self.spec:
                make("test")
                self.run_test('mkdir', options=['-p', self.prefix.bin])
                self.run_test('cp', options=['test/ij', self.prefix.bin + '/.'])

    extra_install_tests = join_path('src', 'examples')

    @run_after('install')
    def cache_test_sources(self):
        self.cache_extra_test_sources(self.extra_install_tests)

    @property
    def _cached_tests_work_dir(self):
        """The working directory for cached test sources."""
        return join_path(self.test_suite.current_test_cache_dir,
                         self.extra_install_tests)

    def test(self):
        """Perform smoke test on installed HYPRE package."""
        if '+mpi' not in self.spec:
            print('Skipping: HYPRE must be installed with +mpi to run tests')
            return

        # Build copied and cached test examples
        self.run_test('make',
                      ['HYPRE_DIR={0}'.format(self.prefix), 'bigint'],
                      purpose='test: building selected examples',
                      work_dir=self._cached_tests_work_dir)

        # Run the examples built above
        for exe in ['./ex5big', './ex15big']:
            self.run_test(exe, [], [], installed=False,
                          purpose='test: ensuring {0} runs'.format(exe),
                          skip_missing=True,
                          work_dir=self._cached_tests_work_dir)

    @property
    def headers(self):
        """Export the main hypre header, HYPRE.h; all other headers can be found
        in the same directory.
        Sample usage: spec['hypre'].headers.cpp_flags
        """
        hdrs = find_headers('HYPRE', self.prefix.include, recursive=False)
        return hdrs or None

    @property
    def libs(self):
        """Export the hypre library.
        Sample usage: spec['hypre'].libs.ld_flags
        """
        is_shared = '+shared' in self.spec
        libs = find_libraries('libHYPRE', root=self.prefix, shared=is_shared,
                              recursive=True)
        return libs or None
