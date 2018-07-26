##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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
from spack import *


class Camellia(CMakePackage):
    """Camellia: user-friendly MPI-parallel adaptive finite element package,
       with support for DPG and other hybrid methods, built atop Trilinos.
    """

    homepage = "https://bitbucket.org/nateroberts/Camellia"
    git      = "https://bitbucket.org/nateroberts/camellia.git"

    maintainers = ['CamelliaDPG']

    version('master', branch='master')

    variant('moab', default=True, description='Compile with MOAB to include support for reading standard mesh formats')

    depends_on('trilinos+amesos+amesos2+belos+epetra+epetraext+exodus+ifpack+ifpack2+intrepid+intrepid2+kokkos+ml+muelu+sacado+shards+teuchos+tpetra+zoltan+mumps+superlu-dist+hdf5+zlib+pnetcdf@master,12.12.1:')
    depends_on('moab@:4', when='+moab')
    depends_on('hdf5@:1.8')
    depends_on('mpi')

    def cmake_args(self):
        spec = self.spec
        options = [
            '-DTrilinos_PATH:PATH=%s' % spec['trilinos'].prefix,
            '-DMPI_DIR:PATH=%s' % spec['mpi'].prefix,
            '-DBUILD_FOR_INSTALL:BOOL=ON'
        ]

        if '+moab' in spec:
            options.extend([
                '-DENABLE_MOAB:BOOL=ON',
                '-DMOAB_PATH:PATH=%s' % spec['moab'].prefix
            ])
        else:
            options.append('-DENABLE_MOAB:BOOL=OFF')

        return options
