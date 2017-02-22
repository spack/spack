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

import os
from spack import *


class Petsc(Package):
    """PETSc is a suite of data structures and routines for the scalable
    (parallel) solution of scientific applications modeled by partial
    differential equations.
    """

    homepage = "http://www.mcs.anl.gov/petsc/index.html"
    url = "http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.5.3.tar.gz"

    version('develop', git='https://bitbucket.org/petsc/petsc.git', tag='master')
    version('xsdk-0.2.0', git='https://bitbucket.org/petsc/petsc.git', tag='xsdk-0.2.0')
    version('for-pflotran-0.1.0', git='https://bitbucket.org/petsc/petsc.git',
            commit='7943f4e1472fff9cf1fc630a1100136616e4970f')

    version('3.7.5', 'f00f6e6a3bac39052350dd47194b58a3')
    version('3.7.4', 'aaf94fa54ef83022c14091f10866eedf')
    version('3.7.2', '50da49867ce7a49e7a0c1b37f4ec7b34')
    version('3.6.4', '7632da2375a3df35b8891c9526dbdde7')
    version('3.6.3', '91dd3522de5a5ef039ff8f50800db606')
    version('3.5.3', 'd4fd2734661e89f18ac6014b5dd1ef2f')
    version('3.5.2', 'ad170802b3b058b5deb9cd1f968e7e13')
    version('3.5.1', 'a557e029711ebf425544e117ffa44d8f')
    version('3.4.4', '7edbc68aa6d8d6a3295dd5f6c2f6979d')

    variant('shared',  default=True,
            description='Enables the build of shared libraries')
    variant('mpi',     default=True,  description='Activates MPI support')
    variant('double',  default=True,
            description='Switches between single and double precision')
    variant('complex', default=False, description='Build with complex numbers')
    variant('debug',   default=False, description='Compile in debug mode')

    variant('metis',   default=True,
            description='Activates support for metis and parmetis')
    variant('hdf5',    default=True,
            description='Activates support for HDF5 (only parallel)')
    variant('boost',   default=True,  description='Activates support for Boost')
    variant('hypre',   default=True,
            description='Activates support for Hypre (only parallel)')
    variant('mumps',   default=False,
            description='Activates support for MUMPS (only parallel'
            ' and 32bit indices)')
    variant('superlu-dist', default=True,
            description='Activates support for SuperluDist (only parallel)')
    variant('trilinos', default=False,
            description='Activates support for Trilinos (only parallel)')
    variant('int64', default=False,
            description='Compile with 64bit indices')

    # Virtual dependencies
    # Git repository needs sowing to build Fortran interface
    depends_on('sowing', when='@develop')

    # PETSc, hypre, superlu_dist when built with int64 use 32 bit integers
    # with BLAS/LAPACK
    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')

    # Build dependencies
    depends_on('python @2.6:2.7', type='build')

    # Other dependencies
    depends_on('boost', when='@:3.5+boost')
    depends_on('metis@5:~int64', when='+metis~int64')
    depends_on('metis@5:+int64', when='+metis+int64')

    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('parmetis', when='+metis+mpi')
    # Hypre does not support complex numbers.
    # Also PETSc prefer to build it without internal superlu, likely due to
    # conflict in headers see
    # https://bitbucket.org/petsc/petsc/src/90564b43f6b05485163c147b464b5d6d28cde3ef/config/BuildSystem/config/packages/hypre.py
    depends_on('hypre~internal-superlu~int64', when='+hypre+mpi~complex~int64')
    depends_on('hypre@xsdk-0.2.0~internal-superlu+int64', when='@xsdk-0.2.0+hypre+mpi~complex+int64')
    depends_on('hypre@xsdk-0.2.0~internal-superlu~int64', when='@xsdk-0.2.0+hypre+mpi~complex~int64')
    depends_on('hypre@develop~internal-superlu+int64', when='@develop+hypre+mpi~complex+int64')
    depends_on('hypre@develop~internal-superlu~int64', when='@develop+hypre+mpi~complex~int64')
    depends_on('hypre~internal-superlu+int64', when='+hypre+mpi~complex+int64')
    depends_on('superlu-dist@:4.3~int64', when='@3.4.4:3.6.4+superlu-dist+mpi~int64')
    depends_on('superlu-dist@:4.3+int64', when='@3.4.4:3.6.4+superlu-dist+mpi+int64')
    depends_on('superlu-dist@5.0.0:~int64', when='@3.7:+superlu-dist+mpi~int64')
    depends_on('superlu-dist@5.0.0:+int64', when='@3.7:+superlu-dist+mpi+int64')
    depends_on('superlu-dist@5.0.0:~int64', when='@for-pflotran-0.1.0+superlu-dist+mpi~int64')
    depends_on('superlu-dist@5.0.0:+int64', when='@for-pflotran-0.1.0+superlu-dist+mpi+int64')
    depends_on('superlu-dist@xsdk-0.2.0~int64', when='@xsdk-0.2.0+superlu-dist+mpi~int64')
    depends_on('superlu-dist@xsdk-0.2.0+int64', when='@xsdk-0.2.0+superlu-dist+mpi+int64')
    depends_on('superlu-dist@develop~int64', when='@develop+superlu-dist+mpi~int64')
    depends_on('superlu-dist@develop+int64', when='@develop+superlu-dist+mpi+int64')
    depends_on('mumps+mpi', when='+mumps+mpi~int64')
    depends_on('scalapack', when='+mumps+mpi~int64')
    depends_on('scalapack', when='+mumps+mpi')
    depends_on('trilinos@12.6.2:', when='@3.7.0:+trilinos+mpi')
    depends_on('trilinos@xsdk-0.2.0', when='@xsdk-0.2.0+trilinos+mpi')
    depends_on('trilinos@develop', when='@xdevelop+trilinos+mpi')        
    
    def mpi_dependent_options(self):
        if '~mpi' in self.spec:
            compiler_opts = [
                '--with-cc=%s' % os.environ['CC'],
                '--with-cxx=%s' % (os.environ['CXX']
                                   if self.compiler.cxx is not None else '0'),
                '--with-fc=%s' % (os.environ['FC']
                                  if self.compiler.fc is not None else '0'),
                '--with-mpi=0'
            ]
            error_message_fmt = \
                '\t{library} support requires "+mpi" to be activated'

            # If mpi is disabled (~mpi), it's an error to have any of these
            # enabled. This generates a list of any such errors.
            errors = [
                error_message_fmt.format(library=x)
                for x in ('hdf5', 'hypre', 'parmetis', 'mumps', 'superlu-dist')
                if ('+' + x) in self.spec]
            if errors:
                errors = ['incompatible variants given'] + errors
                raise RuntimeError('\n'.join(errors))
        else:
            compiler_opts = [
                '--with-cc=%s' % self.spec['mpi'].mpicc,
                '--with-cxx=%s' % self.spec['mpi'].mpicxx,
                '--with-fc=%s' % self.spec['mpi'].mpifc
            ]
        return compiler_opts

    def install(self, spec, prefix):
        options = ['--with-ssl=0',
                   '--with-x=0',
                   '--download-c2html=0',
                   '--download-sowing=0',
                   '--download-hwloc=0']
        options.extend(self.mpi_dependent_options())
        options.extend([
            '--with-precision=%s' % (
                'double' if '+double' in spec else 'single'),
            '--with-scalar-type=%s' % (
                'complex' if '+complex' in spec else 'real'),
            '--with-shared-libraries=%s' % ('1' if '+shared' in spec else '0'),
            '--with-debugging=%s' % ('1' if '+debug' in spec else '0'),
            '--with-64-bit-indices=%s' % ('1' if '+int64' in spec else '0')
        ])
        # Make sure we use exactly the same Blas/Lapack libraries
        # across the DAG. To that end list them explicitly
        lapack_blas = spec['lapack'].libs + spec['blas'].libs
        options.extend([
            '--with-blas-lapack-lib=%s' % lapack_blas.joined()
        ])

        if 'trilinos' in spec:
            options.append('--with-cxx-dialect=C++11')
	    
        # Activates library support if needed
        for library in ('metis', 'boost', 'hdf5', 'hypre', 'parmetis',
                        'mumps', 'scalapack', 'trilinos'):
            options.append(
                '--with-{library}={value}'.format(
                    library=library, value=('1' if library in spec else '0'))
            )
            if library in spec:
                options.append(
                    '--with-{library}-dir={path}'.format(
                        library=library, path=spec[library].prefix)
                )
        # PETSc does not pick up SuperluDist from the dir as they look for
        # superlu_dist_4.1.a
        if 'superlu-dist' in spec:
            options.extend([
                '--with-superlu_dist-include=%s' %
                spec['superlu-dist'].prefix.include,
                '--with-superlu_dist-lib=%s' %
                join_path(spec['superlu-dist'].prefix.lib,
                          'libsuperlu_dist.a'),
                '--with-superlu_dist=1'
            ])
        else:
            options.append(
                '--with-superlu_dist=0'
            )

        configure('--prefix=%s' % prefix, *options)

        # PETSc has its own way of doing parallel make.
        make('MAKE_NP=%s' % make_jobs, parallel=False)
        make("install")

        # solve Poisson equation in 2D to make sure nothing is broken:
        if ('mpi' in spec) and self.run_tests:
            with working_dir('src/ksp/ksp/examples/tutorials'):
                env['PETSC_DIR'] = self.prefix
                cc = Executable(spec['mpi'].mpicc)
                cc('ex50.c', '-I%s' % prefix.include, '-L%s' % prefix.lib,
                   '-lpetsc', '-lm', '-o', 'ex50')
                run = Executable(join_path(spec['mpi'].prefix.bin, 'mpirun'))
                run('ex50', '-da_grid_x', '4', '-da_grid_y', '4')
                if 'superlu-dist' in spec:
                    run('ex50',
                        '-da_grid_x', '4',
                        '-da_grid_y', '4',
                        '-pc_type', 'lu',
                        '-pc_factor_mat_solver_package', 'superlu_dist')

                if 'mumps' in spec:
                    run('ex50',
                        '-da_grid_x', '4',
                        '-da_grid_y', '4',
                        '-pc_type', 'lu',
                        '-pc_factor_mat_solver_package', 'mumps')

                if 'hypre' in spec:
                    run('ex50',
                        '-da_grid_x', '4',
                        '-da_grid_y', '4',
                        '-pc_type', 'hypre',
                        '-pc_hypre_type', 'boomeramg')

    def setup_environment(self, spack_env, run_env):
        # configure fails if these env vars are set outside of Spack
        spack_env.unset('PETSC_DIR')
        spack_env.unset('PETSC_ARCH')

        # Set PETSC_DIR in the module file
        run_env.set('PETSC_DIR', self.prefix)
        run_env.unset('PETSC_ARCH')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # Set up PETSC_DIR for everyone using PETSc package
        spack_env.set('PETSC_DIR', self.prefix)
        spack_env.unset('PETSC_ARCH')
