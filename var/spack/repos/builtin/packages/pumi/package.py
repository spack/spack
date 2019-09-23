# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    git      = "https://github.com/SCOREC/core.git"

    maintainers = ['cwsmith']

    # We will use the scorec/core master branch as the 'nightly' version
    # of pumi in spack.  The master branch is more stable than the
    # scorec/core develop branch and we perfer not to expose spack users
    # to the added instability. The spack version string is 'develop' since
    # it compares greater than a numbered version (e.g., 2.1.0). The spack
    # version string 'master' compares less than a numbered version.
    version('develop', branch='master')
    version('2.2.1', commit='cd826205db21b8439026db1f6af61a8ed4a18564')  # tag 2.2.1
    version('2.2.0', commit='8c7e6f13943893b2bc1ece15003e4869a0e9634f')  # tag 2.2.0
    version('2.1.0', commit='840fbf6ec49a63aeaa3945f11ddb224f6055ac9f')

    variant('int64', default=False, description='Enable 64bit mesh entity ids')
    variant('shared', default=False, description='Build shared libraries')
    variant('zoltan', default=False, description='Enable Zoltan Features')
    variant('fortran', default=False, description='Enable FORTRAN interface')
    variant('simmodsuite', default='none',
            values=('none', 'base', 'kernels', 'full'),
            description="Enable Simmetrix SimModSuite Support: 'base' enables "
            "the minimum set of functionality, 'kernels' adds CAD kernel "
            "support to 'base', and 'full' enables all functionality.")

    depends_on('mpi')
    depends_on('cmake@3:', type='build')
    depends_on('zoltan', when='+zoltan')
    depends_on('zoltan+int64', when='+zoltan+int64')
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
            '-DBUILD_SHARED_LIBS=%s' % ('ON' if '+shared' in spec else 'OFF'),
            '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            '-DPUMI_FORTRAN_INTERFACE=%s' %
            ('ON' if '+fortran' in spec else 'OFF'),
            '-DMDS_ID_TYPE=%s' % ('long' if '+int64' in spec else 'int')
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
