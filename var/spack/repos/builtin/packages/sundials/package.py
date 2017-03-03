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
import os


class Sundials(Package):
    """SUNDIALS (SUite of Nonlinear and DIfferential/ALgebraic equation
    Solvers)"""

    homepage = "http://computation.llnl.gov/casc/sundials/"
    url = "http://computation.llnl.gov/projects/sundials-suite-nonlinear-differential-algebraic-equation-solvers/download/sundials-2.6.2.tar.gz"

    version('2.6.2', '3deeb0ede9f514184c6bd83ecab77d95')

    variant('mpi',     default=True,  description='Enable MPI support')
    variant('lapack',  default=True,
            description='Build with external BLAS/LAPACK libraries')
    variant('klu',     default=False,
            description='Build with SuiteSparse KLU libraries')
    variant('superlu', default=False,
            description='Build with SuperLU_MT libraries')
    variant('openmp',  default=False, description='Enable OpenMP support')
    variant('pthread', default=True,
            description='Enable POSIX threads support')

    depends_on('cmake', type='build')
    depends_on('mpi',                when='+mpi')
    depends_on('blas',               when='+lapack')
    depends_on('lapack',             when='+lapack')
    depends_on('suite-sparse',       when='+klu')
    depends_on('superlu-mt+openmp',  when='+superlu+openmp')
    depends_on('superlu-mt+pthread', when='+superlu+pthread')

    def install(self, spec, prefix):
        cmake_args = std_cmake_args[:]
        cmake_args.extend([
            '-DBUILD_SHARED_LIBS=ON',
            '-DCMAKE_C_FLAGS=-fPIC',
            '-DCMAKE_Fortran_FLAGS=-fPIC',
            '-DEXAMPLES_ENABLE=ON',
            '-DEXAMPLES_INSTALL=ON',
            '-DFCMIX_ENABLE=ON'
        ])

        # MPI support
        if '+mpi' in spec:
            cmake_args.extend([
                '-DMPI_ENABLE=ON',
                '-DMPI_MPICC={0}'.format(spec['mpi'].mpicc),
                '-DMPI_MPIF77={0}'.format(spec['mpi'].mpif77)
            ])
        else:
            cmake_args.append('-DMPI_ENABLE=OFF')

        # Building with LAPACK and BLAS
        if '+lapack' in spec:
            cmake_args.extend([
                '-DLAPACK_ENABLE=ON',
                '-DLAPACK_LIBRARIES={0}'.format(
                    (spec['lapack'].libs +
                     spec['blas'].libs).joined(';')
                )
            ])
        else:
            cmake_args.append('-DLAPACK_ENABLE=OFF')

        # Building with KLU
        if '+klu' in spec:
            cmake_args.extend([
                '-DKLU_ENABLE=ON',
                '-DKLU_INCLUDE_DIR={0}'.format(
                    spec['suite-sparse'].prefix.include),
                '-DKLU_LIBRARY_DIR={0}'.format(
                    spec['suite-sparse'].prefix.lib)
            ])
        else:
            cmake_args.append('-DKLU_ENABLE=OFF')

        # Building with SuperLU_MT
        if '+superlu' in spec:
            cmake_args.extend([
                '-DSUPERLUMT_ENABLE=ON',
                '-DSUPERLUMT_INCLUDE_DIR={0}'.format(
                    spec['superlu-mt'].prefix.include),
                '-DSUPERLUMT_LIBRARY_DIR={0}'.format(
                    spec['superlu-mt'].prefix.lib)
            ])
            if '+openmp' in spec:
                cmake_args.append('-DSUPERLUMT_THREAD_TYPE=OpenMP')
            elif '+pthread' in spec:
                cmake_args.append('-DSUPERLUMT_THREAD_TYPE=Pthread')
            else:
                msg = 'You must choose either +openmp or +pthread when '
                msg += 'building with SuperLU_MT'
                raise RuntimeError(msg)
        else:
            cmake_args.append('-DSUPERLUMT_ENABLE=OFF')

        # OpenMP support
        if '+openmp' in spec:
            cmake_args.append('-DOPENMP_ENABLE=ON')
        else:
            cmake_args.append('-DOPENMP_ENABLE=OFF')

        # POSIX threads support
        if '+pthread' in spec:
            cmake_args.append('-DPTHREAD_ENABLE=ON')
        else:
            cmake_args.append('-DPTHREAD_ENABLE=OFF')

        with working_dir('build', create=True):
            cmake('..', *cmake_args)

            make()
            make('install')

        install('LICENSE', prefix)

        self.filter_compilers()

    def filter_compilers(self):
        """Run after install to tell the Makefiles to use
        the compilers that Spack built the package with.

        If this isn't done, they'll have CC, CPP, and F77 set to
        Spack's generic cc and f77. We want them to be bound to
        whatever compiler they were built with."""

        kwargs = {'ignore_absent': True, 'backup': False, 'string': True}
        dirname = os.path.join(self.prefix, 'examples')

        cc_files = [
            'arkode/C_serial/Makefile',  'arkode/C_parallel/Makefile',
            'cvode/serial/Makefile',     'cvode/parallel/Makefile',
            'cvodes/serial/Makefile',    'cvodes/parallel/Makefile',
            'ida/serial/Makefile',       'ida/parallel/Makefile',
            'idas/serial/Makefile',      'idas/parallel/Makefile',
            'kinsol/serial/Makefile',    'kinsol/parallel/Makefile',
            'nvector/serial/Makefile',   'nvector/parallel/Makefile',
            'nvector/pthreads/Makefile'
        ]

        f77_files = [
            'arkode/F77_serial/Makefile', 'cvode/fcmix_serial/Makefile',
            'ida/fcmix_serial/Makefile',  'ida/fcmix_pthreads/Makefile',
            'kinsol/fcmix_serial/Makefile'
        ]

        for filename in cc_files:
            filter_file(os.environ['CC'], self.compiler.cc,
                        os.path.join(dirname, filename), **kwargs)

        for filename in f77_files:
            filter_file(os.environ['F77'], self.compiler.f77,
                        os.path.join(dirname, filename), **kwargs)
