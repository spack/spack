# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spectre(CMakePackage):
    """The SpECTRE numerical relativity code.

    SpECTRE is an open-source code for multi-scale, multi-physics problems in
    astrophysics and gravitational physics. In the future, we hope that it can
    be applied to problems across discipline boundaries in fluid dynamics,
    geoscience, plasma physics, nuclear physics, and engineering. It runs at
    petascale and is designed for future exascale computers.

    SpECTRE is being developed in support of our collaborative Simulating
    eXtreme Spacetimes (SXS) research program into the multi-messenger
    astrophysics of neutron star mergers, core-collapse supernovae, and
    gamma-ray bursts."""

    homepage = "https://spectre-code.com"
    url = "https://github.com/sxs-collaboration/spectre/archive/v2021.12.15.tar.gz"
    git = "https://github.com/sxs-collaboration/spectre.git"

    maintainers = ['nilsvu']

    generator = 'Ninja'

    version('develop', branch='develop')
    version('2022.02.17', sha256='4bc2949453a35699090efc2bb71b8bd2b951909e0f02d0f8c8af255d1668e63f')
    version('2022.02.08', sha256='996275536c990a6d49cd61f207c04ad771a1449506f38507afc35f95b29d4cf1')
    version('2022.01.03', sha256='872a0d152c19864ad543ddcc585ce30baaad4185c2617c13463d780175cbde5f')
    version('2021.12.15', sha256='4bfe9e27412e263ffdc6fcfcb84011f16d34a9fdd633ad7fc84a34c898f67e5c')

    # Configuration variants
    variant('executables',
            values=any_combination_of(
                # CCE
                'CharacteristicExtract', 'ReduceCceWorldtube',
                # Elliptic / initial data
                'SolvePoisson1D', 'SolvePoisson2D', 'SolvePoisson3D',
                'SolveElasticity2D', 'SolveElasticity3D', 'SolveXcts',
                # Tools
                'ExportCoordinates1D', 'ExportCoordinates2D',
                'ExportCoordinates3D',
            ),
            description="Executables to install")
    variant('python', default=False, description="Build Python bindings")
    variant('doc', default=False, description="Build documentation")
    # Build type and debug symbols:
    # - Both Debug and Release builds have debug symbols enabled by default in
    #   the SpECTRE build system, so we can view backtraces, etc., when
    #   production code fails.
    variant('build_type', values=('Debug', 'Release'),
            default='Release', description='CMake build type')
    # - Allow disabling debug symbols to reduce memory usage and executable size
    variant('debug_symbols', default=True,
            description="Build with debug symbols")
    variant('shared',
            default=False,
            description="Build shared libraries instead of static")
    variant('memory_allocator',
            values=('system', 'jemalloc'),
            multi=False,
            default='system',
            description="Which memory allocator to use")
    variant('formaline',
            default=True,
            description=("Write the source tree into simulation output files "
                         "to increase reproducibility of results"))
    variant('profiling',
            default=False,
            description="Enable options to make profiling SpECTRE easier")

    # Compiler support
    conflicts('%gcc@:6')
    conflicts('%clang@:7')
    conflicts('%apple-clang@:10')

    # Build dependencies
    depends_on('cmake@3.12:', type='build')
    depends_on('ninja', type='build')
    depends_on('python@2.7:', type='build')

    # Link dependencies
    depends_on('charmpp@6.10.2:')
    depends_on('blaze@3.8')
    depends_on('boost@1.60:+math+program_options')
    depends_on('brigand@master')
    depends_on('gsl')
    depends_on('hdf5')
    depends_on('jemalloc', when='memory_allocator=jemalloc')
    depends_on('libsharp~mpi~openmp')
    depends_on('libxsmm@1.16.1:')
    depends_on('blas')
    depends_on('lapack')
    depends_on('yaml-cpp@0.6:')

    # Test dependencies
    depends_on('catch2@2.8:', type='test')
    depends_on('py-numpy@1.10:', type='test')
    depends_on('py-scipy', type='test')
    depends_on('py-h5py', type='test')

    # Python bindings
    with when('+python'):
        extends('python')
        depends_on('python@3.7:', type=('build', 'run'))
        depends_on('py-pybind11@2.6:', type='build')
        depends_on('py-numpy@1.10:', type=('build', 'run'))
        depends_on('py-scipy', type=('build', 'run'))
        depends_on('py-matplotlib', type=('build', 'run'))
        depends_on('py-h5py', type=('build', 'run'))

    # Docs
    with when('+doc'):
        depends_on('doxygen', type='build')
        depends_on('perl', type='build', when="@2022.03.07:")
        depends_on('py-beautifulsoup4', type='build')
        depends_on('py-pybtex', type='build')
        depends_on('py-nbconvert', type='build', when="@2022.03.07:")

    # Incompatibilities
    # - Shared libs builds on macOS don't work before
    #   https://github.com/sxs-collaboration/spectre/pull/2680
    conflicts('+shared', when='@:2022.01.03 platform=darwin')
    # - Blaze with `BLAZE_BLAS_MODE` enabled doesn't work before
    #   https://github.com/sxs-collaboration/spectre/pull/3806 because it
    #   doesn't find the BLAS header. Also, we haven't tested Blaze with BLAS
    #   kernels before then.
    conflicts('^blaze+blas', when='@:2022.02.17')

    # These patches backport updates to the SpECTRE build system to earlier
    # releases, to support installing them with Spack. In particular, we try to
    # support releases associated with published papers, so their results are
    # reproducible.
    # - Backport installation of targets, based on upstream patch:
    #   https://github.com/sxs-collaboration/spectre/commit/fe3514117c8205dbf18c4d42ec17712e67d33251
    patch('install-pre-2022.01.03.patch', when='@:2022.01.03')
    # - Backport experimental support for Charm++ v7+
    patch(
        'https://github.com/sxs-collaboration/spectre/commit/a2203824ef38ec79a247703ae8cd215befffe391.patch',
        sha256='eb6094028530d9f28cb9c91a90b4af908cc537c8525fb4c81b11c74fd0354932',
        when='@:2022.01.03 ^charmpp@7.0.0:')
    # - Backport IWYU toggle to avoid CMake configuration issues
    patch(
        'https://github.com/sxs-collaboration/spectre/commit/cffeba1bc24bf7c00ec8bac710f02d3db36fa111.patch',
        sha256='912877d4f553adff8b6df8264c50600c1e6d5a9c3ad18be0b86c9d801c07699c',
        when='@:2022.01.03')
    # - Backport patch for Boost 1.77
    patch(
        'https://github.com/sxs-collaboration/spectre/commit/001fc190a6ec73ad6c19ada9444d04a2320f2b96.patch',
        sha256='bf539feb01d01e178889828dbbe5e990e8ee58c9e971d8634845c70a7cfb42a9',
        when='@:2022.01.03 ^boost@1.77:')
    # - Backport patch for Python 3.10 in tests
    patch(
        'https://github.com/sxs-collaboration/spectre/commit/82ff2c39cdae0ecc1e42bdf4564506a4ca869818.patch',
        sha256='5a5a3abf102e92812933e7318daabe2ca0a5a00d81d9663731c527e5dc6c8ced',
        when='@:2022.01.03 ^python@3.10:')
    # - Backport patch for hdf5+mpi
    patch(
        'https://github.com/sxs-collaboration/spectre/commit/eb887635f5e2b394ae2c7e96170e9d907eb315cf.patch',
        sha256='eb50b31af79d1e6b6535503bc30a9c5efd2ce36bd3638a2b3ab02af44bac6de3',
        when='@:2022.01.03 ^hdf5+mpi')
    # - Backport `BUILD_TESTING` toggle, based on upstream patch:
    #   https://github.com/sxs-collaboration/spectre/commit/79bed6cad6e95efadf48a5846f389e90801202d4
    patch('build-testing-pre-2022.01.03.patch', when='@:2022.01.03')
    # - Backport `PYTHONPATH` in CTest environment
    patch(
        'https://github.com/sxs-collaboration/spectre/commit/ada1d15d5963bd22581dd8966599e1529a99645d.patch',
        sha256='160d55bb2537ea8f3937cea59a9a0fd56a2bfef856bb7fd8e9dceb504c04836c',
        when='@:2022.01.03')
    # - Backport executable name CTest labels
    patch(
        'https://github.com/sxs-collaboration/spectre/commit/1b61e62a27b02b658cc6a74c4d46af1f5b5d0a4d.patch',
        sha256='07be176ca4dda74a2dd8e71c31dab638a9f3567c3a58eb7fddbfde001646fb8c',
        when='@:2022.01.03')
    # - Backport fix for PCH builds with Spack
    patch(
        'https://github.com/sxs-collaboration/spectre/commit/4bb3f25f905f83d8295a28a8036f6971dc4e75a2.patch',
        sha256='cd39217614a40f080d812e20220044aa8b26b9413324a7cd7a304e2378a2b426',
        when='@:2022.01.03')
    # - Backport installation of shared libs
    patch(
        'https://github.com/sxs-collaboration/spectre/commit/b7c54a2a20c6d62aae6b1c97e3468d4cd39ed6ad.patch',
        sha256='29ad44594ecfd6442a64d2cb57ed2d712cb8d93707c6bceea8030a9a2682b7ed',
        when='@:2022.01.03 +shared')
    # - Fix an issue with Boost pre v1.67
    patch(
        'https://github.com/sxs-collaboration/spectre/commit/b229e939f15362aca892d4480a9182daf88305d4.patch',
        sha256='06a41506d3652b5cb9127ae0e7e9b506f013bde695e478621a1540f46ed1e5bb',
        when='@2022.02.08 ^boost@:1.66')

    def cmake_args(self):
        args = [
            self.define('CHARM_ROOT', self.spec['charmpp'].prefix),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define('Python_EXECUTABLE', self.spec['python'].command.path),
            self.define_from_variant('BUILD_PYTHON_BINDINGS', 'python'),
            self.define('BUILD_TESTING', self.run_tests),
            self.define('USE_GIT_HOOKS', False),
            self.define('USE_IWYU', False),
            self.define_from_variant('USE_FORMALINE', 'formaline'),
            self.define_from_variant('MEMORY_ALLOCATOR').upper(),
            self.define_from_variant('ENABLE_PROFILING', 'profiling'),
            self.define('USE_PCH', True),
            self.define_from_variant('DEBUG_SYMBOLS'),
        ]
        # Allow for more time on slower machines
        if self.run_tests:
            if self.spec.satisfies('@:2022.01.03'):
                args.extend([
                    self.define('SPECTRE_INPUT_FILE_TEST_TIMEOUT_FACTOR', '10'),
                    self.define('SPECTRE_UNIT_TEST_TIMEOUT_FACTOR', '10'),
                    self.define('SPECTRE_PYTHON_TEST_TIMEOUT_FACTOR', '10'),
                ])
            else:
                args.append(self.define('SPECTRE_TEST_TIMEOUT_FACTOR', '10'))
        return args

    @property
    def build_targets(self):
        spec = self.spec
        targets = list(self.spec.variants['executables'].value)
        if 'none' in targets:
            targets.remove('none')
        if '+python' in spec:
            targets.append('all-pybindings')
        if '+doc' in spec:
            targets.append('doc')
        if self.run_tests:
            targets.append('unit-tests')
        if len(targets) == 0:
            raise InstallError("Specify at least one target to build. See "
                               "'spack info spectre' for available targets.")
        return targets

    @run_after('install')
    def install_docs(self):
        if '+doc' in self.spec:
            with working_dir(self.build_directory):
                install_tree(join_path('docs', 'html'), self.prefix.docs)

    @property
    def archive_files(self):
        # Archive the `BuildInfo.txt` file for debugging builds
        return super(Spectre, self).archive_files + [
            join_path(self.build_directory, 'BuildInfo.txt')
        ]

    def check(self):
        with working_dir(self.build_directory):
            # The test suite contains a lot of tests. We select only those
            # related to the targets that were specified.
            # - Unit tests
            ctest('--output-on-failure', '-L', 'unit')
            # - Input file tests for the specified executables
            for executable in self.spec.variants['executables'].value:
                if executable == 'none':
                    continue
                ctest('--output-on-failure', '-L', executable)
