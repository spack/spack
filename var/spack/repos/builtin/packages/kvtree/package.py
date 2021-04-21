# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kvtree(CMakePackage):
    """KVTree provides a fully extensible C datastructure modeled after perl
    hashes."""

    homepage = "https://github.com/ecp-veloc/KVTree"
    url      = "https://github.com/ecp-veloc/KVTree/archive/v1.1.1.tar.gz"
    git      = "https://github.com/ecp-veloc/kvtree.git"

    tags = ['ecp']

    version('master', branch='master')
    version('1.1.1', sha256='e3c652fa69e6f31da48fab57c302a9deb3e33ea41f96b6b4480a78eeb71e7659')
    version('1.1.0', sha256='34182f8e6c8f3c089376579cce3d18cfd93b59caf83649b204ed8456ac97400f')
    version('1.0.3', sha256='b892cf6c270ca6c15c0a816549bd5f8575a9ad2fca287d36e1116bd4cfe5c391')
    version('1.0.2', sha256='6b54f4658e5ebab747c0c2472b1505ac1905eefc8a0b2a97d8776f800ee737a3')

    variant('mpi', default=True, description="Build with MPI message packing")
    depends_on('mpi', when='+mpi')

    variant('file_lock', default='FLOCK',
            values=('FLOCK', 'FNCTL', 'NONE'),
            multi=False,
            description='File locking style for KVTree.')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+mpi'):
            args.append("-DMPI=ON")
            args.append("-DMPI_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        else:
            args.append("-DMPI=OFF")

        args.append('-DKVTREE_FILE_LOCK={0}'.format(
            self.spec.variants['file_lock'].value.upper()))

        if self.spec.satisfies('platform=cray'):
            args.append("-DKVTREE_LINK_STATIC=ON")
        return args
