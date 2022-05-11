# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Rankstr(CMakePackage):
    """Assign one-to-one mapping of MPI ranks to strings"""

    homepage = "https://github.com/ecp-veloc/rankstr"
    url      = "https://github.com/ecp-veloc/rankstr/archive/v0.0.3.tar.gz"
    git      = "https://github.com/ecp-veloc/rankstr.git"
    tags = ['ecp']

    maintainers = ['CamStan', 'gonsie']

    version('main',  branch='main')
    version('0.1.0', sha256='b68239d67b2359ecc067cc354f86ccfbc8f02071e60d28ae0a2449f2e7f88001')
    version('0.0.3', sha256='d32052fbecd44299e13e69bf2dd7e5737c346404ccd784b8c2100ceed99d8cd3')
    version('0.0.2', sha256='b88357bf88cdda9565472543225d6b0fa50f0726f6e2d464c92d31a98b493abb')

    depends_on('mpi')

    variant('shared', default=True, description='Build with shared libraries')

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append(self.define('MPI_C_COMPILER', spec['mpi'].mpicc))

        if spec.satisfies('@0.1.0:'):
            args.append(self.define_from_variant('BUILD_SHARED_LIBS', 'shared'))
        else:
            if spec.satisfies('platform=cray'):
                args.append(self.define('RANKSTR_LINK_STATIC', True))

        return args
