##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
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
from spack import *


class NaluWind(CMakePackage):
    """Nalu-Wind: Wind energy focused variant of Nalu."""

    homepage = "https://github.com/exawind/nalu-wind"
    git      = "https://github.com/exawind/nalu-wind.git"

    maintainers = ['jrood-nrel']

    version('master', branch='master')

    variant('openfast', default=False,
            description='Compile with OpenFAST support')
    variant('tioga', default=False,
            description='Compile with Tioga support')
    variant('hypre', default=False,
            description='Compile with Hypre support')

    depends_on('mpi')
    depends_on('yaml-cpp@0.5.3:')
    depends_on('trilinos+exodus+tpetra+muelu+belos+ifpack2+amesos2+zoltan+stk+boost~superlu-dist+superlu+hdf5+zlib+pnetcdf+shards~hypre@master,develop')
    depends_on('openfast+cxx', when='+openfast')
    depends_on('tioga', when='+tioga')
    depends_on('hypre+mpi+int64', when='+hypre')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend([
            '-DTrilinos_DIR:PATH=%s' % spec['trilinos'].prefix,
            '-DYAML_DIR:PATH=%s' % spec['yaml-cpp'].prefix,
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            '-DMPI_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DMPI_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DMPI_Fortran_COMPILER=%s' % spec['mpi'].mpifc
        ])

        if '+openfast' in spec:
            options.extend([
                '-DENABLE_OPENFAST:BOOL=ON',
                '-DOpenFAST_DIR:PATH=%s' % spec['openfast'].prefix
            ])
        else:
            options.append('-DENABLE_OPENFAST:BOOL=OFF')

        if '+tioga' in spec:
            options.extend([
                '-DENABLE_TIOGA:BOOL=ON',
                '-DTIOGA_DIR:PATH=%s' % spec['tioga'].prefix
            ])
        else:
            options.append('-DENABLE_TIOGA:BOOL=OFF')

        if '+hypre' in spec:
            options.extend([
                '-DENABLE_HYPRE:BOOL=ON',
                '-DHYPRE_DIR:PATH=%s' % spec['hypre'].prefix
            ])
        else:
            options.append('-DENABLE_HYPRE:BOOL=OFF')

        return options
