# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Redset(CMakePackage):
    """Create MPI communicators for disparate redundancy sets"""

    homepage = "https://github.com/ecp-veloc/redset"
    url      = "https://github.com/ecp-veloc/redset/archive/v0.0.5.tar.gz"
    git      = "https://github.com/ecp-veloc/redset.git"
    tags = ['ecp']

    maintainers = ['CamStan', 'gonsie']

    version('main',  branch='main')
    version('0.2.0', sha256='0438b0ba56dafcd5694a8fceeb5a932901307353e056ab29817d30b8387f787f')
    version('0.1.0', sha256='baa75de0d0d6de64ade50cff3d38ee89fd136ce69869182bdaefccf5be5d286d')
    version('0.0.5', sha256='4db4ae59ab9d333a6d1d80678dedf917d23ad461c88b6d39466fc4bf6467d1ee')
    version('0.0.4', sha256='c33fce458d5582f01ad632c6fae8eb0a03eaef00e3c240c713b03bb95e2787ad')
    version('0.0.3', sha256='30ac1a960f842ae23a960a88b312af3fddc4795f2053eeeec3433a61e4666a76')

    depends_on('mpi')
    depends_on('kvtree+mpi')
    depends_on('rankstr')
    depends_on('zlib', type='link')

    variant('shared', default=True, description='Build with shared libraries')
    depends_on('kvtree+shared',  when='@0.1: +shared')
    depends_on('kvtree~shared',  when='@0.1: ~shared')
    depends_on('rankstr+shared', when='@0.1: +shared')
    depends_on('rankstr~shared', when='@0.1: ~shared')

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append(self.define('MPI_C_COMPILER', spec['mpi'].mpicc))
        args.append(self.define('WITH_KVTREE_PREFIX', spec['kvtree'].prefix))
        args.append(self.define('WITH_RANKSTR_PREFIX', spec['rankstr'].prefix))

        if spec.satisfies('@0.1.0:'):
            args.append(self.define_from_variant('BUILD_SHARED_LIBS', 'shared'))
        else:
            if spec.satisfies('platform=cray'):
                args.append(self.define('REDSET_LINK_STATIC', True))

        return args
