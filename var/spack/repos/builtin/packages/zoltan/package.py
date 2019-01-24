# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import re
import os
import glob


class Zoltan(Package):
    """The Zoltan library is a toolkit of parallel combinatorial algorithms
       for parallel, unstructured, and/or adaptive scientific
       applications.  Zoltan's largest component is a suite of dynamic
       load-balancing and partitioning algorithms that increase
       applications' parallel performance by reducing idle time.  Zoltan
       also has graph coloring and graph ordering algorithms, which are
       useful in task schedulers and parallel preconditioners.

    """

    homepage = "http://www.cs.sandia.gov/zoltan"
    url      = "http://www.cs.sandia.gov/~kddevin/Zoltan_Distributions/zoltan_distrib_v3.83.tar.gz"

    version('3.83', '1ff1bc93f91e12f2c533ddb01f2c095f')
    version('3.8', '9d8fba8a990896881b85351d4327c4a9')
    version('3.6', '9cce794f7241ecd8dbea36c3d7a880f9')
    version('3.3', '5eb8f00bda634b25ceefa0122bd18d65')

    variant('debug', default=False, description='Builds a debug version of the library.')
    variant('shared', default=True, description='Builds a shared version of the library.')

    variant('fortran', default=True, description='Enable Fortran support.')
    variant('mpi', default=True, description='Enable MPI support.')
    variant('parmetis', default=False, description='Enable ParMETIS support.')

    depends_on('mpi', when='+mpi')

    depends_on('parmetis@4:', when='+parmetis')
    depends_on('metis', when='+parmetis')

    conflicts('+parmetis', when='~mpi')

    def install(self, spec, prefix):
        # FIXME: The older Zoltan versions fail to compile the F90 MPI wrappers
        # because of some complicated generic type problem.
        if spec.satisfies('@:3.6+fortran+mpi'):
            raise RuntimeError(('Cannot build Zoltan v{0} with +fortran and '
                                '+mpi; please disable one of these features '
                                'or upgrade versions.').format(self.version))

        config_args = [
            self.get_config_flag('f90interface', 'fortran'),
            self.get_config_flag('mpi', 'mpi'),
        ]
        config_cflags = [
            '-O0' if '+debug' in spec else '-O3',
            '-g' if '+debug' in spec else '',
        ]

        if '+shared' in spec:
            config_args.append('RANLIB=echo')
            config_args.append('--with-ar=$(CXX) -shared $(LDFLAGS) -o')
            config_cflags.append(self.compiler.pic_flag)
            if spec.satisfies('%gcc'):
                config_args.append('--with-libs=-lgfortran')
            if spec.satisfies('%intel'):
                config_args.append('--with-libs=-lifcore')

        if '+parmetis' in spec:
            config_args.append('--with-parmetis')
            config_args.append('--with-parmetis-libdir={0}'
                               .format(spec['parmetis'].prefix.lib))
            config_args.append('--with-parmetis-incdir={0}'
                               .format(spec['parmetis'].prefix.include))
            config_args.append('--with-incdirs=-I{0}'
                               .format(spec['metis'].prefix.include))
            config_args.append('--with-ldflags=-L{0}'
                               .format(spec['metis'].prefix.lib))

        if '+mpi' in spec:
            config_args.append('CC={0}'.format(spec['mpi'].mpicc))
            config_args.append('CXX={0}'.format(spec['mpi'].mpicxx))
            config_args.append('FC={0}'.format(spec['mpi'].mpifc))

            config_args.append('--with-mpi={0}'.format(spec['mpi'].prefix))

            # NOTE: Zoltan assumes that it's linking against an MPI library
            # that can be found with '-lmpi' which isn't the case for many
            # MPI packages. We rely on the MPI-wrappers to automatically add
            # what is required for linking and thus pass an empty list of libs
            config_args.append('--with-mpi-libs= ')

        # NOTE: Early versions of Zoltan come packaged with a few embedded
        # library packages (e.g. ParMETIS, Scotch), which messes with Spack's
        # ability to descend directly into the package's source directory.
        source_directory = self.stage.source_path
        if spec.satisfies('@:3.6'):
            zoltan_directory = 'Zoltan_v{0}'.format(self.version)
            source_directory = join_path(source_directory, zoltan_directory)

        build_directory = join_path(source_directory, 'build')
        with working_dir(build_directory, create=True):
            config = Executable(join_path(source_directory, 'configure'))
            config(
                '--prefix={0}'.format(prefix),
                '--with-cflags={0}'.format(' '.join(config_cflags)),
                '--with-cxxflags={0}'.format(' '.join(config_cflags)),
                '--with-fcflags={0}'.format(' '.join(config_cflags)),
                *config_args
            )

            # NOTE: Earlier versions of Zoltan cannot be built in parallel
            # because they contain nested Makefile dependency bugs.
            make(parallel=not spec.satisfies('@:3.6+fortran'))
            make('install')

        # NOTE: Unfortunately, Zoltan doesn't provide any configuration
        # options for the extension of the output library files, so this
        # script must change these extensions as a post-processing step.
        if '+shared' in spec:
            for lib_path in glob.glob(join_path(prefix, 'lib', '*.a')):
                lib_static_name = os.path.basename(lib_path)
                lib_shared_name = re.sub(r'\.a$', '.{0}'.format(dso_suffix),
                                         lib_static_name)
                move(lib_path, join_path(prefix, 'lib', lib_shared_name))

    def get_config_flag(self, flag_name, flag_variant):
        flag_pre = 'en' if '+{0}'.format(flag_variant) in self.spec else 'dis'
        return '--{0}able-{1}'.format(flag_pre, flag_name)
