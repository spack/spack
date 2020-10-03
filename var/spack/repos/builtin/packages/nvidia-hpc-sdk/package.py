# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.util.prefix import Prefix
import os
import platform

_versions = {
    '20.7': {
        'Linux_aarch64': ('71ef81910ae00d2749a23bc1ca6e4a66', 'https://developer.download.nvidia.com/hpc-sdk/nvhpc_2020_207_Linux_aarch64_cuda_11.0.tar.gz'),
        'Linux_ppc64le': ('13210525ae495e86a0a8ecdf1a23251b', 'https://developer.download.nvidia.com/hpc-sdk/nvhpc_2020_207_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux_x86_64': ('71ef81910ae00d2749a23bc1ca6e4a66', 'https://developer.download.nvidia.com/hpc-sdk/nvhpc_2020_207_Linux_x86_64_cuda_multi.tar.gz')
    }
}

class NvidiaHpcSdk(Package):
    """The NVIDIA HPC SDK is a comprehensive suite of compilers and libraries 
    enabling HPC developers to program the entire HPC platform from the GPU 
    foundation to the CPU and through the interconnect. It is the only 
    comprehensive, integrated SDK for programming accelerated computing systems."""

    homepage = "https://developer.nvidia.com/hpc-sdk"

    maintainers = ['Nischay-Pro']

    for ver, packages in _versions.items():
        key = "{}_{}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version(ver, md5=pkg[0], url=pkg[1], expand=True)

    variant('network', default=True, description="Perform a network install")

    variant('single',  default=False, description="Perform a single system install")

    if platform.machine() != "aarch64":
        variant('cuda_version', default='11.0', description='Choose CUDA version', values=('11.0', '10.2', '10.1'), multi=False)
    else:
        variant('cuda_version', default='11.0', description='Choose CUDA version', values=('11.0'), multi=False)

    variant('mpi', default=False, description="Enable installation of Open MPI")

    depends_on('cuda')

    depends_on('cuda@11.0.2:',   when='cuda_version=11.0')
    depends_on('cuda@10.2.89:',  when='cuda_version=10.2')
    depends_on('cuda@10.1.243:', when='cuda_version=10.1')

    def install(self, spec, prefix):
        # Enable the silent installation feature
        os.environ['NVHPC_SILENT'] = 'true'
        os.environ['NVHPC_INSTALL_DIR'] = prefix

        if '+network' in spec and '~single' in spec:
            os.environ['NVHPC_INSTALL_TYPE'] = "network"
            os.environ['NVHPC_INSTALL_LOCAL_DIR'] = "{}/{}/shared_objects".format(prefix, self.version)
        elif '+single' in spec and '~network' in spec:
            os.environ['NVHPC_INSTALL_TYPE'] = "single"
        else:
            msg  = 'You must choose either a network install or a single '
            msg += 'system install.\nYou cannot choose both.'
            raise RuntimeError(msg)

        cuda_version = self.spec.variants['cuda_version'].value
        os.environ['NVHPC_DEFAULT_CUDA'] = cuda_version

        os.system('./install')
    
    def setup_run_environment(self, env):
        prefix = Prefix(join_path(self.prefix, '{}_{}'.format(platform.system(), platform.machine()), self.version))

        env.set('target', '{}_{}'.format(platform.system(), platform.machine()))
        env.set('version', str(self.version))
        env.set('NVHPC', prefix)

        env.prepend_path('PATH', prefix.compilers.bin)
        env.prepend_path('MANPATH', prefix.compilers.man)
        env.prepend_path('LD_LIBRARY_PATH', prefix.compilers.lib)

        env.prepend_path('CPATH', prefix.cuda.include)
        env.prepend_path('CPATH', prefix.compilers.include)
        env.prepend_path('CPATH', prefix.math_libs.include)

        env.prepend_path('LD_LIBRARY_PATH', prefix.cuda.lib64)
        env.prepend_path('LD_LIBRARY_PATH', prefix.compilers.lib)
        env.prepend_path('LD_LIBRARY_PATH', prefix.math_libs.lib64)

        env.set('CC',  join_path(prefix.compilers.bin, 'nvc'))
        env.set('CXX', join_path(prefix.compilers.bin, 'nvc++'))
        env.set('F77', join_path(prefix.compilers.bin, 'nvfortran'))
        env.set('F90', join_path(prefix.compilers.bin, 'nvfortran'))
        env.set('FC',  join_path(prefix.compilers.bin, 'nvfortran'))
        env.set('CPP',  'cpp')

        if '+mpi' in self.spec:
            env.prepend_path('PATH', prefix.comm_libs.mpi.bin)
            env.prepend_path('PATH', prefix.comm_libs.nccl.bin)
            env.prepend_path('PATH', prefix.comm_libs.nvshmem.bin)

            env.prepend_path('CPATH', prefix.comm_libs.mpi.include)
            env.prepend_path('CPATH', prefix.comm_libs.nccl.include)
            env.prepend_path('CPATH', prefix.comm_libs.nvshmem.include)

            env.prepend_path('LD_LIBRARY_PATH', prefix.comm_libs.mpi.lib)
            env.prepend_path('LD_LIBRARY_PATH', prefix.comm_libs.nccl.lib)
            env.prepend_path('LD_LIBRARY_PATH', prefix.comm_libs.nvshmem.lib)
