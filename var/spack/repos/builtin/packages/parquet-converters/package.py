##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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

from spack import *


class ParquetConverters(CMakePackage):
    """Parquet conversion tools developed by Blue Brain Project, EPFL
    """
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/building/ParquetConverters"
    url      = "ssh://bbpcode.epfl.ch/building/ParquetConverters"

    version('develop', git=url)
    version('0.3', git=url, tag='v0.3', preferred=True)
    version('0.2.1', git=url, tag='v0.2.1')

    depends_on('hdf5+mpi')
    depends_on('highfive+mpi')
    depends_on('arrow+parquet')
    depends_on('arrow+parquet@0.12:', when='@0.4:')
    depends_on('snappy~shared')
    depends_on('synapsetool+mpi')
    depends_on('mpi')
    depends_on('range-v3', when='@0.4:')

    def cmake_args(self):
        return [
            '-DCMAKE_C_COMPILER={}'.format(self.spec['mpi'].mpicc),
            '-DCMAKE_CXX_COMPILER={}'.format(self.spec['mpi'].mpicxx),
            '-DNEURONPARQUET_USE_MPI=ON'
        ]
