# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Nvshmem(MakefilePackage, CudaPackage):
    """NVSHMEM is a parallel programming interface based on OpenSHMEM that
    provides efficient and scalable communication for NVIDIA GPU
    clusters. NVSHMEM creates a global address space for data that spans
    the memory of multiple GPUs and can be accessed with fine-grained
    GPU-initiated operations, CPU-initiated operations, and operations on
    CUDA streams."""

    homepage = "https://developer.nvidia.com/nvshmem"

    maintainers = ['bvanessen']

    version('2.2.1-0', sha256='c8efc6cd560e0ed66d5fe4c5837c650247bec7b0dc65b5089deb8ab49658e1c3')
    version('2.1.2-0', sha256='367211808df99b4575fb901977d9f4347065c61a26642d65887f24d60342a4ec')
    version('2.0.3-0', sha256='20da93e8508511e21aaab1863cb4c372a3bec02307b932144a7d757ea5a1bad2')

    variant('cuda', default=True, description='Build with CUDA')
    variant('ucx', default=True, description='Build with UCX support')
    variant('nccl', default=True, description='Build with NCCL support')
    variant('gdrcopy', default=True, description='Build with gdrcopy support')
    variant('mpi', default=True, description='Build with MPI support')
    variant('shmem', default=False, description='Build with shmem support')
    conflicts('~cuda')

    def url_for_version(self, version):
        ver_str = '{0}'.format(version)
        directory = ver_str.split('-')[0]
        url_fmt = "https://developer.download.nvidia.com/compute/redist/nvshmem/{0}/source/nvshmem_src_{1}.txz"
        return url_fmt.format(directory, version)

    depends_on('mpi', when='+mpi')
    depends_on('ucx', when='+ucx')
    depends_on('gdrcopy', when='+gdrcopy')
    depends_on('nccl', when='+nccl')

    def setup_build_environment(self, env):
        env.set('CUDA_HOME', self.spec['cuda'].prefix)
        env.set('NVSHMEM_PREFIX', self.prefix)

        if '+ucx' in self.spec:
            env.set('NVSHMEM_UCX_SUPPORT', '1')
            env.set('UCX_HOME', self.spec['ucx'].prefix)

        if '+gdrcopy' in self.spec:
            env.set('NVSHMEM_USE_GDRCOPY', '1')
            env.set('GDRCOPY_HOME', self.spec['gdrcopy'].prefix)

        if '+nccl' in self.spec:
            env.set('NVSHMEM_USE_NCCL', '1')
            env.set('NCCL_HOME', self.spec['nccl'].prefix)

        if '+mpi' in self.spec:
            env.set('NVSHMEM_MPI_SUPPORT', '1')
            env.set('MPI_HOME', self.spec['mpi'].prefix)

            if self.spec.satisfies('^spectrum-mpi') or self.spec.satisfies('^openmpi'):
                env.set('NVSHMEM_MPI_IS_OMPI', '1')
            else:
                env.set('NVSHMEM_MPI_IS_OMPI', '0')

        if '+shmem' in self.spec:
            env.set('NVSHMEM_SHMEM_SUPPORT', '1')
            env.set('SHMEM_HOME', self.spec['mpi'].prefix)
