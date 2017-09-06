##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import sys


class Sundials(Package):
    """SUNDIALS (SUite of Nonlinear and DIfferential/ALgebraic equation
    Solvers)"""

    homepage = "http://computation.llnl.gov/casc/sundials/"
    url = "http://computation.llnl.gov/projects/sundials-suite-nonlinear-differential-algebraic-equation-solvers/download/sundials-2.6.2.tar.gz"

    version('2.7.0', 'c304631b9bc82877d7b0e9f4d4fd94d3')
    version('2.6.2', '3deeb0ede9f514184c6bd83ecab77d95')

    variant('mpi',     default=True,
            description='Enable MPI parallelism')
    variant('lapack',  default=True,
            description='Use external BLAS/LAPACK libraries')
    variant('klu',     default=False,
            description='Enable KLU sparse, direct solver')
    variant('superlu', default=False,
            description='Enable SuperLU_MT sparse, direct solver')
    variant('openmp',  default=False,
            description='Enable OpenMP parallelism')
    variant('pthread', default=True,
            description='Enable Pthreads parallelism')
    variant('hypre', default=False,
            description='Enable Hypre parallel vector for MPI parallelism')

    depends_on('cmake',              type='build')
    depends_on('mpi',                when='+mpi')
    depends_on('mpi',                when='@2.7:+hypre')
    depends_on('hypre',              when='@2.7:+hypre')
    depends_on('blas',               when='+lapack')
    depends_on('lapack',             when='+lapack')
    depends_on('suite-sparse',       when='+klu')
    depends_on('superlu-mt+openmp',  when='+superlu+openmp')
    depends_on('superlu-mt+pthread', when='+superlu+pthread')

    def install(self, spec, prefix):

        def on_off(varstr):
            return 'ON' if varstr in self.spec else 'OFF'

        cmake_args = std_cmake_args[:]

        fortran_flag = self.compiler.pic_flag
        if spec.satisfies('%clang platform=darwin'):
            mpif77 = Executable(self.spec['mpi'].mpif77)
            libgfortran = LibraryList(mpif77('--print-file-name',
                                             'libgfortran.a', output=str))
            fortran_flag += ' ' + libgfortran.ld_flags

        cmake_args.extend([
            '-DBUILD_SHARED_LIBS=ON',
            '-DCMAKE_C_FLAGS={0}'.format(self.compiler.pic_flag),
            '-DCMAKE_Fortran_FLAGS={0}'.format(fortran_flag),
            '-DEXAMPLES_ENABLE=ON',
            '-DEXAMPLES_INSTALL=ON',
            '-DFCMIX_ENABLE=ON',
            '-DMPI_ENABLE=%s' % on_off('+mpi'),
            '-DLAPACK_ENABLE=%s' % on_off('+lapack'),
            '-DKLU_ENABLE=%s' % on_off('+klu'),
            '-DHYPRE_ENABLE=%s' % on_off('+hypre'),
            '-DSUPERLUMT_ENABLE=%s' % on_off('+superlu'),
            '-DOPENMP_ENABLE=%s' % on_off('+openmp'),
            '-DPTHREAD_ENABLE=%s' % on_off('+pthread')
        ])

        # MPI support
        if '+mpi' in spec:
            cmake_args.extend([
                '-DMPI_MPICC={0}'.format(spec['mpi'].mpicc),
                '-DMPI_MPIF77={0}'.format(spec['mpi'].mpif77)
            ])

        # Building with Hypre
        if '+hypre' in spec and spec.satisfies('@2.7:'):
            cmake_args.extend([
                '-DHYPRE_INCLUDE_DIR={0}'.format(
                    spec['hypre'].prefix.include),
                '-DHYPRE_LIBRARY_DIR={0}'.format(
                    spec['hypre'].prefix.lib)
            ])

        # Building with LAPACK and BLAS
        if '+lapack' in spec:
            cmake_args.extend([
                '-DLAPACK_LIBRARIES={0}'.format(
                    (spec['lapack'].libs +
                     spec['blas'].libs).joined(';')
                )
            ])

        # Building with KLU
        if '+klu' in spec:
            cmake_args.extend([
                '-DKLU_INCLUDE_DIR={0}'.format(
                    spec['suite-sparse'].prefix.include),
                '-DKLU_LIBRARY_DIR={0}'.format(
                    spec['suite-sparse'].prefix.lib)
            ])

        # Building with SuperLU_MT
        if '+superlu' in spec:
            cmake_args.extend([
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

        with working_dir('build', create=True):
            cmake('..', *cmake_args)

            make()
            make('install')

            if (sys.platform == 'darwin'):
                fix_darwin_install_name(prefix.lib)

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
