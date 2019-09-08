# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import llnl.util.tty as tty
import os


def detect_scheduler():
    if (os.environ.get('CROSS') is None):
        srunbin = which('srun')
        if srunbin is None:
            aprunbin = which('aprun')
            if aprunbin is None:
                tty.warn("CROSS has not been set, however "
                         "cannot detect scheduler.")
                return 'none'
            else:
                tty.warn("CROSS has not been set, however "
                         "aprun has been found, assuming alps scheduler.")
                return 'alps'
        else:
            tty.warn("CROSS has not been set, however "
                     "srun has been found, assuming slurm scheduler.")
            return 'slurm'
    else:
        tty.warn("CROSS has been set to %s by the user."
                 % os.environ.get('CROSS'))
        return 'user'


class Upcxx(Package):
    """UPC++ is a C++ library that supports Partitioned Global Address Space
    (PGAS) programming, and is designed to interoperate smoothly and
    efficiently with MPI, OpenMP, CUDA and AMTs. It leverages GASNet-EX to
    deliver low-overhead, fine-grained communication, including Remote Memory
    Access (RMA) and Remote Procedure Call (RPC)."""

    homepage = "https://upcxx.lbl.gov"

    version('2019.3.2', '844722cb0e8c0bc649017fce86469457')

    variant('cuda', default=False,
            description='Builds a CUDA-enabled version of UPC++')

    variant('scheduler', values=('slurm', 'alps', 'user', 'none'),
            default=detect_scheduler(),
            description="Resource manager to use")
    conflicts('scheduler=none', when='platform=cray',
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
            if "scheduler=slurm" in self.spec:
                tty.warn("CROSS has been automatically set to %s."
                         % 'cray-aries-slurm')
                spack_env.set('CROSS', 'cray-aries-slurm')
            elif "scheduler=alps" in self.spec:
                tty.warn("CROSS has been automatically set to %s."
                         % 'cray-aries-alps')
                spack_env.set('CROSS', 'cray-aries-alps')
        if '+cuda' in self.spec:
            spack_env.set('UPCXX_CUDA', '1')
            spack_env.set('UPCXX_CUDA_NVCC', self.spec['cuda'].prefix.bin.nvcc)

    def setup_dependent_package(self, module, dep_spec):
        dep_spec.upcxx = self.prefix.bin.upcxx

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('UPCXX_INSTALL', self.prefix)
        spack_env.set('UPCXX', self.prefix.bin.upcxx)
        if 'platform=cray' in self.spec:
            spack_env.set('UPCXX_GASNET_CONDUIT', 'aries')

    def install(self, spec, prefix):
        installsh = Executable('./install')
        installsh(prefix)
