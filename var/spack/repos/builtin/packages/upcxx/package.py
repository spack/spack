# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


def cross_detect():
    if spack.architecture.platform().name == 'cray':
        if which('srun'):
            return 'cray-aries-slurm'
        if which('alps'):
            return 'cray-aries-alps'
    return 'none'


class Upcxx(Package):
    """UPC++ is a C++ library that supports Partitioned Global Address Space
    (PGAS) programming, and is designed to interoperate smoothly and
    efficiently with MPI, OpenMP, CUDA and AMTs. It leverages GASNet-EX to
    deliver low-overhead, fine-grained communication, including Remote Memory
    Access (RMA) and Remote Procedure Call (RPC)."""

    homepage = "https://upcxx.lbl.gov"
    maintainers = ['bonachea']

    version('2019.9.0', sha256='7d67ccbeeefb59de9f403acc719f52127a30801a2c2b9774a1df03f850f8f1d4')
    version('2019.3.2', sha256='dcb0b337c05a0feb2ed5386f5da6c60342412b49cab10f282f461e74411018ad')

    variant('cuda', default=False,
            description='Builds a CUDA-enabled version of UPC++')

    variant('cross', default=cross_detect(),
            description="UPC++ cross-compile target (autodetect by default)")

    conflicts('cross=none', when='platform=cray',
              msg='None is unacceptable on Cray.')

    depends_on('cuda', when='+cuda')
    depends_on('python@2.7.5:2.999', type=("build", "run"))

    def url_for_version(self, version):
        if version > Version('2019.3.2'):
            url = "https://bitbucket.org/berkeleylab/upcxx/downloads/upcxx-{0}.tar.gz"
        else:
            url = "https://bitbucket.org/berkeleylab/upcxx/downloads/upcxx-{0}-offline.tar.gz"
        return url.format(version)

    def setup_build_environment(self, env):
        if 'platform=cray' in self.spec:
            env.set('GASNET_CONFIGURE_ARGS', '--enable-mpi=probe')

        if 'cross=none' not in self.spec:
            env.set('CROSS', self.spec.variants['cross'].value)

        if '+cuda' in self.spec:
            env.set('UPCXX_CUDA', '1')
            env.set('UPCXX_CUDA_NVCC', self.spec['cuda'].prefix.bin.nvcc)

    def setup_run_environment(self, env):
        env.set('UPCXX_INSTALL', self.prefix)
        env.set('UPCXX', self.prefix.bin.upcxx)
        if 'platform=cray' in self.spec:
            env.set('UPCXX_GASNET_CONDUIT', 'aries')
            env.set('UPCXX_NETWORK', 'aries')

    def setup_dependent_package(self, module, dep_spec):
        dep_spec.upcxx = self.prefix.bin.upcxx

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('UPCXX_INSTALL', self.prefix)
        env.set('UPCXX', self.prefix.bin.upcxx)
        if 'platform=cray' in self.spec:
            env.set('UPCXX_GASNET_CONDUIT', 'aries')
            env.set('UPCXX_NETWORK', 'aries')

    def install(self, spec, prefix):
        env['CC'] = self.compiler.cc
        env['CXX'] = self.compiler.cxx
        installsh = Executable("./install")
        installsh(prefix)
