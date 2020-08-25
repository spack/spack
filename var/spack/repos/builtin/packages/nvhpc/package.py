# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

class Nvhpc(Package):
    """The NVIDIA HPC Software Development Kit (SDK) includes the proven compilers,
       libraries and software tools essential to maximizing developer productivity
       and the performance and portability of HPC applications.
    """

    homepage = "https://developer.nvidia.com/hpc-sdk"
    url      = "https://developer.download.nvidia.com/hpc-sdk/nvhpc_2020_207_Linux_x86_64_cuda_multi.tar.gz"

    maintainers = ['ajkotobi']

    version('2020_207_Linux_x86_64_cuda_multi', sha256='a5c5c8726d2210f2310a852c6d6e03c9ef8c75e3643e9c94e24909f5e9c2ea7a')

    variant(
        'cuda', default='11.0', description='List of CUDA that are enabled',
        values=('11.0', '10.2', '10.1'), multi=False
    )

    variant(
        'network', default='network', description='Network installation',
        values=('network', 'single'), multi=False
    )

    def install(self, spec, prefix):

        os.environ['NVHPC_SILENT'] = "true"
        os.environ['NVHPC_INSTALL_DIR'] = self.prefix
        os.environ['NVHPC_DEFAULT_CUDA'] = self.spec.variants['cuda'].value
        os.environ['NVHPC_INSTALL_TYPE'] = self.spec.variants['network'].value
        os.environ['NVHPC_INSTALL_LOCAL_DIR'] = self.prefix

        os.system("./install")
