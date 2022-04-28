# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spath(CMakePackage):
    """Represent and manipulate file system paths"""

    homepage = "https://github.com/ecp-veloc/spath"
    url      = "https://github.com/ECP-VeloC/spath/archive/v0.0.2.tar.gz"
    git      = "https://github.com/ecp-veloc/spath.git"
    tags = ['ecp']

    maintainers = ['CamStan', 'gonsie']

    version('main',  branch='main')
    version('0.1.0', sha256='2cfc635b2384d3f92973c7aea173dabe47da112d308f5098e6636e4b2f4a704c')
    version('0.0.2', sha256='7a65be59c3d27e92ed4718fba1a97a4a1c68e0a552b54de13d58afe3d8199cf7')
    version('0.0.1', sha256='f41c0ac74e6fb8acfd0c072d756db0fc9c00441f22be492cc4ad25f7fb596a24')

    depends_on('zlib', type='link', when='@:0.0.2')

    variant('mpi', default=True, description='Build with MPI support')
    depends_on('mpi', when='+mpi')

    variant('shared', default=True, description='Build with shared libraries')

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append(self.define_from_variant('MPI'))
        if '+mpi' in spec:
            args.append(self.define('MPI_C_COMPILER', spec['mpi'].mpicc))

        if spec.satisfies('@0.1.0:'):
            args.append(self.define_from_variant('BUILD_SHARED_LIBS', 'shared'))
        else:
            if spec.satisfies('platform=cray'):
                args.append(self.define('SPATH_LINK_STATIC', True))

        return args
