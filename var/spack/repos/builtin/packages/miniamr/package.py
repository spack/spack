# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Miniamr(MakefilePackage):
    """Proxy Application. 3D stencil calculation with
       Adaptive Mesh Refinement (AMR)
    """

    homepage = "https://mantevo.org"
    url      = "https://github.com/Mantevo/miniAMR/archive/v1.4.0.tar.gz"

    tags = ['proxy-app', 'ecp-proxy-app']

    version('1.4.1', sha256='dd8e8d9fd0768cb4f2c5d7fe6989dfa6bb95a8461f04deaccdbb50b0dd51e97a')
    version('1.4.0', '3aab0247047a94e343709cf2e51cc46e')

    variant('mpi', default=True, description='Build with MPI support')

    depends_on('mpi', when="+mpi")

    @property
    def build_targets(self):
        targets = []
        if '+mpi' in self.spec:
            targets.append('CC={0}'.format(self.spec['mpi'].mpicc))
            targets.append('LD={0}'.format(self.spec['mpi'].mpicc))
            targets.append('LDLIBS=-lm')
        else:
            targets.append('CC={0}'.format(self.compiler.cc))
            targets.append('LD={0}'.format(self.compiler.cc))
        targets.append('--directory=ref')

        return targets

    def install(self, spec, prefix):
        # Manual installation
        mkdir(prefix.bin)
        mkdir(prefix.docs)

        install('ref/ma.x', prefix.bin)
        # Install Support Documents
        install('ref/README', prefix.docs)
