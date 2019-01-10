# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    version('0.1', sha256='3880b736866e439dd94e6a61eeeb5bb2abccebbac82b82d52033bc6c94950bdb')

    variant('gpu', default=False, description='Builds with support for GPUs via CUDA and cuDNN')
    variant('nccl', default=False, description='Builds with support for NCCL communication lib')
    variant('mpi_cuda', default=False, description='Builds with support for MPI-CUDA enabled library')

    depends_on('cmake@3.9.0:', type='build')
    depends_on('cuda', when='+gpu')
    depends_on('cudnn', when='+gpu')
    depends_on('cub', when='+gpu')
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
