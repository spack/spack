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


class Magma(Package):
    """The MAGMA project aims to develop a dense linear algebra library
       similar to LAPACK but for heterogeneous/hybrid architectures,
       starting with current "Multicore+GPU" systems.
    """

    homepage = "http://icl.cs.utk.edu/magma/"
    url = "http://icl.cs.utk.edu/projectsfiles/magma/downloads/magma-2.2.0.tar.gz"

    # TODO: make develop version of Magma
    version('2.2.0', '6c1ebf4cdf63eb302ff6258ff8c49217')

    variant('shared',  default=True,
            description='Enables the build of shared libraries')

    depends_on('cuda')
    depends_on('blas')
    depends_on('lapack')

    def install(self, spec, prefix):

        # TODO fix the handling for -DADD_
        # TODO add -std=c++11 only when supported
        # TODO add -DMAGMA_NOAFFINITY only when needed
        # TODO support debug version that turns off -DNDEBUG
        # TODO supported make shared when shared property is on
        fd = open('make.inc', 'w')
        fd.write('DESTDIR = \n')
        fd.write('prefix = ' + prefix + '\n')
        fd.write('CC = ' + self.compiler.cc + '\n')
        fd.write('CXX = ' + self.compiler.cxx + '\n')
        fd.write('FORT = ' + self.compiler.fc + '\n')
        fd.write('CFLAGS    = -O3 $(FPIC) -DNDEBUG -DADD_ -std=c99 -DMAGMA_NOAFFINITY' + '\n')
        fd.write('CXXFLAGS  = -O3 $(FPIC) -DNDEBUG -DADD_ -std=c++11  -DMAGMA_NOAFFINITY' + '\n')
        fd.write('FFLAGS    = -O3 $(FPIC) -DNDEBUG -DADD_ ' + '\n')
        fd.write('F90FLAGS  = -O3 $(FPIC) -DNDEBUG -DADD_ ' + '\n')

        fd.write('ARCH = ar' + '\n')
        fd.write('ARCHFLAGS = cr' + '\n')
        fd.write('RANLIB = ranlib' + '\n')
        fd.write('FPIC      = -fPIC' + '\n')

        # BLAS/LAPACK libraries
        lapack_blas = spec['lapack'].lapack_libs + spec['blas'].blas_libs
        fd.write('LIB       = ' + lapack_blas.joined() + '\n')

        # Magma seems to require CUDA?
        fd.write('CUDADIR = ' + spec['cuda'].prefix + '\n')
        fd.write('NVCC = $(CUDADIR)/bin/nvcc' + '\n')
        fd.write('NVCCFLAGS = -O3 -DNDEBUG -DADD_  -Xcompiler "$(FPIC)"' + '\n')
        fd.write('LIBDIR    = -L$(CUDADIR)/lib' + '\n')
        fd.write('INC       = -I$(CUDADIR)/include' + '\n')
        fd.write('LIB      += -lcublas -lcusparse -lcudart -lcudadevrt' + '\n')
        fd.close()

        make('lib', parallel=True)
        # make('shared', parallel=False)
        make('install', parallel=False)
