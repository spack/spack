class Yaxt(AutotoolsPackage):
    """Yet Another eXchange Tool"""

    homepage = "https://www.dkrz.de/redmine/projects/yaxt/wiki"
    git = "https://gitlab.dkrz.de/dkrz-sw/yaxt.git"

    version('0.9.2.1', branch='release-0.9.2.1')
    version('0.9.2', branch='release-0.9.2')
    version('0.9.1', branch='release-0.9.1')
    version('0.9.0', branch='release-0.9.0')
    version('0.8.1', branch='release-0.8.1')
    version('0.8.0', branch='release-0.8.0')
    version('0.7.0-p1', branch='release-0.7.0-patched', preferred=True)
    version('0.7.0', branch='release-0.7.0')

    variant('shared', default=True, description='Enable shared libraries')
    variant('fortran', default=True, description='Enable Fortran interface')

    conflicts('~fortran', when='@:0.8.999')

    depends_on('mpi')

    # Do not fail if MPI_LAUNCH does not work and MPI defect checks are disabled
    # (see https://gitlab.dkrz.de/dkrz-sw/yaxt/-/commit/ff5dd54576620e35b6b93b85e791787eb53c9764):
    patch(
        'mpirun/0.7.0.patch',
        # The condition matches version 0.7.0 but not 0.7.0-p1:
        when='@:0.7.0-p0')

    # Fix a typo in the makefile
    # (see https://gitlab.dkrz.de/dkrz-sw/yaxt/-/merge_requests/8)
    patch(
        'mpich/0.9.2.patch',
        # We do not put ^mpich to the condition because there are other
        # MPICH-based MPI packages that might need this:
        when='@0.9.2:0.9.2.1')

    # Enable the PGI/Cray workaround also when macro NO_2D_PARAM is defined:
    patch('no_2d_param/0.7.0.patch', when='@:0.7%aocc+fortran')

    def flag_handler(self, name, flags):
        if name == 'fflags':
            if self.compiler.name == 'aocc':
                flags.append('-DNO_2D_PARAM')
        return flags, None, None

    @property
    def libs(self):
        lib_names = []
        if 'fortran' in self.spec.last_query.extra_parameters:
            lib_names.append('libyaxt')
        lib_names.append('libyaxt_c')

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
        args = [
            '--enable-static',
            'CC={0}'.format(self.spec['mpi'].mpicc),
            'FC={0}'.format(self.spec['mpi'].mpifc if '+fortran' in
                            self.spec else 'no'),
            # We cannot provide a universal value for MPI_LAUNCH, therefore
            # we have to disable the MPI checks:
            '--without-regard-for-quality'
        ]

        # Do not build examples and test programs by default:
        if self.version >= ver('0.8.0'):
            args.extend([
                '--with-on-demand-check-programs', '--without-example-programs'
            ])

        args += self.enable_or_disable('shared')

        return args

    @run_after('configure')
    def patch_libtool(self):
        if not self.spec.satisfies('+fortran+shared'):
            return

        if self.compiler.name in ['nvhpc', 'aocc']:
            # Libtool does not fully support the compiler toolchains, therefore
            # we have to patch the script. The C compilers normally get
            # configured correctly, the variables of interest in the
            # 'BEGIN LIBTOOL CONFIG' section are set to non-empty values and,
            # therefore, are not affected by the replacements below. A more
            # robust solution would be to extend the filter_file function with
            # an additional argument start_at and perform the replacements
            # between the '# ### BEGIN LIBTOOL TAG CONFIG: FC' and
            # '# ### END LIBTOOL TAG CONFIG: FC' markers.

            # How to pass a linker flag through the compiler:
            filter_file(r'^wl=""$',
                        'wl="{0}"'.format(self.compiler.linker_arg), 'libtool')

            # How to compile PIC objects:
            filter_file(r'^pic_flag=""$',
                        'pic_flag=" {0}"'.format(self.compiler.fc_pic_flag),
                        'libtool')
