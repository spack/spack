# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hpccg(MakefilePackage):
    """Proxy Application. Intended to be the 'best approximation
       to an unstructured implicit finite element or finite volume
       application in 800 lines or fewer.'
    """

    homepage = "https://mantevo.org/about/applications/"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/HPCCG/HPCCG-1.0.tar.gz"

    tags = ['proxy-app']

    version('1.0', '2e99da1a89de5ef0844da5e6ffbf39dc')

    variant('mpi', default=True, description='Build with MPI support')
    variant('openmp', default=True, description='Build with OpenMP support')

    # Optional dependencies
    depends_on('mpi', when='+mpi')

    @property
    def build_targets(self):
        targets = []

        if '+mpi' in self.spec:
            targets.append('CXX={0}'.format(self.spec['mpi'].mpicxx))
            targets.append('LINKER={0}'.format(self.spec['mpi'].mpicxx))
            targets.append('USE_MPI=-DUSING_MPI')
        else:
            targets.append('CXX=c++')
            targets.append('LINKER=c++')

        if '+openmp' in self.spec:
            targets.append('USE_OMP=-DUSING_OMP')
            targets.append('OMP_FLAGS={0}'.format(self.compiler.openmp_flag))

        # Remove Compiler Specific Optimization Flags
        if '%gcc' not in self.spec:
            targets.append('CPP_OPT_FLAGS=')

        return targets

    def install(self, spec, prefix):
        # Manual installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install('test_HPCCG', prefix.bin)
        install('README', prefix.doc)
        install('weakScalingRunScript', prefix.bin)
        install('strongScalingRunScript', prefix.bin)
