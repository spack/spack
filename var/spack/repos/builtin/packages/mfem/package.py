# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import shutil


class Mfem(Package):
    """Free, lightweight, scalable C++ library for finite element methods."""

    tags = ['FEM', 'finite elements', 'high-order', 'AMR', 'HPC']

    homepage = 'http://www.mfem.org'
    git      = 'https://github.com/mfem/mfem.git'

    maintainers = ['goxberry', 'tzanio', 'markcmiller86', 'acfisher',
                   'v-dobrev']

    # Recommended mfem builds to test when updating this file: see the shell
    # script 'test_builds.sh' in the same directory as this file.

    # mfem is downloaded from a URL shortener at request of upstream
    # author Tzanio Kolev <tzanio@llnl.gov>.  See here:
    #     https://github.com/mfem/mfem/issues/53
    #
    # The following procedure should be used to verify security when a
    # new version is added:
    #
    # 1. Verify that no checksums on old versions have changed.
    #
    # 2. Verify that the shortened URL for the new version is listed at:
    #    http://mfem.org/download/
    #
    # 3. Use http://getlinkinfo.com or similar to verify that the
    #    underling download link for the latest version comes has the
    #    prefix: http://mfem.github.io/releases
    #
    # If this quick verification procedure fails, additional discussion
    # will be required to verify the new version.

    # 'develop' is a special version that is always larger (or newer) than any
    # other version.
    version('develop', branch='master')

    # Tagged development version used by the laghos package:
    version('3.4.1-laghos-v2.0', tag='laghos-v2.0')

    version('3.4.0',
            '4e73e4fe0482636de3c5dc983cd395839a83cb16f6f509bd88b053e8b3858e05',
            url='https://bit.ly/mfem-3-4', extension='.tar.gz',
            preferred=True)

    version('3.3.2',
            'b70fa3c5080b9ec514fc05f4a04ff74322b99ac4ecd6d99c229f0ed5188fc0ce',
            url='https://goo.gl/Kd7Jk8', extension='.tar.gz')

    # Tagged development version used by the laghos package:
    version('3.3.1-laghos-v1.0', tag='laghos-v1.0')

    version('3.3',
            'b17bd452593aada93dc0fee748fcfbbf4f04ce3e7d77fdd0341cc9103bcacd0b',
            url='http://goo.gl/Vrpsns', extension='.tar.gz')

    version('3.2',
            '2938c3deed4ec4f7fd5b5f5cfe656845282e86e2dcd477d292390058b7b94340',
            url='http://goo.gl/Y9T75B', extension='.tar.gz')

    version('3.1',
            '841ea5cf58de6fae4de0f553b0e01ebaab9cd9c67fa821e8a715666ecf18fc57',
            url='http://goo.gl/xrScXn', extension='.tar.gz')

    variant('static', default=True,
            description='Build static library')
    variant('shared', default=False,
            description='Build shared library')
    variant('mpi', default=True,
            description='Enable MPI parallelism')
    # Can we make the default value for 'metis' to depend on the 'mpi' value?
    variant('metis', default=True,
            description='Enable METIS support')
    # TODO: The 'hypre' variant is the same as 'mpi', we may want to remove it.
    #       For now, keep the 'hypre' variant while ignoring its setting. This
    #       is done to preserve compatibility with other packages that refer to
    #       it, e.g. xSDK.
    variant('hypre', default=True,
            description='Required for MPI parallelism')
    variant('openmp', default=False,
            description='Enable OpenMP parallelism')
    variant('threadsafe', default=False,
            description=('Enable thread safe features.'
                         ' Required for OpenMP.'
                         ' May cause minor performance issues.'))
    variant('superlu-dist', default=False,
            description='Enable MPI parallel, sparse direct solvers')
    # Placeholder for STRUMPACK, support added in mfem v3.3.2:
    # variant('strumpack', default=False,
    #       description='Enable support for STRUMPACK')
    variant('suite-sparse', default=False,
            description='Enable serial, sparse direct solvers')
    variant('petsc', default=False,
            description='Enable PETSc solvers, preconditioners, etc.')
    variant('sundials', default=False,
            description='Enable Sundials time integrators')
    variant('pumi', default=False,
            description='Enable functionality based on PUMI')
    variant('mpfr', default=False,
            description='Enable precise, 1D quadrature rules')
    variant('lapack', default=False,
            description='Use external blas/lapack routines')
    variant('debug', default=False,
            description='Build debug instead of optimized version')
    variant('netcdf', default=False,
            description='Enable Cubit/Genesis reader')
    variant('conduit', default=False,
            description='Enable binary data I/O using Conduit')
    variant('gzstream', default=True,
            description='Support zip\'d streams for I/O')
    variant('gnutls', default=False,
            description='Enable secure sockets using GnuTLS')
    variant('libunwind', default=False,
            description='Enable backtrace on error support using Libunwind')
    variant('timer', default='auto',
            values=('auto', 'std', 'posix', 'mac', 'mpi'),
            description='Timing functions to use in mfem::StopWatch')
    variant('examples', default=False,
            description='Build and install examples')
    variant('miniapps', default=False,
            description='Build and install miniapps')

    conflicts('+shared', when='@:3.3.2')
    conflicts('~static~shared')
    conflicts('~threadsafe', when='+openmp')

    conflicts('+netcdf', when='@:3.1')
    conflicts('+superlu-dist', when='@:3.1')
    conflicts('+gnutls', when='@:3.1')
    conflicts('+gzstream', when='@:3.2')
    conflicts('+mpfr', when='@:3.2')
    conflicts('+petsc', when='@:3.2')
    conflicts('+sundials', when='@:3.2')
    conflicts('+pumi', when='@:3.3.2')
    conflicts('timer=mac', when='@:3.3.0')
    conflicts('timer=mpi', when='@:3.3.0')
    conflicts('~metis+mpi', when='@:3.3.0')
    conflicts('+metis~mpi', when='@:3.3.0')
    conflicts('+conduit', when='@:3.3.2')

    conflicts('+superlu-dist', when='~mpi')
    conflicts('+petsc', when='~mpi')
    conflicts('+pumi', when='~mpi')
    conflicts('timer=mpi', when='~mpi')

    conflicts('+pumi', when='+shared')

    depends_on('mpi', when='+mpi')
    depends_on('hypre@2.10.0:2.13.999', when='@:3.3.999+mpi')
    depends_on('hypre', when='@3.4:+mpi')

    depends_on('metis', when='+metis')
    depends_on('blas', when='+lapack')
    depends_on('lapack', when='+lapack')

    depends_on('sundials@2.7.0', when='@:3.3.0+sundials~mpi')
    depends_on('sundials@2.7.0+mpi+hypre', when='@:3.3.0+sundials+mpi')
    depends_on('sundials@2.7.0:', when='@3.3.2:+sundials~mpi')
    depends_on('sundials@2.7.0:+mpi+hypre', when='@3.3.2:+sundials+mpi')
    depends_on('pumi', when='+pumi')
    depends_on('suite-sparse', when='+suite-sparse')
    depends_on('superlu-dist', when='+superlu-dist')
    # The PETSc tests in MFEM will fail if PETSc is not configured with
    # SuiteSparse and MUMPS. On the other hand, if we require the variants
    # '+suite-sparse+mumps' of PETSc, the xsdk package concretization fails.
    depends_on('petsc@3.8:+mpi+double+hypre', when='+petsc')
    # Recommended when building outside of xsdk:
    # depends_on('petsc@3.8:+mpi+double+hypre+suite-sparse+mumps',
    #            when='+petsc')
    depends_on('mpfr', when='+mpfr')
    depends_on('netcdf', when='+netcdf')
    depends_on('unwind', when='+libunwind')
    depends_on('zlib', when='+gzstream')
    depends_on('gnutls', when='+gnutls')
    depends_on('conduit@0.3.1:,master:', when='+conduit')
    depends_on('conduit+mpi', when='+conduit+mpi')

    patch('mfem_ppc_build.patch', when='@3.2:3.3.0 arch=ppc64le')
    patch('mfem-3.4.patch', when='@3.4.0')
    patch('mfem-3.3-3.4-petsc-3.9.patch',
          when='@3.3.0:3.4.0 +petsc ^petsc@3.9.0:')

    phases = ['configure', 'build', 'install']

    def setup_environment(self, spack_env, run_env):
        spack_env.unset('MFEM_DIR')
        spack_env.unset('MFEM_BUILD_DIR')

    #
    # Note: Although MFEM does support CMake configuration, MFEM
    # development team indicates that vanilla GNU Make is the
    # preferred mode of configuration of MFEM and the mode most
    # likely to be up to date in supporting *all* of MFEM's
    # configuration options. So, don't use CMake
    #
    def configure(self, spec, prefix):

        def yes_no(varstr):
            return 'YES' if varstr in self.spec else 'NO'

        # We need to add rpaths explicitly to allow proper export of link flags
        # from within MFEM.

        # Similar to spec[pkg].libs.ld_flags but prepends rpath flags too.
        def ld_flags_from_library_list(libs_list):
            flags = ['-Wl,-rpath,%s' % dir for dir in libs_list.directories]
            flags += [libs_list.ld_flags]
            return ' '.join(flags)

        def ld_flags_from_dirs(pkg_dirs_list, pkg_libs_list):
            flags = ['-Wl,-rpath,%s' % dir for dir in pkg_dirs_list]
            flags += ['-L%s' % dir for dir in pkg_dirs_list]
            flags += ['-l%s' % lib for lib in pkg_libs_list]
            return ' '.join(flags)

        def find_optional_library(name, prefix):
            for shared in [True, False]:
                for path in ['lib64', 'lib']:
                    lib = find_libraries(name, join_path(prefix, path),
                                         shared=shared, recursive=False)
                    if lib:
                        return lib
            return LibraryList([])

        metis5_str = 'NO'
        if ('+metis' in spec) and spec['metis'].satisfies('@5:'):
            metis5_str = 'YES'

        options = [
            'PREFIX=%s' % prefix,
            'MFEM_USE_MEMALLOC=YES',
            'MFEM_DEBUG=%s' % yes_no('+debug'),
            # NOTE: env['CXX'] is the spack c++ compiler wrapper. The real
            # compiler is defined by env['SPACK_CXX'].
            'CXX=%s' % env['CXX'],
            'MFEM_USE_LIBUNWIND=%s' % yes_no('+libunwind'),
            'MFEM_USE_GZSTREAM=%s' % yes_no('+gzstream'),
            'MFEM_USE_METIS=%s' % yes_no('+metis'),
            'MFEM_USE_METIS_5=%s' % metis5_str,
            'MFEM_THREAD_SAFE=%s' % yes_no('+threadsafe'),
            'MFEM_USE_MPI=%s' % yes_no('+mpi'),
            'MFEM_USE_LAPACK=%s' % yes_no('+lapack'),
            'MFEM_USE_SUPERLU=%s' % yes_no('+superlu-dist'),
            'MFEM_USE_SUITESPARSE=%s' % yes_no('+suite-sparse'),
            'MFEM_USE_SUNDIALS=%s' % yes_no('+sundials'),
            'MFEM_USE_PETSC=%s' % yes_no('+petsc'),
            'MFEM_USE_PUMI=%s' % yes_no('+pumi'),
            'MFEM_USE_NETCDF=%s' % yes_no('+netcdf'),
            'MFEM_USE_MPFR=%s' % yes_no('+mpfr'),
            'MFEM_USE_GNUTLS=%s' % yes_no('+gnutls'),
            'MFEM_USE_OPENMP=%s' % yes_no('+openmp'),
            'MFEM_USE_CONDUIT=%s' % yes_no('+conduit')]

        cxxflags = spec.compiler_flags['cxxflags']
        if cxxflags:
            # The cxxflags are set by the spack c++ compiler wrapper. We also
            # set CXXFLAGS explicitly, for clarity, and to properly export the
            # cxxflags in the variable MFEM_CXXFLAGS in config.mk.
            options += ['CXXFLAGS=%s' % ' '.join(cxxflags)]

        if '~static' in spec:
            options += ['STATIC=NO']
        if '+shared' in spec:
            options += ['SHARED=YES', 'PICFLAG=%s' % self.compiler.pic_flag]

        if '+mpi' in spec:
            options += ['MPICXX=%s' % spec['mpi'].mpicxx]
            hypre = spec['hypre']
            # The hypre package always links with 'blas' and 'lapack'.
            all_hypre_libs = hypre.libs + hypre['lapack'].libs + \
                hypre['blas'].libs
            options += [
                'HYPRE_OPT=-I%s' % hypre.prefix.include,
                'HYPRE_LIB=%s' % ld_flags_from_library_list(all_hypre_libs)]

        if '+metis' in spec:
            options += [
                'METIS_OPT=-I%s' % spec['metis'].prefix.include,
                'METIS_LIB=%s' %
                ld_flags_from_dirs([spec['metis'].prefix.lib], ['metis'])]

        if '+lapack' in spec:
            lapack_blas = spec['lapack'].libs + spec['blas'].libs
            options += [
                # LAPACK_OPT is not used
                'LAPACK_LIB=%s' % ld_flags_from_library_list(lapack_blas)]

        if '+superlu-dist' in spec:
            lapack_blas = spec['lapack'].libs + spec['blas'].libs
            options += [
                'SUPERLU_OPT=-I%s -I%s' %
                (spec['superlu-dist'].prefix.include,
                 spec['parmetis'].prefix.include),
                'SUPERLU_LIB=-L%s -L%s -lsuperlu_dist -lparmetis %s' %
                (spec['superlu-dist'].prefix.lib,
                 spec['parmetis'].prefix.lib,
                 ld_flags_from_library_list(lapack_blas))]

        if '+suite-sparse' in spec:
            ss_spec = 'suite-sparse:' + self.suitesparse_components
            options += [
                'SUITESPARSE_OPT=-I%s' % spec[ss_spec].prefix.include,
                'SUITESPARSE_LIB=%s' %
                ld_flags_from_library_list(spec[ss_spec].libs)]

        if '+sundials' in spec:
            sun_spec = 'sundials:' + self.sundials_components
            options += [
                'SUNDIALS_OPT=%s' % spec[sun_spec].headers.cpp_flags,
                'SUNDIALS_LIB=%s' %
                ld_flags_from_library_list(spec[sun_spec].libs)]

        if '+petsc' in spec:
            # options += ['PETSC_DIR=%s' % spec['petsc'].prefix]
            options += [
                'PETSC_OPT=%s' % spec['petsc'].headers.cpp_flags,
                'PETSC_LIB=%s' %
                ld_flags_from_library_list(spec['petsc'].libs)]

        if '+pumi' in spec:
            options += ['PUMI_DIR=%s' % spec['pumi'].prefix]

        if '+netcdf' in spec:
            options += [
                'NETCDF_OPT=-I%s' % spec['netcdf'].prefix.include,
                'NETCDF_LIB=%s' %
                ld_flags_from_dirs([spec['netcdf'].prefix.lib], ['netcdf'])]

        if '+gzstream' in spec:
            if "@:3.3.2" in spec:
                options += ['ZLIB_DIR=%s' % spec['zlib'].prefix]
            else:
                options += [
                    'ZLIB_OPT=-I%s' % spec['zlib'].prefix.include,
                    'ZLIB_LIB=%s' %
                    ld_flags_from_library_list(spec['zlib'].libs)]

        if '+mpfr' in spec:
            options += [
                'MPFR_OPT=-I%s' % spec['mpfr'].prefix.include,
                'MPFR_LIB=%s' %
                ld_flags_from_dirs([spec['mpfr'].prefix.lib], ['mpfr'])]

        if '+gnutls' in spec:
            options += [
                'GNUTLS_OPT=-I%s' % spec['gnutls'].prefix.include,
                'GNUTLS_LIB=%s' %
                ld_flags_from_dirs([spec['gnutls'].prefix.lib], ['gnutls'])]

        if '+libunwind' in spec:
            libunwind = spec['unwind']
            headers = find_headers('libunwind', libunwind.prefix.include)
            headers.add_macro('-g')
            libs = find_optional_library('libunwind', libunwind.prefix)
            # When mfem uses libunwind, it also needs 'libdl'.
            libs += LibraryList(find_system_libraries('libdl'))
            options += [
                'LIBUNWIND_OPT=%s' % headers.cpp_flags,
                'LIBUNWIND_LIB=%s' % ld_flags_from_library_list(libs)]

        if '+openmp' in spec:
            options += ['OPENMP_OPT=%s' % self.compiler.openmp_flag]

        timer_ids = {'std': '0', 'posix': '2', 'mac': '4', 'mpi': '6'}
        timer = spec.variants['timer'].value
        if timer != 'auto':
            options += ['MFEM_TIMER_TYPE=%s' % timer_ids[timer]]

        if '+conduit' in spec:
            conduit = spec['conduit']
            headers = HeaderList(find(conduit.prefix.include, 'conduit.hpp',
                                      recursive=True))
            conduit_libs = ['libconduit', 'libconduit_relay',
                            'libconduit_blueprint']
            libs = find_libraries(conduit_libs, conduit.prefix.lib,
                                  shared=('+shared' in conduit))
            libs += LibraryList(find_system_libraries('libdl'))
            if '+hdf5' in conduit:
                hdf5 = conduit['hdf5']
                headers += find_headers('hdf5', hdf5.prefix.include)
                libs += hdf5.libs
            options += [
                'CONDUIT_OPT=%s' % headers.cpp_flags,
                'CONDUIT_LIB=%s' % ld_flags_from_library_list(libs)]

        make('config', *options, parallel=False)
        make('info', parallel=False)

    def build(self, spec, prefix):
        make('lib')

    @run_after('build')
    def check_or_test(self):
        # Running 'make check' or 'make test' may fail if MFEM_MPIEXEC or
        # MFEM_MPIEXEC_NP are not set appropriately.
        if not self.run_tests:
            # check we can build ex1 (~mpi) or ex1p (+mpi).
            make('-C', 'examples', 'ex1p' if ('+mpi' in self.spec) else 'ex1',
                 parallel=False)
            # make('check', parallel=False)
        else:
            make('all')
            make('test', parallel=False)

    def install(self, spec, prefix):
        make('install', parallel=False)

        # TODO: The way the examples and miniapps are being installed is not
        # perfect. For example, the makefiles do not work.

        install_em = ('+examples' in spec) or ('+miniapps' in spec)
        if install_em and ('+shared' in spec):
            make('examples/clean', 'miniapps/clean')
            # This is a hack to get the examples and miniapps to link with the
            # installed shared mfem library:
            with working_dir('config'):
                os.rename('config.mk', 'config.mk.orig')
                copy(str(self.config_mk), 'config.mk')
                shutil.copystat('config.mk.orig', 'config.mk')

        prefix_share = join_path(prefix, 'share', 'mfem')

        if '+examples' in spec:
            make('examples')
            install_tree('examples', join_path(prefix_share, 'examples'))

        if '+miniapps' in spec:
            make('miniapps')
            install_tree('miniapps', join_path(prefix_share, 'miniapps'))

        if install_em:
            install_tree('data', join_path(prefix_share, 'data'))

    @property
    def suitesparse_components(self):
        """Return the SuiteSparse components needed by MFEM."""
        ss_comps = 'umfpack,cholmod,colamd,amd,camd,ccolamd,suitesparseconfig'
        if self.spec.satisfies('@3.2:'):
            ss_comps = 'klu,btf,' + ss_comps
        return ss_comps

    @property
    def sundials_components(self):
        """Return the SUNDIALS components needed by MFEM."""
        sun_comps = 'arkode,cvode,nvecserial,kinsol'
        if '+mpi' in self.spec:
            sun_comps += ',nvecparhyp,nvecparallel'
        return sun_comps

    @property
    def headers(self):
        """Export the main mfem header, mfem.hpp.
        """
        hdrs = HeaderList(find(self.prefix.include, 'mfem.hpp',
                               recursive=False))
        return hdrs or None

    @property
    def libs(self):
        """Export the mfem library file.
        """
        libs = find_libraries('libmfem', root=self.prefix.lib,
                              shared=('+shared' in self.spec), recursive=False)
        return libs or None

    @property
    def config_mk(self):
        """Export the location of the config.mk file.
           This property can be accessed using spec['mfem'].package.config_mk
        """
        dirs = [self.prefix, self.prefix.share.mfem]
        for d in dirs:
            f = join_path(d, 'config.mk')
            if os.access(f, os.R_OK):
                return FileList(f)
        return FileList(find(self.prefix, 'config.mk', recursive=True))

    @property
    def test_mk(self):
        """Export the location of the test.mk file.
           This property can be accessed using spec['mfem'].package.test_mk.
           In version 3.3.2 and newer, the location of test.mk is also defined
           inside config.mk, variable MFEM_TEST_MK.
        """
        dirs = [self.prefix, self.prefix.share.mfem]
        for d in dirs:
            f = join_path(d, 'test.mk')
            if os.access(f, os.R_OK):
                return FileList(f)
        return FileList(find(self.prefix, 'test.mk', recursive=True))
