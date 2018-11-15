# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Adlbx(AutotoolsPackage):
    """ADLB/X: Master-worker library + work stealing and data dependencies"""

    homepage = 'http://swift-lang.org/Swift-T'
    url      = 'http://swift-lang.github.io/swift-t-downloads/spack/adlbx-0.0.0.tar.gz'

    version('0.9.1', '07151ddef5fb83d8f4b40700013d9daf')
    version('0.8.0', '34ade59ce3be5bc296955231d47a27dd')

    depends_on('exmcutils@:0.5.3', when='@:0.8.0')
    depends_on('exmcutils', when='@0.9.1:')
    depends_on('mpi')

    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        spack_env.set('CC', spec['mpi'].mpicc)
        spack_env.set('CXX', spec['mpi'].mpicxx)
        spack_env.set('CXXLD', spec['mpi'].mpicxx)

    def configure_args(self):
        args = ['--with-c-utils=' + self.spec['exmcutils'].prefix]
        return args
