# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pdc(CMakePackage):
    """Proactive Data Containers (PDC) software provides an object-centric
    API and a runtime system with a set of data object management services.
    These services allow placing data in the memory and storage hierarchy,
    performing data movement asynchronously, and providing scalable
    metadata operations to find data objects."""

    homepage = "https://pdc.readthedocs.io/en/latest/"
    url      = "https://github.com/hpc-io/pdc/archive/refs/tags/0.1.tar.gz"

    maintainers = ['houjun', 'sbyna']

    version('0.1', sha256='24787806a30cd1cda1fed17220a62e768bdba5de56877f2ea7126279ff2a4f69')

    conflicts('%clang')
    depends_on('libfabric@1.11.2')
    depends_on('mercury')
    depends_on('mpi')

    root_cmakelists_dir = 'src'

    def cmake_args(self):
        args = [
            self.define('MPI_C_COMPILER', self.spec['mpi'].mpicc),
            self.define('BUILD_MPI_TESTING', 'ON'),
            self.define('BUILD_SHARED_LIBS', 'ON'),
            self.define('BUILD_TESTING', 'ON'),
            self.define('PDC_ENABLE_MPI', 'ON'),
            self.define('CMAKE_C_COMPILER', self.spec['mpi'].mpicc)
        ]

        if self.spec.satisfies('platform=cray'):
            args.append("-DRANKSTR_LINK_STATIC=ON")
        return args
