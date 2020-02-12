# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class AdolC(AutotoolsPackage):
    """A package for the automatic differentiation of first and higher
    derivatives of vector functions in C and C++ programs by operator
    overloading."""

    homepage = "https://projects.coin-or.org/ADOL-C"
    url      = "http://www.coin-or.org/download/source/ADOL-C/ADOL-C-2.6.1.tgz"
    git      = "https://gitlab.com/adol-c/adol-c.git"

    version('develop',  branch='master')
    version('2.6.3', sha256='6ed74580695a0d2c960581e5430ebfcd380eb5da9337daf488bf2e89039e9c21')
    version('2.6.2', sha256='f6326e7ba994d02074816132d4461915221069267c31862b31fab7020965c658')
    version('2.6.1', sha256='037089e0f64224e5e6255b61af4fe7faac080533fd778b76fe946e52491918b5')
    version('2.5.2', sha256='2fa514d9799989d6379738c2bcf75070d9834e4d227eb32a5b278840893b2af9')

    variant('advanced_branching', default=False,
            description='Enable advanced branching to reduce retaping')
    variant('atrig_erf', default=True,
            description='Enable arc-trig and error functions')
    variant('doc',      default=True,  description='Install documentation')
    variant('openmp',   default=False, description='Enable OpenMP support')
    variant('sparse',   default=False, description='Enable sparse drivers')
    variant('examples', default=True,  description='Install examples')
    variant('boost',    default=False, description='Enable boost')

    # Build dependencies
    depends_on('automake', type='build', when='@develop')
    depends_on('autoconf', type='build', when='@develop')
    depends_on('libtool',  type='build', when='@develop')
    depends_on('m4',       type='build', when='@develop')

    # Link dependencies
    depends_on('boost+system', when='+boost')

    # FIXME: add
    #  --with-colpack=DIR      path to the colpack library and headers
    #                       [default=system libraries]
    #  --with-mpi-root=MPIROOT absolute path to the MPI root directory
    #  --with-mpicc=MPICC      name of the MPI C++ compiler (default mpicc)
    #  --with-mpicxx=MPICXX    name of the MPI C++ compiler (default mpicxx)
    #  --with-ampi=AMPI_DIR    full path to the installation of adjoinable MPI
    #                           (AMPI)

    patch('openmp_exam_261.patch', when='@2.6.1')

    def configure_args(self):
        spec = self.spec

        configure_args = []

        if '+boost' in spec:
            configure_args.append(
                '--with-boost={0}'.format(spec['boost'].prefix)
            )
        else:
            configure_args.append(
                '--with-boost=no'
            )

        if '+advanced_branching' in spec:
            configure_args.append(
                '--enable-advanced-branching'
            )

        if '+atrig_erf' in spec:
            configure_args.append(
                '--enable-atrig-erf'
            )

        if '+openmp' in spec:
            configure_args.append(
                '--with-openmp-flag={0}'.format(self.compiler.openmp_flag)
            )

        if '+sparse' in spec:
            configure_args.append(
                '--enable-sparse'
            )

        # We can simply use the bundled examples to check
        # whether Adol-C works as expected
        if '+examples' in spec:
            configure_args.extend([
                '--enable-docexa',  # Documented examples
                '--enable-addexa'  # Additional examples
            ])
            if '+openmp' in spec:
                configure_args.append(
                    '--enable-parexa'  # Parallel examples
                )

        return configure_args

    @run_after('install')
    def install_additional_files(self):
        spec = self.spec
        prefix = self.prefix

        # Copy the config.h file, as some packages might require it
        source_directory = self.stage.source_path
        config_h = join_path(source_directory, 'ADOL-C', 'src', 'config.h')
        install(config_h, join_path(prefix.include, 'adolc'))

        # Install documentation to {prefix}/share
        if '+doc' in spec:
            install_tree(join_path('ADOL-C', 'doc'),
                         join_path(prefix.share, 'doc'))

        # Install examples to {prefix}/share
        if '+examples' in spec:
            install_tree(join_path('ADOL-C', 'examples'),
                         join_path(prefix.share, 'examples'))

            # Run some examples that don't require user input
            # TODO: Check that bundled examples produce the correct results
            with working_dir(join_path(
                    source_directory, 'ADOL-C', 'examples')):
                Executable('./tapeless_scalar')()
                Executable('./tapeless_vector')()

            with working_dir(join_path(
                    source_directory,
                    'ADOL-C', 'examples', 'additional_examples')):
                Executable('./checkpointing/checkpointing')()

            if '+openmp' in spec:
                with working_dir(join_path(
                        source_directory,
                        'ADOL-C', 'examples', 'additional_examples')):
                    Executable('./checkpointing/checkpointing')()
