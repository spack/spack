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
import platform


class Hpl(Package):
    """HPL is a software package that solves a (random) dense linear system
    in double precision (64 bits) arithmetic on distributed-memory computers.
    It can thus be regarded as a portable as well as freely available
    implementation of the High Performance Computing Linpack Benchmark."""

    homepage = "http://www.netlib.org/benchmark/hpl/"
    url      = "http://www.netlib.org/benchmark/hpl/hpl-2.2.tar.gz"

    version('2.2', '0eb19e787c3dc8f4058db22c9e0c5320')

    variant('openmp', default=False, description='Enable OpenMP support')

    depends_on('mpi@1.1:')
    depends_on('blas')

    parallel = False

    def configure(self, spec, arch):
        # List of configuration options
        # Order is important
        config = []

        # OpenMP support
        if '+openmp' in spec:
            config.append(
                'OMP_DEFS     = {0}'.format(self.compiler.openmp_flag)
            )

        config.extend([
            # Shell
            'SHELL        = /bin/sh',
            'CD           = cd',
            'CP           = cp',
            'LN_S         = ln -fs',
            'MKDIR        = mkdir -p',
            'RM           = /bin/rm -f',
            'TOUCH        = touch',
            # Platform identifier
            'ARCH         = {0}'.format(arch),
            # HPL Directory Structure / HPL library
            'TOPdir       = {0}'.format(os.getcwd()),
            'INCdir       = $(TOPdir)/include',
            'BINdir       = $(TOPdir)/bin/$(ARCH)',
            'LIBdir       = $(TOPdir)/lib/$(ARCH)',
            'HPLlib       = $(LIBdir)/libhpl.a',
            # Message Passing library (MPI)
            'MPinc        = -I{0}'.format(spec['mpi'].prefix.include),
            'MPlib        = -L{0}'.format(spec['mpi'].prefix.lib),
            # Linear Algebra library (BLAS or VSIPL)
            'LAinc        = {0}'.format(spec['blas'].prefix.include),
            'LAlib        = {0}'.format(spec['blas'].libs.joined()),
            # F77 / C interface
            'F2CDEFS      = -DAdd_ -DF77_INTEGER=int -DStringSunStyle',
            # HPL includes / libraries / specifics
            'HPL_INCLUDES = -I$(INCdir) -I$(INCdir)/$(ARCH) ' +
            '-I$(LAinc) -I$(MPinc)',
            'HPL_LIBS     = $(HPLlib) $(LAlib) $(MPlib)',
            'HPL_OPTS     = -DHPL_DETAILED_TIMING -DHPL_PROGRESS_REPORT',
            'HPL_DEFS     = $(F2CDEFS) $(HPL_OPTS) $(HPL_INCLUDES)',
            # Compilers / linkers - Optimization flags
            'CC           = {0}'.format(spec['mpi'].mpicc),
            'CCNOOPT      = $(HPL_DEFS)',
            'CCFLAGS      = $(HPL_DEFS) -O3',
            'LINKER       = $(CC)',
            'LINKFLAGS    = $(CCFLAGS) $(OMP_DEFS)',
            'ARCHIVER     = ar',
            'ARFLAGS      = r',
            'RANLIB       = echo'
        ])

        # Write configuration options to include file
        with open('Make.{0}'.format(arch), 'w') as makefile:
            for var in config:
                makefile.write('{0}\n'.format(var))

    def install(self, spec, prefix):
        # Arch used for file naming purposes only
        arch = '{0}-{1}'.format(platform.system(), platform.processor())

        # Generate Makefile include
        self.configure(spec, arch)

        make('arch={0}'.format(arch))

        # Manual installation
        install_tree(join_path('bin', arch), prefix.bin)
        install_tree(join_path('lib', arch), prefix.lib)
        install_tree(join_path('include', arch), prefix.include)
        install_tree('man', prefix.man)
