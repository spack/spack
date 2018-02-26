##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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

import os
import fnmatch
from spack import *


class Phist(CMakePackage):
    """ PHIST - a Pipelined, Hybrid-parallel Iterative Solver Toolkit.
        
PHIST provides implementations of and interfaces to block iterative solvers for sparse linear and eigenvalue problems.
In contrast to other libraries we support multiple backends (e.g. Trilinos, PETSc and our own optimized kernels),
and interfaces in multiple languages such as C, C++, Fortran 2003 and Python. PHIST has a clear focus on
portability and hardware performance: in particular we support row-major storage of block vectors and using GPUs (via
the ghost library or Trilinos/Tpetra).
"""

    homepage = "https://bitbucket.org/essex/phist/"
    
    # run expensive test suite (recommended oly if you have 12 physical cores, takes a few minutes)
    run_tests  = False
    smoke_test = True

    version('develop',
            git='https://bitbucket.org/essex/phist/phist.git', branch='devel')
    version('master',
            git='https://bitbucket.org/essex/phist/phist.git', branch='master')
    version('1.4.1', '53ca2c2c000a36790e1626ed1eb642e3',
            url='https://bitbucket.org/essex/phist/get/phist-1.4.1.tar.gz')

    # note: there is no virtual package for lapacke (the C bindings for lapack),
    # We look for a file like lapacke.h in the lapack prefix, if it is found we
    # pass it to phist's cmake, otherwise we hope that phist finds it itself.
    def lapacke_include_dir(self):
        prefix=self.spec['lapack'].prefix
        include_dir="NOTFOUND"
        for root, dir, files in os.walk(prefix):
            if fnmatch.filter(files, "*lapacke.h"):
                include_dir=root
                break
        return include_dir

    def cmake_args(self):
        spec=self.spec
        outlev=spec.variants['outlev'].value
        lapack_libs = (spec['lapack'].libs + spec['blas'].libs).joined(';')
        lapacke_inc = self.lapacke_include_dir()
        tpl_lapacke_include_dirs=''
        if lapacke_inc != "NOTFOUND":
            tpl_lapacke_include_dirs='-DTPL_LAPACKE_INCLUDE_DIRS='+lapacke_inc
        # Use everything until the first '+' sign as the kernel library.
        # Note that we already restrict the string to a list of given values,
        # so we don't need to check more carefully here.
        kernel_lib=spec.variants['kernel_lib'].value.split('+',1)[0]
                    
        args = ['-DPHIST_KERNEL_LIB=%s' % kernel_lib,
                '-DPHIST_OUTLEV=%s' % outlev,
                '-DTPL_LAPACKE_LIBRARIES=%s' % lapack_libs,
                tpl_lapacke_include_dirs,
                '-DPHIST_ENABLE_MPI:BOOL=%s' % ('ON' if '+mpi' in spec else 'OFF'),
                '-DBUILD_SHARED_LIBS:BOOL=%s' % ('ON' if '+shared' in spec else 'OFF'),
                '-DPHIST_USE_TRILINOS_TPLS:BOOL=%s' % ('ON' if '+trilinos' in spec else 'OFF'),
                '-DPHIST_USE_SOLVER_TPLS:BOOL=%s' % ('ON' if '+trilinos' in spec else 'OFF'),
                '-DPHIST_USE_PRECON_TPLS:BOOL=%s' % ('ON' if '+trilinos' in spec else 'OFF'),
                ];
                        
        return args

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def check(self):
        with working_dir(self.build_directory):
            make("check")


    @run_after('install')
    @on_package_attributes(smoke_test=True)
    def test_install(self):
        with working_dir(self.build_directory):
            make("test_install")

    variant(name='kernel_lib',   default='builtin',
            description='select the kernel library (backend) for phist',
            values=['builtin','epetra','tpetra','petsc','petsc+complex','eigen','ghost'])
    variant(name='outlev', default='2',            description='verbosity. 0: errors 1: +warnings 2: +info 3: +verbose 4: +extreme 5; +debug')

    variant('shared',  default=True, description='Enables the build of shared libraries')

    variant('mpi', default=True, description='enable/disable MPI (note that the kernel library must also support this)')
    variant('parmetis', default=False, description='enable/disable ParMETIS partitioning (only actually used with kernel_lib=builtin)')
    variant('trilinos', default=False, description='''enable/disable Trilinos third-party libraries. For all kernel_libs, we can use Belos and Anasazi iterative solvers.
    For the Trilinos backends (kernel_lib=epetra|tpetra) we can use preconditioner packages such as Ifpack, Ifpack2 and ML.''')

    # ###################### Dependencies ##########################

    # Everything should be compiled position independent (-fpic)
    depends_on('cmake@3.8:')
    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')
    depends_on('trilinos@12.12.1', when='+trilinos')
    depends_on('trilinos@12.12.1', when='kernel_lib=tpetra')
    # Epetra backend also works with older Trilinos versions
    depends_on('trilinos@11.12.1:12.12.1', when='kernel_lib=epetra')
    depends_on('petsc~complex', when='kernel_lib=petsc')
    depends_on('petsc+complex', when='kernel_lib=petsc+complex')
    depends_on('eigen', when='kernel_lib=eigen')
    depends_on('ghost', when='kernel_lib=ghost')
    
    depends_on('trilinos', when='+trilinos')
    depends_on('parmetis', when='+parmetis')


