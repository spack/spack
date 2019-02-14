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


class Pumi(CMakePackage):
    """SCOREC RPI's Parallel Unstructured Mesh Infrastructure (PUMI).
       An efficient distributed mesh data structure and methods to support
       parallel adaptive analysis including general mesh-based operations,
       such as mesh entity creation/deletion, adjacency and geometric
       classification, iterators, arbitrary (field) data attachable to mesh
       entities, efficient communication involving entities duplicated
       across multiple tasks, migration of mesh entities between tasks,
       and dynamic load balancing."""

    homepage = "https://www.scorec.rpi.edu/pumi"
    url      = "https://github.com/SCOREC/core.git"

    version('2.1.0', git='https://github.com/SCOREC/core.git',
        commit='840fbf6ec49a63aeaa3945f11ddb224f6055ac9f')
    version('develop', git='https://github.com/SCOREC/core.git',
        branch='master')

    variant('zoltan', default=False, description='Enable Zoltan Features')
    variant('fortran', default=False, description='Enable FORTRAN interface')
    variant('simmodsuite', default='none',
        values=('none', 'base', 'kernels', 'full'),
        description="Enable Simmetrix SimModSuite Support: 'base' enables "
        "the minimum set of functionality, 'kernels' adds CAD kernel support "
        "to 'base', and 'full' enables all functionality.")

    depends_on('mpi')
    depends_on('cmake@3:', type='build')
    depends_on('zoltan', when='+zoltan')
    simbase = "+base"
    simkernels = simbase + "+parasolid+acis+discrete"
    simfull = simkernels + "+abstract+adv+advmodel\
                            +import+paralleladapt+parallelmesh"
    depends_on('simmetrix-simmodsuite' + simbase,
        when='simmodsuite=base')
    depends_on('simmetrix-simmodsuite' + simkernels,
        when='simmodsuite=kernels')
    depends_on('simmetrix-simmodsuite' + simfull,
        when='simmodsuite=full')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DSCOREC_CXX_WARNINGS=OFF',
            '-DENABLE_ZOLTAN=%s' % ('ON' if '+zoltan' in spec else 'OFF'),
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            '-DPUMI_FORTRAN_INTERFACE=%s' %
            ('ON' if '+fortran' in spec else 'OFF')
        ]
        if self.spec.satisfies('simmodsuite=base'):
            args.append('-DENABLE_SIMMETRIX=ON')
        if self.spec.satisfies('simmodsuite=kernels') or \
           self.spec.satisfies('simmodsuite=full'):
            args.append('-DENABLE_SIMMETRIX=ON')
            args.append('-DSIM_PARASOLID=ON')
            args.append('-DSIM_ACIS=ON')
            args.append('-DSIM_DISCRETE=ON')
            mpi_id = spec['mpi'].name + spec['mpi'].version.string
            args.append('-DSIM_MPI=' + mpi_id)
        return args
