class ScalesPpm(AutotoolsPackage):
    """Convenience library to provide parallelization and performance oriented
    modules to parallel software packages, particularly for earth system
    models."""

    homepage = "https://www.dkrz.de/redmine/projects/scales-ppm"
    url = "https://www.dkrz.de/redmine/attachments/download/500/ppm-1.0.6.tar.gz"
    list_url = "https://www.dkrz.de/redmine/projects/scales-ppm/files"

    version(
        '1.0.8',
        sha256=
        '34cde7ce210eee4755ec0228d3f2d61542e94522e7a4eefdc5472ed3772f32f7',
        url=
        'https://www.dkrz.de/redmine/attachments/download/517/ppm-1.0.8.tar.gz'
    )
    version(
        '1.0.7',
        sha256=
        'e37bfa8a68a975b6de40c757a75ad05d4ff3b70dc21de8876daa259dbe8065cb',
        url=
        'https://www.dkrz.de/redmine/attachments/download/509/ppm-1.0.7.tar.gz'
    )
    version(
        '1.0.6',
        sha256=
        'fa45d75d4225f726985128727fe65a075096e7308557dfa05ca8f0ce13ebbda4',
        url=
        'https://www.dkrz.de/redmine/attachments/download/500/ppm-1.0.6.tar.gz'
    )

    variant('mpi', default=True, description='enable MPI support')
    variant('fortran', default=True, description='enable Fortran interface')

    depends_on('perl', type='build')
    # It looks like Python is needed only for the example:
    # depends_on('python', type='build')

    depends_on('mpi', when='+mpi')

    conflicts('~fortran',
              when='@:1.0.7',
              msg='Fortran interface can be disabled '
              'only starting version 1.0.8')

    # Do not fail if MPI_LAUNCH does not work and MPI defect checks are
    # disabled (see https://gitlab.dkrz.de/jahns/ppm/-/merge_requests/1):
    patch('mpirun/1.0.6.patch', when='@:1.0.6+mpi')

    def flag_handler(self, name, flags):
        if name == 'fflags' and '+fortran' in self.spec:
            if self.spec.satisfies('%gcc@10: +mpi'):
                # Enable building with 'gcc@10:' (it looks like we need the flag
                # only when MPI support is enabled):
                flags.append('-fallow-argument-mismatch')
            elif self.spec.satisfies('%nvhpc'):
                flags.append(self.compiler.fc_pic_flag)

        return flags, None, None

    def configure_args(self):
        config_args = [
            '--disable-crypto', '--disable-netcdf', '--disable-parmetis',
            '--disable-metis', '--with-on-demand-check-programs',
            '--without-example-programs'
        ]

        fc = None if '+fortran' in self.spec else 'no'

        if '+mpi' in self.spec:
            config_args.extend([
                '--enable-MPI',
                'CC=' + self.spec['mpi'].mpicc,
                # We cannot provide a universal value for
                # MPI_LAUNCH, therefore we have to disable the
                # MPI checks:
                '--without-regard-for-quality'
            ])
            if fc is None:
                fc = self.spec['mpi'].mpifc
        else:
            config_args.append('--disable-MPI')

        if fc:
            config_args.append('FC=' + fc)

        return config_args
