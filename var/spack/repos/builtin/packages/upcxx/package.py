# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    version('2019.9.0', '7642877e05300e38f6fa0afbc6062788')
    version('2019.3.2', '844722cb0e8c0bc649017fce86469457')

    variant('cuda', default=False,
            description='Builds a CUDA-enabled version of UPC++')

    variant('cross', default=cross_detect(),
            description="UPC++ cross-compile target (autodetect by default)")

    conflicts('cross=none', when='platform=cray',
              msg='None is unacceptable on Cray.')

    depends_on('cuda', when='+cuda')

    def url_for_version(self, version):
        if version > Version('2019.3.2'):
            url = "https://bitbucket.org/berkeleylab/upcxx/downloads/upcxx-{0}.tar.gz"
        else:
            url = "https://bitbucket.org/berkeleylab/upcxx/downloads/upcxx-{0}-offline.tar.gz"
        return url.format(version)

    def setup_environment(self, spack_env, run_env):
        if 'platform=cray' in self.spec:
            spack_env.set('GASNET_CONFIGURE_ARGS', '--enable-mpi=probe')

        if 'cross=none' not in self.spec:
            spack_env.set('CROSS', self.spec.variants['cross'].value)

        if '+cuda' in self.spec:
            spack_env.set('UPCXX_CUDA', '1')
            spack_env.set('UPCXX_CUDA_NVCC', self.spec['cuda'].prefix.bin.nvcc)

        run_env.set('UPCXX_INSTALL', self.prefix)
        run_env.set('UPCXX', self.prefix.bin.upcxx)
        if 'platform=cray' in self.spec:
            run_env.set('UPCXX_GASNET_CONDUIT', 'aries')
            run_env.set('UPCXX_NETWORK', 'aries')

    def setup_dependent_package(self, module, dep_spec):
        dep_spec.upcxx = self.prefix.bin.upcxx

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('UPCXX_INSTALL', self.prefix)
        spack_env.set('UPCXX', self.prefix.bin.upcxx)
        if 'platform=cray' in self.spec:
            spack_env.set('UPCXX_GASNET_CONDUIT', 'aries')
            spack_env.set('UPCXX_NETWORK', 'aries')

    def install(self, spec, prefix):
        env['CC'] = self.compiler.cc
        env['CXX'] = self.compiler.cxx
        installsh = Executable("./install")
        installsh(prefix)
