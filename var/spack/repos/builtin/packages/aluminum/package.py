# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Aluminum(CMakePackage):
    """Aluminum provides a generic interface to high-performance
    communication libraries, with a focus on allreduce
    algorithms. Blocking and non-blocking algorithms and GPU-aware
    algorithms are supported. Aluminum also contains custom
    implementations of select algorithms to optimize for certain
    situations."""

    homepage = "https://github.com/LLNL/Aluminum"
    url      = "https://github.com/LLNL/Aluminum/archive/v0.1.tar.gz"
    git      = "https://github.com/LLNL/Aluminum.git"

    version('master', branch='master')
    version('0.3.3',   sha256='26e7f263f53c6c6ee0fe216e981a558dfdd7ec997d0dd2a24285a609a6c68f3b')
    version('0.3.2',   sha256='09b6d1bcc02ac54ba269b1123eee7be20f0104b93596956c014b794ba96b037f')
    version('0.2.1-1', sha256='066b750e9d1134871709a3e2414b96b166e0e24773efc7d512df2f1d96ee8eef')
    version('0.2.1', sha256='3d5d15853cccc718f60df68205e56a2831de65be4d96e7f7e8497097e7905f89')
    version('0.2', sha256='fc8f06c6d8faab17a2aedd408d3fe924043bf857da1094d5553f35c4d2af893b')
    version('0.1', sha256='3880b736866e439dd94e6a61eeeb5bb2abccebbac82b82d52033bc6c94950bdb')

    variant('gpu', default=False, description='Builds with support for GPUs via CUDA and cuDNN')
    variant('nccl', default=False, description='Builds with support for NCCL communication lib')
    variant('mpi_cuda', default=False, description='Builds with support for MPI-CUDA enabled library')

    depends_on('cmake@3.9.0:', type='build')
    depends_on('cuda', when='+gpu')
    depends_on('mpi')
    depends_on('nccl', when='+nccl')
    depends_on('hwloc')

    generator = 'Ninja'
    depends_on('ninja', type='build')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DALUMINUM_ENABLE_CUDA:BOOL=%s' % ('+gpu' in spec),
            '-DALUMINUM_ENABLE_MPI_CUDA:BOOL=%s' % ('+mpi_cuda' in spec),
            '-DALUMINUM_ENABLE_NCCL:BOOL=%s' % ('+nccl' in spec)]
        return args
