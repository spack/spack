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
import os

from spack import *


class SynapseTool(CMakePackage):
    """Synapse format utilities.
    """
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/hpc/synapse-tool"
    url      = "ssh://bbpcode.epfl.ch/hpc/synapse-tool"

    version('dev-201806',
            commit='8c4bbe548006d7221f215f32c077338f169ba015',
            git=url,
            preferred=True,
            submodules=True)

    variant('mpi', default=True)

    depends_on('boost@1.60:')
    depends_on('hdf5@1.10:')
    depends_on('hdf5@1.10:~mpi', when='~mpi')
    depends_on('highfive@develop')
    depends_on('highfive@develop+mpi', when='+mpi')
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        args = [
            '-DLIBHDF5_ROOT={}'.format(self.spec['hdf5'].prefix),
            '-DBOOST_ROOT={}'.format(self.spec['boost'].prefix),
        ]
        if '+mpi' in self.spec:
            args.extend([
                '-DCMAKE_C_COMPILER={}'.format(self.spec['mpi'].mpicc),
                '-DCMAKE_CXX_COMPILER={}'.format(self.spec['mpi'].mpicxx),
                '-DSYNTOOL_WITH_MPI=ON',
            ])
        return args
