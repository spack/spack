##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *
import re
import os
import glob


class Zoltan(Package):
    """The Zoltan library is a toolkit of parallel combinatorial algorithms
       for parallel, unstructured, and/or adaptive scientific
       applications.  Zoltan's largest component is a suite of dynamic
       load-balancing and paritioning algorithms that increase
       applications' parallel performance by reducing idle time.  Zoltan
       also has graph coloring and graph ordering algorithms, which are
       useful in task schedulers and parallel preconditioners.

    """

    homepage = "http://www.cs.sandia.gov/zoltan"
    base_url = "http://www.cs.sandia.gov/~kddevin/Zoltan_Distributions"

    version('3.83', '1ff1bc93f91e12f2c533ddb01f2c095f')
    version('3.8', '9d8fba8a990896881b85351d4327c4a9')
    version('3.6', '9cce794f7241ecd8dbea36c3d7a880f9')
    version('3.3', '5eb8f00bda634b25ceefa0122bd18d65')

    variant('debug', default=False, description='Builds a debug version of the library.')
    variant('shared', default=True, description='Builds a shared version of the library.')

    variant('fortran', default=True, description='Enable Fortran support.')
    variant('mpi', default=True, description='Enable MPI support.')

    depends_on('mpi', when='+mpi')

    def url_for_version(self, version):
        return '%s/zoltan_distrib_v%s.tar.gz' % (Zoltan.base_url, version)

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
            '-g' if '+debug' in spec else '-g0',
        ]

        if '+shared' in spec:
            config_args.append('RANLIB=echo')
            config_args.append('--with-ar=$(CXX) -shared $(LDFLAGS) -o')
            config_cflags.append('-fPIC')
            if spec.satisfies('%gcc'):
                config_args.append('--with-libs={0}'.format('-lgfortran'))

        if '+mpi' in spec:
            config_args.append('CC={0}'.format(spec['mpi'].mpicc))
            config_args.append('CXX={0}'.format(spec['mpi'].mpicxx))
            config_args.append('FC={0}'.format(spec['mpi'].mpifc))

            config_args.append('--with-mpi={0}'.format(spec['mpi'].prefix))

            mpi_libs = self.get_mpi_libs()

            # NOTE: Some external mpi installations may have empty lib
            # directory (e.g. bg-q). In this case we need to explicitly
            # pass empty library name.
            if mpi_libs:
                mpi_libs = ' -l'.join(mpi_libs)
                config_args.append('--with-mpi-libs=-l{0}'.format(mpi_libs))
            else:
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

    # NOTE: Zoltan assumes that it's linking against an MPI library that can
    # be found with '-lmpi,' which isn't the case for many MPI packages.  This
    # function finds the names of the actual libraries for Zoltan's MPI dep.
    def get_mpi_libs(self):
        mpi_libs = set()

        for lib_path in glob.glob(join_path(self.spec['mpi'].prefix.lib, '*')):
            mpi_lib_match = re.match(
                r'^(lib)((\w*)mpi(\w*))\.((a)|({0}))$'.format(dso_suffix),
                os.path.basename(lib_path))
            if mpi_lib_match:
                mpi_libs.add(mpi_lib_match.group(2))

        return list(mpi_libs)
