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


class Sundials(CMakePackage):
    """SUNDIALS (SUite of Nonlinear and DIfferential/ALgebraic equation
    Solvers)"""

    homepage = "https://computation.llnl.gov/projects/sundials"
    url = "https://computation.llnl.gov/projects/sundials/download/sundials-2.7.0.tar.gz"


    ##### Versions #####

    version('3.0.0-beta-2',
            git='https://github.com/LLNL/sundials.git', tag='v3.0.0-beta-2')
    version('2.7.0', 'c304631b9bc82877d7b0e9f4d4fd94d3', preferred=True)
    version('2.6.2', '3deeb0ede9f514184c6bd83ecab77d95')


    ##### Variants #####

    # SUNDIALS solvers
    variant('cvode',  default=True,
            description='Enable CVODE')
    variant('cvodes', default=True,
            description='Enable CVODES')
    variant('arkode', default=True,
            description='Enable ARKode')
    variant('ida',    default=True,
            description='Enable IDA')
    variant('idas',   default=True,
            description='Enable IDAS')
    variant('kinsol', default=True,
            description='Enable KINSOL')

    # Real precision type
    variant(
        'precision',
        default='double',
        description='''real type precision''',
        values=('single', 'double', 'extended'),
        multi=False
    )
    
    # Index type
    variant(
        'indextype',
        default='int64_t',
        description='''index integer type''',
        values=('int32_t', 'int64_t'),
        multi=False
    )

    # Parallelism 
    variant('mpi',     default=True,
            description='Enable MPI parallel vector')
    variant('openmp',  default=False,
            description='Enable OpenMP parallel vector')
    variant('pthread', default=False,
            description='Enable Pthreads parallel vector')
    variant('cuda',    default=False,
            description='Enable CUDA parallel vector')
    variant('raja',    default=False,
            description='Enable RAJA parallel vector')

    # External libraries
    variant('blas',       default=False,
            description='Enable external BLAS libraries')
    variant('lapack',     default=False,
            description='Enable external LAPACK libraries')
    variant('klu',        default=False,
            description='Enable KLU sparse, direct solver')
    variant('superlu-mt', default=False,
            description='Enable SuperLU_MT sparse, direct solver')
    variant('hypre',      default=False,
            description='Enable Hypre MPI parallel vector')
    variant('petsc',      default=False,
            description='Enable PETSc MPI parallel vector')

    # Library type
    variant('shared',  default=True,
            description='Build shared libraries')
    variant('static',  default=True,
            description='Build static libraries')

    # Fortran interface
    variant('fcmix', default=False,
            description='Enable Fortran interface')

    # Examples
    variant('examples-c', default=True,
            description='Enable C examples')
    variant('examples-cxx', default=False,
            description='Enable C++ examples')
    variant('examples-f77', default=True,
            description='Enable Fortran 77 examples')
    variant('examples-f90', default=False,
            description='Enable Fortran 90 examples')
    variant('examples-cuda', default=False,
            description='Enable CUDA examples')
    variant('examples-raja', default=False,
            description='Enable RAJA examples')
    variant('examples-install', default=True,
            description='Install examples')

    # Generic (std-c) math libraries (UNIX only)
    variant('generic-math', default=True,
            description='Use generic (std-c) math libraries on unix systems')

    # xSDK options
    variant('xsdk-defaults', default=False,
            description='Use default xSDK configuration')
    
    
    ##### Conflicts #####
    
    # Options added after v2.6.2
    conflicts('+hypre', when='@:2.6.2')
    conflicts('+petsc', when='@:2.6.2')
    
    # Options added after v2.7.0
    conflicts('+cuda',          when='@:2.7.0')
    conflicts('+raja',          when='@:2.7.0')
    conflicts('+blas',          when='@:2.7.0')
    conflicts('+indextype',     when='@:2.7.0')
    conflicts('+xsdk-defaults', when='@:2.7.0')
    conflicts('+examples-cuda', when='@:2.7.0')
    conflicts('+examples-raja', when='@:2.7.0')
    
    ##### Dependencies #####
    
    # Build dependencies
    depends_on('cmake', type='build')
    
    # MPI related dependencies
    depends_on('mpi', when='+mpi')
    depends_on('mpi', when='+hypre')
    depends_on('mpi', when='+petsc')
    
    # Other parallelism dependencies
    depends_on('cuda', when='+cuda')
    depends_on('raja', when='+raja')
    
    # External libraries
    depends_on('hypre',              when='+hypre')
    depends_on('petsc',              when='+petsc')
    depends_on('blas',               when='+blas')
    depends_on('lapack',             when='+lapack')
    depends_on('suite-sparse',       when='+klu')
    depends_on('superlu-mt+openmp',  when='+superlu-mt+openmp')
    depends_on('superlu-mt+pthread', when='+superlu-mt+pthread')
    
    
    ##### SUNDIALS Settings #####
    
    def cmake_args(self):
        spec   = self.spec
        prefix = self.spec.prefix
                
        def on_off(varstr):
            return 'ON' if varstr in self.spec else 'OFF'
        
        fortran_flag = self.compiler.pic_flag
        if spec.satisfies('%clang platform=darwin'):
            mpif77 = Executable(self.spec['mpi'].mpif77)
            libgfortran = LibraryList(mpif77('--print-file-name',
                                             'libgfortran.a', output=str))
            fortran_flag += ' ' + libgfortran.ld_flags

        # SUNDIALS solvers
        args = [
            '-DBUILD_CVODE=%s'  % on_off('+cvode'),
            '-DBUILD_CVODES=%s' % on_off('+cvodes'),
            '-DBUILD_ARKODE=%s' % on_off('+arkode'),
            '-DBUILD_IDA=%s'    % on_off('+ida'),
            '-DBUILD_IDAS=%s'   % on_off('+idas'),
            '-DBUILD_KINSOL=%s' % on_off('+kinsol')
        ]
        
        # precision
        if 'precision=single' in spec:
            args.extend(['-DSUNDIALS_PRECISION=single'])
        elif 'precision=double' in spec:
            args.extend(['-DSUNDIALS_PRECISION=double'])
        elif 'precision=extended' in spec:
            args.extend(['-DSUNDIALS_PRECISION=extended'])
        
        # index type (after v2.7.0)
        if not spec.satisfies('@:2.7.0'):
            if 'indextype=int32_t' in spec:
                args.extend(['-DSUNDIALS_INDEX_TYPE=int32_t'])
            elif 'indextype=int64_t' in spec:
                args.extend(['-DSUNDIALS_INDEX_TYPE=int64_t'])
        
        # Fortran interface
        args.extend([
            '-DFCMIX_ENABLE=%s' % on_off('+fcmix')
        ])
        
        # library type
        args.extend([
            '-DBUILD_SHARED_LIBS=%s' % on_off('+shared'),
            '-DBUILD_STATIC_LIBS=%s' % on_off('+static')
        ])

        # generic (std-c) math libraries
        args.extend([
            '-DUSE_GENERIC_MATH=%s' % on_off('+generic-math')       
        ])

        # parallelism 
        args.extend([
            '-DMPI_ENABLE=%s'     % on_off('+mpi'),
            '-DOPENMP_ENABLE=%s'  % on_off('+openmp'),
            '-DPTHREAD_ENABLE=%s' % on_off('+pthread'),
            '-DCUDA_ENABLE=%s'    % on_off('+cuda'),
            '-DRAJA_ENABLE=%s'    % on_off('+raja'),
        ])
        
        # MPI support
        if '+mpi' in spec:
            args.extend([
                '-DMPI_MPICC={0}'.format(spec['mpi'].mpicc)
            ])
            if 'examples-cxx' in spec:
                args.extend([
                    '-DMPI_MPICXX={0}'.format(spec['mpi'].mpicxx)
                ])
            if ('+fcmix' in spec) and ('+examples-f77' in spec):
                args.extend([
                    '-DMPI_MPIF77={0}'.format(spec['mpi'].mpif77)
                ])
            if ('+fcmix' in spec) and ('+examples-f90' in spec):
                args.extend([
                    '-DMPI_MPIF90={0}'.format(spec['mpi'].mpifc)
                ])

        # Building with LAPACK and BLAS
        if spec.satisfies('@:2.7.0'):
            if '+lapack' in spec:
                args.extend([
                    '-DLAPACK_LIBRARIES={0}'.format(
                        (spec['lapack'].libs +
                         spec['blas'].libs).joined(';')
                    )
                ]) 
        else:
            if '+blas' in spec:
                args.extend([
                    '-DBLAS_ENABLE=ON',
                    '-DBLAS_LIBRARIES={0}'.format(spec['blas'].libs),
                ])
            if '+lapack' in spec:
                args.extend([
                    '-DLAPACK_ENABLE=ON',
                    '-DLAPACK_LIBRARIES={0}'.format(spec['lapack'].libs),
                ])

        # Building with KLU
        if '+klu' in spec:
            args.extend([
                '-DKLU_ENABLE=ON',
                '-DKLU_INCLUDE_DIR={0}'.format(
                    spec['suite-sparse'].prefix.include),
                '-DKLU_LIBRARY_DIR={0}'.format(
                    spec['suite-sparse'].prefix.lib),
            ])

        # Building with SuperLU_MT
        if '+superlu-mt' in spec:
            args.extend([
                '-DSUPERLUMT_ENABLE=ON',
                '-DSUPERLUMT_INCLUDE_DIR={0}'.format(
                    spec['superlu-mt'].prefix.include),
                '-DSUPERLUMT_LIBRARY_DIR={0}'.format(
                    spec['superlu-mt'].prefix.lib)
            ])
            if '+openmp' in spec:
                args.append('-DSUPERLUMT_THREAD_TYPE=OpenMP')
            elif '+pthread' in spec:
                args.append('-DSUPERLUMT_THREAD_TYPE=Pthread')
            else:
                msg = 'You must choose either +openmp or +pthread when '
                msg += 'building with SuperLU_MT'
                raise RuntimeError(msg)

        # Building with Hypre
        if '+hypre' in spec:
            args.extend([
                '-DHYPRE_ENABLE=ON',
                '-DHYPRE_INCLUDE_DIR={0}'.format(
                    spec['hypre'].prefix.include),
                '-DHYPRE_LIBRARY_DIR={0}'.format(
                    spec['hypre'].prefix.lib)
            ])

        # Building with PETSc
        if '+petsc' in spec:
            args.extend([
                '-DPETSC_ENABLE=ON',
                '-DPETSC_INCLUDE_DIR={0}'.format(
                    spec['petsc'].prefix.include),
                '-DPETSC_LIBRARY_DIR={0}'.format(
                    spec['petsc'].prefix.lib)
            ])

        # Examples
        if not spec.satisfies('@:2.7.0'):
            args.extend([
                '-DEXAMPLES_ENABLE_C=%s'    % on_off('+examples-c'),
                '-DEXAMPLES_ENABLE_CXX=%s'  % on_off('+examples-cxx'),
                '-DEXAMPLES_ENABLE_F77=%s'  % on_off('+examples-f77'),
                '-DEXAMPLES_ENABLE_F90=%s'  % on_off('+examples-f90'),
                '-DEXAMPLES_ENABLE_CUDA=%s' % on_off('+examples-cuda'),
                '-DEXAMPLES_ENABLE_RAJA=%s' % on_off('+examples-raja')
            ])
        else:
            args.extend([
                '-DEXAMPLES_ENABLE=%s' % on_off('+examples-c'),
                '-DCXX_ENABLE=%s'      % on_off('+examples-cxx'),
                '-DF90_ENABLE=%s'      % on_off('+examples-f90')
            ])

        args.extend([
            '-DEXAMPLES_INSTALL=%s' % on_off('+examples-install')
        ])

        return args


    ##### SUNDIALS xSDK Settings #####
    
    @when('xsdk-defaults=True')
    def cmake_args(self):
        spec   = self.spec
        prefix = self.spec.prefix
                
        def on_off(varstr):
            return 'ON' if varstr in self.spec else 'OFF'
        
        fortran_flag = self.compiler.pic_flag
        if spec.satisfies('%clang platform=darwin'):
            mpif77 = Executable(self.spec['mpi'].mpif77)
            libgfortran = LibraryList(mpif77('--print-file-name',
                                             'libgfortran.a', output=str))
            fortran_flag += ' ' + libgfortran.ld_flags

        # SUNDIALS solvers
        args = [
            '-DBUILD_CVODE=%s'  % on_off('+cvode'),
            '-DBUILD_CVODES=%s' % on_off('+cvodes'),
            '-DBUILD_ARKODE=%s' % on_off('+arkode'),
            '-DBUILD_IDA=%s'    % on_off('+ida'),
            '-DBUILD_IDAS=%s'   % on_off('+idas'),
            '-DBUILD_KINSOL=%s' % on_off('+kinsol')
        ]
        
        # precision
        if 'precision=single' in spec:
            args.extend(['-DXSDK_PRECISION=single'])
        elif 'precision=double' in spec:
            args.extend(['-DXSDK_PRECISION=double'])
        elif 'precision=extended' in spec:
            args.extend(['-DXSDK_PRECISION=quad'])
        
        # index type (after v2.7.0)
        if 'indextype=int32_t' in spec:
            args.extend(['-DXSDK_INDEX_SIZE=32'])
        elif 'indextype=int64_t' in spec:
            args.extend(['-DXSDK_INDEX_SIZE=64'])
        
        # Fortran interface
        args.extend([
            '-DXSDK_ENABLE_FORTRAN=%s' % on_off('+fcmix')
        ])
        
        # library type
        args.extend([
            '-DBUILD_SHARED_LIBS=%s' % on_off('+shared'),
            '-DBUILD_STATIC_LIBS=%s' % on_off('+static')
        ])

        # generic (std-c) math libraries
        args.extend([
            '-DUSE_GENERIC_MATH=%s' % on_off('+generic-math')       
        ])

        # parallelism 
        args.extend([
            '-DMPI_ENABLE=%s'     % on_off('+mpi'),
            '-DOPENMP_ENABLE=%s'  % on_off('+openmp'),
            '-DPTHREAD_ENABLE=%s' % on_off('+pthread'),
            '-DCUDA_ENABLE=%s'    % on_off('+cuda'),
            '-DRAJA_ENABLE=%s'    % on_off('+raja'),
        ])
        
        # MPI support
        if '+mpi' in spec:
            args.extend([
                '-DMPI_MPICC={0}'.format(spec['mpi'].mpicc)
            ])
            if 'examples-cxx' in spec:
                args.extend([
                    '-DMPI_MPICXX={0}'.format(spec['mpi'].mpicxx)
                ])
            if ('+fcmix' in spec) and ('+examples-f77' in spec):
                args.extend([
                    '-DMPI_MPIF77={0}'.format(spec['mpi'].mpif77)
                ])
            if ('+fcmix' in spec) and ('+examples-f90' in spec):
                args.extend([
                    '-DMPI_MPIF90={0}'.format(spec['mpi'].mpifc)
                ])

        # Building with BLAS
        if '+blas' in spec:
            args.extend([
                '-DTPL_ENABLE_BLAS=ON',
                '-DTPL_BLAS_LIBRARIES={0}'.format(spec['blas'].libs),
            ])

        # Building with LAPACK
        if '+lapack' in spec:
            args.extend([
                '-DTPL_ENABLE_LAPACK=ON',
                '-DTPL_LAPACK_LIBRARIES={0}'.format(spec['lapack'].libs),
            ])

        # Building with KLU
        if '+klu' in spec:
            args.extend([
                '-DTPL_ENABLE_KLU=ON',
                '-DTPL_KLU_INCLUDE_DIRS={0}'.format(
                    spec['suite-sparse'].prefix.include),
                '-DTPL_KLU_LIBRARIES={0}'.format(
                    spec['suite-sparse'].prefix.lib),
            ])

        # Building with SuperLU_MT
        if '+superlu-mt' in spec:
            args.extend([
                '-DTPL_ENABLE_SUPERLUMT=ON',
                '-DTPL_SUPERLUMT_INCLUDE_DIRS={0}'.format(
                    spec['superlu-mt'].prefix.include),
                '-DTPL_SUPERLUMT_LIBRARIES={0}'.format(
                    spec['superlu-mt'].prefix.lib)
            ])
            if '+openmp' in spec:
                args.append('-DTPL_SUPERLUMT_THREAD_TYPE=OpenMP')
            elif '+pthread' in spec:
                args.append('-DTPL_SUPERLUMT_THREAD_TYPE=Pthread')
            else:
                msg = 'You must choose either +openmp or +pthread when '
                msg += 'building with SuperLU_MT'
                raise RuntimeError(msg)

        # Building with Hypre
        if '+hypre' in spec:
            args.extend([
                '-DTPL_ENABLE_HYPRE=ON',
                '-DTPL_HYPRE_INCLUDE_DIRS={0}'.format(
                    spec['hypre'].prefix.include),
                '-DTPL_HYPRE_LIBRARIES={0}'.format(
                    spec['hypre'].prefix.lib)
            ])

        # Building with PETSc
        if '+petsc' in spec:
            args.extend([
                '-DTPL_ENABLE_PETSC=ON',
                '-DTPL_PETSC_INCLUDE_DIRS={0}'.format(
                    spec['petsc'].prefix.include),
                '-DTPL_PETSC_LIBRARIES={0}'.format(
                    spec['petsc'].prefix.lib)
            ])

        # Examples
        args.extend([
            '-DEXAMPLES_ENABLE_C=%s'    % on_off('+examples-c'),
            '-DEXAMPLES_ENABLE_CXX=%s'  % on_off('+examples-cxx'),
            '-DEXAMPLES_ENABLE_F77=%s'  % on_off('+examples-f77'),
            '-DEXAMPLES_ENABLE_F90=%s'  % on_off('+examples-f90'),
            '-DEXAMPLES_ENABLE_CUDA=%s' % on_off('+examples-cuda'),
            '-DEXAMPLES_ENABLE_RAJA=%s' % on_off('+examples-raja'),
            '-DEXAMPLES_INSTALL=%s'     % on_off('+examples-install')
        ])

        return args


    ##### Post Install Fixes #####

    @run_after('install')
    def post_install(self):
        prefix = self.spec.prefix

        if (sys.platform == 'darwin'):
            fix_darwin_install_name(prefix.lib)

        install('LICENSE', prefix)


    ##### Fix Example Makefiles #####

    @run_after('install')
    def filter_compilers(self):
        """Run after install to tell the Makefiles to use
        the compilers that Spack built the package with.

        If this isn't done, they'll have CC, CPP, and F77 set to
        Spack's generic cc and f77. We want them to be bound to
        whatever compiler they were built with."""

        kwargs = {'ignore_absent': True, 'backup': False, 'string': True}
        dirname = os.path.join(self.prefix, 'examples')

        cc_files = [
            'arkode/C_openmp/Makefile',
            'arkode/C_parallel/Makefile',
            'arkode/C_parhyp/Makefile',
            'arkode/C_serial/Makefile',
            'cvode/C_openmp/Makefile',
            'cvode/parallel/Makefile',
            'cvode/parhyp/Makefile',
            'cvode/serial/Makefile',
            'cvodes/C_openmp/Makefile',
            'cvodes/parallel/Makefile',
            'cvodes/serial/Makefile',
            'ida/C_openmp/Makefile',
            'ida/parallel/Makefile',
            'ida/petsc/Makefile',
            'ida/serial/Makefile',
            'idas/C_openmp/Makefile',
            'idas/parallel/Makefile',
            'idas/serial/Makefile', 
            'kinsol/C_openmp/Makefile',
            'kinsol/parallel/Makefile',
            'kinsol/serial/Makefile',
            'nvector/C_openmp/Makefile',
            'nvector/parallel/Makefile',
            'nvector/parhyp/Makefile',
            'nvector/petsc/Makefile',
            'nvector/pthreads/Makefile',
            'nvector/serial/Makefile',
            'sunlinsol/band/Makefile',
            'sunlinsol/dense/Makefile',
            'sunlinsol/klu/Makefile',
            'sunlinsol/lapackband/Makefile',
            'sunlinsol/lapackdense/Makefile',
            'sunlinsol/pcg/parallel/Makefile',
            'sunlinsol/pcg/serial/Makefile',
            'sunlinsol/spbcgs/parallel/Makefile',
            'sunlinsol/spbcgs/serial/Makefile',
            'sunlinsol/spfgmr/parallel/Makefile',
            'sunlinsol/spfgmr/serial/Makefile',
            'sunlinsol/spgmr/parallel/Makefile',
            'sunlinsol/spgmr/serial/Makefile',
            'sunlinsol/sptfqmr/parallel/Makefile',
            'sunlinsol/sptfqmr/serial/Makefile',
            'sunlinsol/superlumt/Makefile',
            'sunmatrix/band/Makefile',
            'sunmatrix/dense/Makefile',
            'sunmatrix/sparse/Makefile'
        ]

        cxx_files = [
            'arkode/CXX_parallel/Makefile',
            'arkode/CXX_serial/Makefile'
            'cvode/cuda/Makefile',
            'cvode/raja/Makefile',
            'nvector/cuda/Makefile',
            'nvector/raja/Makefile'
        ]

        f77_files = [
            'arkode/F77_parallel/Makefile',
            'arkode/F77_serial/Makefile',
            'cvode/fcmix_parallel/Makefile',
            'cvode/fcmix_serial/Makefile',
            'ida/fcmix_openmp/Makefile',
            'ida/fcmix_parallel/Makefile',
            'ida/fcmix_pthreads/Makefile',
            'ida/fcmix_serial/Makefile',
            'kinsol/fcmix_parallel/Makefile',
            'kinsol/fcmix_serial/Makefile'
        ]

        f90_files = [
            'arkode/F90_parallel/Makefile',
            'arkode/F90_serial/Makefile'
        ]

        for filename in cc_files:
            filter_file(os.environ['CC'], self.compiler.cc,
                        os.path.join(dirname, filename), **kwargs)

        for filename in cc_files:
            filter_file(r'^CPP\s*=.*', self.compiler.cc,
                        os.path.join(dirname, filename), **kwargs)

        for filename in cxx_files:
            filter_file(os.environ['CXX'], self.compiler.cxx,
                        os.path.join(dirname, filename), **kwargs)

        for filename in cxx_files:
            filter_file(r'^CPP\s*=.*', self.compiler.cc,
                        os.path.join(dirname, filename), **kwargs)

        for filename in f77_files:
            filter_file(os.environ['F77'], self.compiler.f77,
                        os.path.join(dirname, filename), **kwargs)

        for filename in f90_files:
            filter_file(os.environ['FC'], self.compiler.fc,
                        os.path.join(dirname, filename), **kwargs)
