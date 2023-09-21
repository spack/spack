import os

from spack.util.environment import is_system_path


class LibcdiPio(AutotoolsPackage):
    """A version of CDI with parallel I/O features."""

    homepage = 'https://gitlab.dkrz.de/dkrz-sw/cdi-pio'
    git = 'git@gitlab.dkrz.de:mpim-sw/libcdi.git'

    version('master', branch='cdipio-dev-snapshot-20210223')

    variant('shared', default=True, description='Enable shared libraries')
    variant('netcdf', default=True, description='Enable NetCDF support')
    variant('grib2',
            default='eccodes',
            values=('eccodes', 'grib-api', 'none'),
            description='Specify GRIB2 backend')
    variant('external-grib1',
            default=False,
            description='Ignore the built-in support and use the external '
            'GRIB2 backend for GRIB1 files')
    variant('szip-grib1',
            default=False,
            description='Enable szip compression for GRIB1')
    variant('fortran', default=True, description='Enable Fortran interfaces')
    variant('threads',
            default=True,
            description='Compile and link for multithreading')
    variant('mpi', default=True, description='Enable parallel output features')

    depends_on('pkgconfig', type='build')

    depends_on('netcdf-c', when='+netcdf')
    # The library implicitly links to HDF5 when NetCDF support is enabled
    depends_on('hdf5', when='+netcdf')

    depends_on('grib-api', when='grib2=grib-api')
    depends_on('eccodes', when='grib2=eccodes')

    depends_on('szip', when='+szip-grib1')

    depends_on('uuid')

    depends_on('mpi', when='+mpi')
    depends_on('yaxt', when='+mpi')
    depends_on('yaxt+fortran', when='+mpi+fortran')
    depends_on('scales-ppm+mpi', when='+mpi')

    conflicts('+szip-grib1',
              when='+external-grib1 grib2=none',
              msg='The configuration does not support GRIB1')

    conflicts('^ossp-uuid', msg='OSSP uuid is not currently supported')

    # Libtool fails to recognize NAG compiler behind an MPI wrapper and NAG
    # compiler fails to process -pthread compiler flag:
    patch('nag.patch', when='%nag')

    # The library uses librt but does not check whether it is available without
    # the respective linker flag:
    patch('librt.patch', when='+mpi')

    @property
    def libs(self):
        lib_names = []
        if 'fortran' in self.spec.last_query.extra_parameters:
            lib_names.append('libcdi_f2003')
        if '+mpi' in self.spec:
            lib_names.append('libcdipio')
        lib_names.append('libcdi')

        shared = '+shared' in self.spec
        libs = find_libraries(lib_names,
                              root=self.prefix,
                              shared=shared,
                              recursive=True)

        if libs:
            return libs

        msg = 'Unable to recursively locate {0} libraries in {1}'
        raise spack.error.NoLibrariesError(
            msg.format(self.spec.name, self.spec.prefix))

    def configure_args(self):
        config_args = [
            # Always build static libraries
            '--enable-static',
            # Use the service library
            '--enable-service',
            # Use the extra library
            '--enable-extra',
            # Use the ieg library
            '--enable-ieg',
            # Disable HIRLAM extensions
            '--disable-hirlam-extensions',
            # Due to a bug in the configure script we have to avoid explicit
            # disabling of swig-based, ruby and python bindings with
            # '--disable-swig', '--disable-ruby', and '--disable-python'.
        ]

        config_args += self.enable_or_disable('shared')
        config_args += self.with_or_without('threads')

        # Help Libtool to find the right UUID library
        libs = self.spec['uuid'].libs

        if '+netcdf' in self.spec:
            config_args.append('--with-netcdf=' + self.spec['netcdf-c'].prefix)
            # Help Libtool to find the right HDF5 library
            libs += self.spec['hdf5'].libs
        else:
            config_args.append('--without-netcdf')

        if self.spec.variants['grib2'].value == 'eccodes':
            config_args.append('--with-eccodes=' + self.spec['eccodes'].prefix)
            config_args.append('--without-grib_api')
        elif self.spec.variants['grib2'].value == 'grib-api':
            config_args.append('--with-grib_api=' +
                               self.spec['grib-api'].prefix)
            config_args.append('--without-eccodes')
        else:
            config_args.append('--without-grib_api')
            config_args.append('--without-eccodes')

        if '+external-grib1' in self.spec:
            config_args.append('--disable-cgribex')
        else:
            config_args.append('--enable-cgribex')

        if '+szip-grib1' in self.spec:
            config_args.append('--with-szlib=' + self.spec['szip'].prefix)
        else:
            config_args.append('--without-szlib')

        if '+fortran' in self.spec:
            config_args.extend(
                ['--enable-iso-c-interface', '--enable-cf-interface'])
        else:
            config_args.extend(
                ['--disable-iso-c-interface', '--disable-cf-interface'])

        if '+mpi' in self.spec:
            config_args.extend([
                'CC=' + self.spec['mpi'].mpicc, 'FC=' + self.spec['mpi'].mpifc,
                '--enable-mpi'
            ])
        else:
            # Due to a bug in the configure script we have to avoid explicit
            # disabling of MPI support with '--disable-mpi'.
            pass

        if '^yaxt~fortran' in self.spec:
            config_args.extend(['YAXT_LIBS= ', 'YAXT_CFLAGS= '])

        if self.run_tests and '^openmpi' in self.spec:
            config_args.append(self.spec['openmpi'].format(
                'MPI_LAUNCH={prefix.bin.mpirun} --oversubscribe'))

        # We do not use libs.search_flags because we need to filter the system
        # directories out.
        config_args.extend([
            'LDFLAGS={0}'.format(' '.join([
                '-L' + d for d in libs.directories if not is_system_path(d)
            ])), 'LIBS={0}'.format(libs.link_flags)
        ])

        return config_args

    @run_after('configure')
    def skip_mpi_tests(self):
        # The parallel tests fail if the configure script is unable to find a
        # working MPI_LAUNCH command. This means that we cannot run the serial
        # tests too since all tests run with a single 'make check' command. The
        # idea is to check whether the configure managed to find a working
        # MPI_LAUNCH command and if that is not the case, hack the test scripts
        # so that the serial tests would run normally and the parallel tests
        # would be marked as skipped.

        # No need to do anything if we are not going to run the parallel tests:
        if not self.run_tests or '~mpi' in self.spec:
            return

        with working_dir(self.build_directory):
            # We get the value of the MPI_LAUNCH output variable and hack the
            # test scripts by calling and modifying ./config.status:
            config_status = Executable('./config.status')

            # Create a template for ./config.status:
            tmp_filename = 'mpi_launch.spack~'
            with open(tmp_filename, 'w') as f:
                f.write('@MPI_LAUNCH@')

            # Get the value of MPI_LAUNCH:
            mpi_launch = config_status('-q',
                                       '--file=-:{0}'.format(tmp_filename),
                                       output=str,
                                       error=os.devnull).strip()

            # No need to continue if the configure script managed to find a
            # working MPI_LAUNCH command (the value 'true' indicates that
            # MPI_LAUNCH is not found):
            if mpi_launch != 'true':
                return

            # Hack ./config.status so it starts substituting @MPI_LAUNCH@ with
            # '|| exit 77;', which triggers the parallel tests to exit with the
            # 77 exit code (tests that exit with the 77 exit code are marked
            # as skipped by Automake). Note that we update the file here, which
            # will trigger make to re-run it and update the test scripts with
            # the new value for MPI_LAUNCH:
            filter_file('S["MPI_LAUNCH"]="true"',
                        'S["MPI_LAUNCH"]="|| exit 77;"',
                        './config.status',
                        string=True,
                        backup=False)

    @run_after('configure')
    def patch_libtool(self):
        # Libtool does not fully support NVHPC and AOCC compiler toolchains,
        # therefore we have to patch the script. We, however, patch it
        # indirectly because method skip_mpi_tests (see above) intentionally
        # updates the timestamp of ./config.status, which triggers re-generation
        # of ./libtool during the build stage.

        # No need to do anything if we are not going to use NVHPC and AOCC
        # Fortran compilers:
        if not (self.spec.satisfies('+fortran+shared')
                and self.compiler.name in ['nvhpc', 'aocc']):
            return

        with working_dir(self.build_directory):
            # How to pass a linker flag through the compiler:
            filter_file(r"^lt_prog_compiler_wl_FC=''$",
                        "lt_prog_compiler_wl_FC='{0}'".format(
                            self.compiler.linker_arg),
                        './config.status',
                        string=False,
                        backup=False)

            # How to compile PIC objects:
            filter_file(r"^lt_prog_compiler_pic_FC=''$",
                        "lt_prog_compiler_pic_FC=' {0}'".format(
                            self.compiler.fc_pic_flag),
                        './config.status',
                        string=False,
                        backup=False)
