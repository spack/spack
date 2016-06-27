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

class P4est(Package):
    """Dynamic management of a collection (a forest) of adaptive octrees in parallel"""
    homepage = "http://www.p4est.org"
    url      = "http://p4est.github.io/release/p4est-1.1.tar.gz"

    version('1.1', '37ba7f4410958cfb38a2140339dbf64f')

    variant('tests', default=True, description='Run small tests')

    # build dependencies
    depends_on('automake')
    depends_on('autoconf')
    depends_on('libtool@2.4.2:')

    # other dependencies
    depends_on('lua') # Needed for the submodule sc
    depends_on('mpi')
    depends_on('zlib')

    def install(self, spec, prefix):
        options = ['--enable-mpi',
                   '--enable-shared',
                   '--disable-vtk-binary',
                   '--without-blas',
                   'CPPFLAGS=-DSC_LOG_PRIORITY=SC_LP_ESSENTIAL',
                   'CFLAGS=-O2',
                   'CC=%s'  % self.spec['mpi'].mpicc,
                   'CXX=%s' % self.spec['mpi'].mpicxx,
                   'FC=%s'  % self.spec['mpi'].mpifc,
                   'F77=%s' % self.spec['mpi'].mpif77
                  ]

        configure('--prefix=%s' % prefix, *options)

        make()
        # Make tests optional as sometimes mpiexec can't be run with an error:
        # mpiexec has detected an attempt to run as root.
        # Running at root is *strongly* discouraged as any mistake (e.g., in
        # defining TMPDIR) or bug can result in catastrophic damage to the OS
        # file system, leaving your system in an unusable state.
        if '+tests' in self.spec:
          make("check")
        make("install")
