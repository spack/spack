# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import llnl.util.tty as tty


class Qmcpack(CMakePackage):
    """QMCPACK, is a modern high-performance open-source Quantum Monte
       Carlo (QMC) simulation code."""

    # Package information
    homepage = "http://www.qmcpack.org/"
    git      = "https://github.com/QMCPACK/qmcpack.git"

    tags = ['ecp', 'ecp-apps']

    # This download method is untrusted, and is not recommended by the
    # Spack manual. However, it is easier to maintain because github hashes
    # can occasionally change.
    # NOTE: 12/19/2017 QMCPACK 3.0.0 does not build properly with Spack.
    version('develop')
    version('3.6.0', tag='v3.6.0')
    version('3.5.0', tag='v3.5.0')
    version('3.4.0', tag='v3.4.0')
    version('3.3.0', tag='v3.3.0')
    version('3.2.0', tag='v3.2.0')
    version('3.1.1', tag='v3.1.1')
    version('3.1.0', tag='v3.1.0')

    # These defaults match those in the QMCPACK manual
    variant('debug', default=False, description='Build debug version')
    variant('mpi', default=True, description='Build with MPI support')
    variant('phdf5', default=True, description='Build with parallel collective I/O')
    variant('cuda', default=False,
            description='Enable CUDA and GPU acceleration')
    variant('complex', default=False,
            description='Build the complex (general twist/k-point) version')
    variant('mixed', default=False,
            description='Build the mixed precision (mixture of single and '
                        'double precision) version for gpu and cpu')
    variant('soa', default=False,
            description='Build with Structure-of-Array instead of '
                        'Array-of-Structure code. Only for CPU code'
                        'and only in mixed precision')
    variant('timers', default=False,
            description='Build with support for timers')
    variant('da', default=False,
            description='Install with support for basic data analysis tools')
    variant('gui', default=False,
            description='Install with Matplotlib (long installation time)')
    variant('qe', default=True,
            description='Install with patched Quantum Espresso 6.3.0')

    # cuda variant implies mixed precision variant by default, but there is
    # no way to express this in variant syntax, need something like
    # variant('+mixed', default=True, when='+cuda', description="...")

    # conflicts
    conflicts(
        '+phdf5',
        when='~mpi',
        msg='Parallel collective I/O requires MPI-enabled QMCPACK. ' \
        'Please add "~phdf5" to the Spack install line for serial QMCPACK.'
    )
    conflicts(
        '+qe',
        when='~mpi',
        msg='QMCPACK QE variant requires MPI due to limitation in QE build ' \
        'system. Please add "~qe" to the Spack install line for serial ' \
        'QMCPACK.'
    )
    conflicts(
        '+soa',
        when='+cuda',
        msg='QMCPACK SOA variant does not exist for CUDA'
    )
    conflicts(
        '^openblas+ilp64',
        msg='QMCPACK does not support OpenBLAS 64-bit integer variant'
    )
    conflicts(
        '^intel-mkl+ilp64',
        msg='QMCPACK does not support MKL 64-bit integer variant'
    )

    # QMCPACK 3.6.0 or later requires support for C++14
    compiler_warning = 'QMCPACK 3.6.0 or later requires a ' \
                       'compiler with support for C++14'
    conflicts('%gcc@:4', when='@3.6.0:', msg=compiler_warning)
    conflicts('%intel@:17', when='@3.6.0:', msg=compiler_warning)
    conflicts('%pgi@:17', when='@3.6.0:', msg=compiler_warning)
    conflicts('%llvm@:3.4', when='@3.6.0:', msg=compiler_warning)

    # Dependencies match those in the QMCPACK manual.
    # FIXME: once concretizer can unite unconditional and conditional
    # dependencies, some of the '~mpi' variants below will not be necessary.
    # Essential libraries
    depends_on('cmake@3.4.3:', when='@:3.5.0', type='build')
    depends_on('cmake@3.6.0:', when='@3.6.0:', type='build')
    depends_on('boost')
    depends_on('boost@1.61.0:', when='@3.6.0:')
    depends_on('libxml2')
    depends_on('mpi', when='+mpi')
    depends_on('cuda', when='+cuda')
    # HDF5
    depends_on('hdf5+hl+fortran', when='+qe')
    depends_on('hdf5+hl+fortran+mpi', when='+qe+mpi')
    depends_on('hdf5+hl+fortran~mpi', when='+qe~mpi')
    depends_on('hdf5~hl~fortran', when='~qe')
    depends_on('hdf5~hl~fortran+mpi', when='~qe+mpi')
    depends_on('hdf5~hl~fortran~mpi', when='~qe~mpi')
    # Math libraries
    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw-api@3')

    # qmcpack data analysis tools
    # basic command line tool based on Python and NumPy
    # It may be necesseary to disable the blas and lapack
    # when building the 'py-numpy' package, but it should not be a hard
    # dependency on the 'py-numpy~blas~lapack' variant
    depends_on('py-numpy', when='+da', type='run')

    # GUI is optional for data anlysis
    # py-matplotlib leads to a long complex DAG for dependencies
    depends_on('py-matplotlib', when='+gui', type='run')

    # B-spline basis calculation require a patched version of
    # Quantum Espresso 6.3 (see QMCPACK manual)
    # Building explicitly without ELPA due to issues in Quantum Espresso
    # Spack package
    patch_url = 'https://raw.githubusercontent.com/QMCPACK/qmcpack/develop/external_codes/quantum_espresso/add_pw2qmcpack_to_qe-6.3.diff'
    patch_checksum = '2ee346e24926479f5e96f8dc47812173a8847a58354bbc32cf2114af7a521c13'
    depends_on('quantum-espresso@6.3~elpa+mpi+hdf5',
               patches=patch(patch_url, sha256=patch_checksum, when='+qe'),
                   when='+qe+mpi', type='run')

    depends_on('quantum-espresso@6.3~elpa~scalapack~mpi+hdf5',
               patches=patch(patch_url, sha256=patch_checksum, when='+qe'),
                   when='+qe~mpi', type='run')

    # Backport several patches from recent versions of QMCPACK
    # The test_numerics unit test is broken prior to QMCPACK 3.3.0
    patch_url = 'https://patch-diff.githubusercontent.com/raw/QMCPACK/qmcpack/pull/621.patch'
    patch_checksum = 'e2ff7a6f0f006856085d4aab6d31f32f16353e41f760a33a7ef75f3ecce6a5d6'
    patch(patch_url, sha256=patch_checksum, when='@3.1.0:3.3.0')

    # FindMKL.cmake has an issues prior to QMCPACK 3.3.0
    patch_url = 'https://patch-diff.githubusercontent.com/raw/QMCPACK/qmcpack/pull/623.patch'
    patch_checksum = '3eb9dec05fd1a544318ff84cd8b5926cfc6b46b375c7f3b012ccf0b50cf617b7'
    patch(patch_url, sha256=patch_checksum, when='@3.1.0:3.3.0')

    # git-rev files for not git builds issues prior to QMCPACK 3.3.0
    patch_url = 'https://patch-diff.githubusercontent.com/raw/QMCPACK/qmcpack/pull/643.patch'
    patch_checksum = 'c066c79901a612cf8848135e0d544efb114534cca70b90bfccc8ed989d3d9dde'
    patch(patch_url, sha256=patch_checksum, when='@3.1.0:3.3.0')

    def patch(self):
        # FindLibxml2QMC.cmake doesn't check the environment by default
        # for libxml2, so we fix that.
        filter_file(r'$ENV{LIBXML2_HOME}/lib',
                    '${LIBXML2_HOME}/lib $ENV{LIBXML2_HOME}/lib',
                    'CMake/FindLibxml2QMC.cmake')

    def cmake_args(self):
        spec = self.spec
        args = []

        if '+mpi' in spec:
            mpi = spec['mpi']
            args.append('-DCMAKE_C_COMPILER={0}'.format(mpi.mpicc))
            args.append('-DCMAKE_CXX_COMPILER={0}'.format(mpi.mpicxx))
            args.append('-DMPI_BASE_DIR:PATH={0}'.format(mpi.prefix))

        # Currently FFTW_HOME and LIBXML2_HOME are used by CMake.
        # Any CMake warnings about other variables are benign.
        xml2_prefix = spec['libxml2'].prefix
        args.append('-DLIBXML2_HOME={0}'.format(xml2_prefix))
        args.append('-DLibxml2_INCLUDE_DIRS={0}'.format(xml2_prefix.include))
        args.append('-DLibxml2_LIBRARY_DIRS={0}'.format(xml2_prefix.lib))

        if '^fftw@3:' in spec:
            fftw_prefix = spec['fftw'].prefix
            args.append('-DFFTW_HOME={0}'.format(fftw_prefix))
            args.append('-DFFTW_INCLUDE_DIRS={0}'.format(fftw_prefix.include))
            args.append('-DFFTW_LIBRARY_DIRS={0}'.format(fftw_prefix.lib))

        args.append('-DBOOST_ROOT={0}'.format(self.spec['boost'].prefix))
        args.append('-DHDF5_ROOT={0}'.format(self.spec['hdf5'].prefix))

        # Default is MPI, serial version is convenient for cases, e.g. laptops
        if '+mpi' in spec:
            args.append('-DQMC_MPI=1')
        else:
            args.append('-DQMC_MPI=0')

        # Default is parallel collective I/O enabled
        if '+phdf5' in spec:
            args.append('-DENABLE_PHDF5=1')
        else:
            args.append('-DENABLE_PHDF5=0')

        # Default is real-valued single particle orbitals
        if '+complex' in spec:
            args.append('-DQMC_COMPLEX=1')
        else:
            args.append('-DQMC_COMPLEX=0')

        # When '-DQMC_CUDA=1', CMake automatically sets:
        # '-DQMC_MIXED_PRECISION=1'
        #
        # There is a double-precision CUDA path, but it is not as well
        # tested.

        if '+cuda' in spec:
            args.append('-DQMC_CUDA=1')
        else:
            args.append('-DQMC_CUDA=0')

        # Mixed-precision versues double-precision CPU and GPU code
        if '+mixed' in spec:
            args.append('-DQMC_MIXED_PRECISION=1')
        else:
            args.append('-DQMC_MIXED_PRECISION=0')

        # New Structure-of-Array (SOA) code, much faster than default
        # Array-of-Structure (AOS) code.
        # No support for local atomic orbital basis.
        if '+soa' in spec:
            args.append('-DENABLE_SOA=1')
        else:
            args.append('-DENABLE_SOA=0')

        # Manual Timers
        if '+timers' in spec:
            args.append('-DENABLE_TIMERS=1')
        else:
            args.append('-DENABLE_TIMERS=0')

        # Proper detection of optimized BLAS and LAPACK.
        # Based on the code from the deal II Spack package:
        # https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/dealii/package.py
        #
        # Basically, we override CMake's auto-detection mechanism
        # and use the Spack's interface instead
        lapack_blas = spec['lapack'].libs + spec['blas'].libs
        args.extend([
            '-DLAPACK_FOUND=true',
            '-DLAPACK_LIBRARIES=%s' % lapack_blas.joined(';')
        ])

        # Additionally, we need to pass the BLAS+LAPACK include directory for
        # header files. This is to insure vectorized math and FFT libraries
        # get properly detected. Intel MKL requires special case due to
        # differences in Darwin vs. Linux $MKLROOT naming schemes. This section
        # of code is intentionally redundant for backwards compatibility.
        if 'intel-mkl' in spec:
            lapack_dir = format(join_path(env['MKLROOT'], 'include'))
            # Next two lines were introduced in QMCPACK 3.5.0 and later.
            # Prior to v3.5.0, these lines should be benign.
            args.append('-DENABLE_MKL=1')
            args.append('-DMKL_ROOT=%s' % env['MKLROOT'])
        else:
            lapack_dir = ':'.join((
                spec['lapack'].prefix.include,
                spec['blas'].prefix.include
            ))

        args.extend([
            '-DCMAKE_CXX_FLAGS=-I%s' % lapack_dir,
            '-DCMAKE_C_FLAGS=-I%s' % lapack_dir
        ])

        return args

    # QMCPACK 3.6.0 release and later has a functional 'make install',
    # the Spack 'def install' is retained for backwards compatiblity.
    # Note that the two install methods differ in their directory
    # structure.
    @when('@:3.5.0')
    def install(self, spec, prefix):
        """Make the install targets"""

        # QMCPACK 'make install' does nothing, which causes
        # Spack to throw an error.
        #
        # This install method creates the top level directory
        # and copies the bin subdirectory into the appropriate
        # location. We do not copy include or lib at this time due
        # to technical difficulties in qmcpack itself.

        mkdirp(prefix)

        # We assume cwd is self.stage.source_path

        # install manual
        install_tree('manual', prefix.manual)

        # install nexus
        install_tree('nexus', prefix.nexus)

        with working_dir(self.build_directory):
            mkdirp(prefix)

            # install binaries
            install_tree('bin', prefix.bin)

    # QMCPACK 3.6.0 install directory structure changed, thus there
    # thus are two version of the setup_environment method
    @when('@:3.5.0')
    def setup_environment(self, spack_env, run_env):
        """Set-up runtime environment for QMCPACK.
        Set PYTHONPATH for basic analysis scripts and for Nexus."""
        run_env.prepend_path('PYTHONPATH', self.prefix.nexus)

    @when('@3.6.0:')
    def setup_environment(self, spack_env, run_env):
        """Set-up runtime environment for QMCPACK.
        Set PYTHONPATH for basic analysis scripts and for Nexus. Binaries
        are in the  'prefix' directory instead of 'prefix.bin' which is
        not set by the default module environment"""
        run_env.prepend_path('PATH', self.prefix)
        run_env.prepend_path('PYTHONPATH', self.prefix)

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def check(self):
        """Run ctest after building binary.
        It can take over 24 hours to run all the regression tests, here we
        only run the unit tests and short tests. If the unit tests fail,
        the QMCPACK installation aborts. On the other hand, the short tests
        are too strict and often fail, but are still useful to run. In the
        future, the short tests will be more reasonable in terms of quality
        assurance (i.e. they will not be so strict), but will be sufficient to
        validate QMCPACK in production."""

        with working_dir(self.build_directory):
            ctest('-L', 'unit')
            try:
                ctest('-R', 'short')
            except ProcessError:
                warn  = 'Unit tests passed, but short tests have failed.\n'
                warn += 'Please review failed tests before proceeding\n'
                warn += 'with production calculations.\n'
                tty.msg(warn)
